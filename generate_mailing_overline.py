# -*- coding: utf-8 -*-
"""
Genera el mailing del Maillot Hombre Overline en Google Docs.
Doc: 1dMyhyLfczC24P6m6QO3osI5Yis-ttAfzS1zIC8QD9DU  Tab: hvbmsx1uk239
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1dMyhyLfczC24P6m6QO3osI5Yis-ttAfzS1zIC8QD9DU"
TAB_ID = "t.hvbmsx1uk239"

# ── HELPERS ────────────────────────────────────────────────────────────────
def utf16_len(text):
    return sum(2 if ord(c) > 0xFFFF else 1 for c in text)

def loc(idx):
    return {"index": idx, "tabId": TAB_ID}

def rng(s, e):
    return {"startIndex": s, "endIndex": e, "tabId": TAB_ID}

def get_tab_end(service):
    doc = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
    for tab in doc.get("tabs", []):
        if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
            body = tab.get("documentTab", {}).get("body", {}).get("content", [])
            if body:
                return max(1, body[-1].get("endIndex", 2) - 1)
    return 1

def find_last_table(service, approx_pos):
    doc = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
    best = None
    for tab in doc.get("tabs", []):
        if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
            for el in tab.get("documentTab", {}).get("body", {}).get("content", []):
                if "table" in el and abs(el.get("startIndex", 0) - approx_pos) <= 10:
                    best = (el["table"], el.get("startIndex", approx_pos))
    return best  # (table, table_start_index) or None

# ── CONTENIDO ──────────────────────────────────────────────────────────────
# style: 'normal' | 'bold' | 'bold+underline' | 'bullet'
SECTIONS = [
    ('text', [
        ('ASUNTO: El calor tiene nombre propio', 'normal'),
        ('PREENCABEZADO: El Overline: mid-mesh, ultra-ligero y construido para rodar en verano.', 'normal'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Ciclista en ruta con el Overline, luz dura de verano, velocidad alta. Plano lateral o tres cuartos.',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+summer+mesh+road+speed',
    ]),
    ('text', [
        ('', 'normal'),
        ('30 grados. El asfalto devuelve el calor. El ritmo no baja y el cuerpo te pide que el equipo haga su parte.', 'normal'),
        ('', 'normal'),
        ('Es ahí donde el Overline demuestra por qué existe.', 'normal'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Plano cerrado del tejido mid-mesh en movimiento',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+mesh+fabric+closeup+lightweight',
    ]),
    ('text', [
        ('', 'normal'),
        ('Tejido mid-mesh ultra-ligero y ultra-elástico. Estructura semi-abierta que deja pasar el aire de forma constante. Sin acumulación de calor. Sin pérdida de vatios por culpa del equipo.', 'bullet'),
        ('Secado rápido. La humedad desaparece antes de que la notes. Solo ruedas.', 'bullet'),
        ('Patrón aerodinámico que reduce la resistencia frontal y elimina arrugas abdominales. El maillot trabaja contigo, no contra ti.', 'bullet'),
        ('Mangas extendidas con acabado seamless. Sin costuras, sin rozaduras en los brazos. Solo kilómetros.', 'bullet'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Detalle trasero — bolsillos lumbares de perfil bajo con gel y móvil, silueta aerodinámica sin bultos.',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+back+pockets+aero+summer',
    ]),
    ('text', [
        ('', 'normal'),
        ('Tres bolsillos lumbares de perfil bajo. Todo lo que necesitas sin romper la aerodinámica. Geles, el móvil, la alimentación del fondo. Todo en su sitio.', 'bullet'),
        ('Cintura seamless con banda elástica integrada. Estabilidad total en el pedaleo. Sin que se mueva sola.', 'bullet'),
        ('Disponible en 3 colores: Lime Green, Waxy Yellow, Cream. Desde €135.', 'bullet'),
        ('', 'normal'),
    ]),
    ('cta', 'VER EL OVERLINE →'),
    ('text', [
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Grid de los 3 colorways del Overline sobre fondo limpio — Lime Green, Waxy Yellow, Cream',
    ]),
]

# ── MAIN ───────────────────────────────────────────────────────────────────
creds = get_google_credentials()
service = build("docs", "v1", credentials=creds)

# 1. Clear existing content
print("Leyendo y limpiando tab...")
end_idx = get_tab_end(service)
if end_idx > 1:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [{"deleteContentRange": {"range": rng(1, end_idx)}}]}
    ).execute()
    print(f"  Contenido anterior eliminado (1 a {end_idx}).")

# Tracking for deferred formatting (bold/underline on text sections)
all_bold_ranges = []
all_underline_ranges = []
all_imgbox_text_ranges = []  # for gray color

# 2. Process sections
for sec_type, sec_data in SECTIONS:

    if sec_type == 'text':
        current_end = get_tab_end(service)
        idx = current_end
        insert_reqs = []
        bullet_ranges_this = []

        for text, style in sec_data:
            is_bullet = style == 'bullet'
            full = text + "\n"
            n = utf16_len(full)
            insert_reqs.append({"insertText": {"location": loc(idx), "text": full}})
            if text:
                if 'bold' in style:
                    all_bold_ranges.append((idx, idx + n))
                if 'underline' in style:
                    all_underline_ranges.append((idx, idx + n))
                if is_bullet:
                    bullet_ranges_this.append((idx, idx + n))
            idx += n

        bullet_reqs = [
            {"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
            for s, e in bullet_ranges_this
        ]
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": insert_reqs + bullet_reqs}
        ).execute()
        print(f"  Bloque de texto insertado (idx {current_end} a {idx}).")

    elif sec_type == 'imgbox':
        approx_pos = get_tab_end(service)
        # Insert 1-row 1-col table
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertTable": {"rows": 1, "columns": 1, "location": loc(approx_pos)}}]}
        ).execute()
        result = find_last_table(service, approx_pos)
        if result:
            table, tbl_start = result
            cell_el = table["tableRows"][0]["tableCells"][0]
            insert_idx = cell_el["content"][0]["startIndex"]
            cell_text = "\n".join(sec_data)
            n = utf16_len(cell_text)
            cell_reqs = [
                {"insertText": {"location": loc(insert_idx), "text": cell_text}},
                # Center-align the cell paragraph
                {"updateParagraphStyle": {
                    "range": rng(insert_idx, insert_idx + n),
                    "paragraphStyle": {"alignment": "CENTER"},
                    "fields": "alignment",
                }},
                # Gray background
                {"updateTableCellStyle": {
                    "tableRange": {
                        "tableCellLocation": {
                            "tableStartLocation": loc(tbl_start),
                            "rowIndex": 0,
                            "columnIndex": 0,
                        },
                        "rowSpan": 1,
                        "columnSpan": 1,
                    },
                    "tableCellStyle": {
                        "backgroundColor": {
                            "color": {"rgbColor": {"red": 0.933, "green": 0.933, "blue": 0.933}}
                        }
                    },
                    "fields": "backgroundColor",
                }},
            ]
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": cell_reqs}).execute()
            all_imgbox_text_ranges.append((insert_idx, insert_idx + n))
        # Empty line after table
        new_end = get_tab_end(service)
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertText": {"location": loc(new_end), "text": "\n"}}]}
        ).execute()
        print(f"  Caja de imagen insertada.")

    elif sec_type == 'cta':
        approx_pos = get_tab_end(service)
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertTable": {"rows": 1, "columns": 1, "location": loc(approx_pos)}}]}
        ).execute()
        result = find_last_table(service, approx_pos)
        if result:
            table, _ = result
            cell_el = table["tableRows"][0]["tableCells"][0]
            insert_idx = cell_el["content"][0]["startIndex"]
            n = utf16_len(sec_data)
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={"requests": [
                    {"insertText": {"location": loc(insert_idx), "text": sec_data}},
                    {"updateTextStyle": {
                        "range": rng(insert_idx, insert_idx + n),
                        "textStyle": {"bold": True},
                        "fields": "bold",
                    }},
                ]}
            ).execute()
        new_end = get_tab_end(service)
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertText": {"location": loc(new_end), "text": "\n"}}]}
        ).execute()
        print(f"  CTA insertado.")

# 3. Apply Arial 11 globally
print("Aplicando Arial 11...")
total_end = get_tab_end(service)
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"updateTextStyle": {
        "range": rng(1, total_end),
        "textStyle": {
            "weightedFontFamily": {"fontFamily": "Arial"},
            "fontSize": {"magnitude": 11, "unit": "PT"},
        },
        "fields": "weightedFontFamily,fontSize",
    }}]}
).execute()
print(f"  Arial 11 aplicado (1 a {total_end}).")

# 4. Apply bold (last — overwrites any reset from Arial pass)
if all_bold_ranges:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"updateTextStyle": {"range": rng(s, e), "textStyle": {"bold": True}, "fields": "bold"}}
            for s, e in all_bold_ranges
        ]}
    ).execute()
    print(f"  {len(all_bold_ranges)} rangos en negrita.")

# 5. Apply underline
if all_underline_ranges:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"updateTextStyle": {"range": rng(s, e), "textStyle": {"underline": True}, "fields": "underline"}}
            for s, e in all_underline_ranges
        ]}
    ).execute()
    print(f"  {len(all_underline_ranges)} rangos subrayados.")

# 6. Apply gray color to image box text
if all_imgbox_text_ranges:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"updateTextStyle": {
                "range": rng(s, e),
                "textStyle": {"foregroundColor": {"color": {"rgbColor": {
                    "red": 0.333, "green": 0.333, "blue": 0.333
                }}}},
                "fields": "foregroundColor",
            }}
            for s, e in all_imgbox_text_ranges
        ]}
    ).execute()
    print(f"  {len(all_imgbox_text_ranges)} cajas de imagen con texto gris.")

print("\nMailing Overline completado.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
