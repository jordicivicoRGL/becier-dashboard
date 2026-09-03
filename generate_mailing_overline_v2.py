# -*- coding: utf-8 -*-
"""
Genera el mailing del Maillot Hombre Overline (enfoque comodidad/entreno) en Google Docs.
Doc: 1dMyhyLfczC24P6m6QO3osI5Yis-ttAfzS1zIC8QD9DU  Tab: t.9hk1gpwnz1gu
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1dMyhyLfczC24P6m6QO3osI5Yis-ttAfzS1zIC8QD9DU"
TAB_ID = "t.9hk1gpwnz1gu"

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
    return best

SECTIONS = [
    ('text', [
        ('ASUNTO: Para rodar horas sin pensar en el maillot', 'normal'),
        ('PREENCABEZADO: Ultra elástico, sin manchas de sudor. El maillot del entrenamiento diario.', 'normal'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Ciclista en ruta larga, luz suave de mañana o tarde. Plano lateral o tres cuartos.',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+long+ride+training+road',
    ]),
    ('text', [
        ('', 'normal'),
        ('Hay salidas que duran cuatro horas. Días en que el ritmo no baja y el cuerpo te pide que el equipo haga su parte.', 'normal'),
        ('', 'normal'),
        ('El Overline está diseñado exactamente para eso.', 'normal'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Plano cerrado del tejido en movimiento, detalle del ajuste sobre el cuerpo',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+elastic+fit+body+closeup',
    ]),
    ('text', [
        ('', 'normal'),
        ('Tejido ultra elástico que se adapta a cualquier tipo de cuerpo como una segunda piel. Sin tirones ni zonas de presión.', 'bullet'),
        ('Absorbe la humedad sin dejar marcas de sudor en el tejido. La transpirabilidad hace el trabajo; tú solo ruedas.', 'bullet'),
        ('Estructura semiabierta de alta transpiración. El aire circula, el calor no se acumula.', 'bullet'),
        ('Peso ultraligero. En salidas largas, no notarás que lo llevas.', 'bullet'),
        ('', 'normal'),
    ]),
    ('imgbox', [
        'IMAGEN: Detalle trasero con bolsillos lumbares y cintura, plano lateral en movimiento',
        'Referencia Pinterest: pinterest.com/search/pins/?q=cycling+jersey+back+pockets+waist+fit',
    ]),
    ('text', [
        ('', 'normal'),
        ('Mangas de largo ampliado con acabado limpio, sin dobladillos. Sin rozaduras en los brazos, kilómetro tras kilómetro.', 'bullet'),
        ('Cintura sin costuras con banda elástica integrada. Ajuste seguro en cada pedalada. No se mueve.', 'bullet'),
        ('Tres bolsillos traseros de perfil bajo. Geles, móvil y alimentación del fondo. Todo en su sitio, sin bultos.', 'bullet'),
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

creds = get_google_credentials()
service = build("docs", "v1", credentials=creds)

print("Leyendo y limpiando tab...")
end_idx = get_tab_end(service)
if end_idx > 1:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [{"deleteContentRange": {"range": rng(1, end_idx)}}]}
    ).execute()
    print(f"  Contenido anterior eliminado (1 a {end_idx}).")

all_bold_ranges = []
all_underline_ranges = []
all_imgbox_text_ranges = []

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
                {"updateParagraphStyle": {
                    "range": rng(insert_idx, insert_idx + n),
                    "paragraphStyle": {"alignment": "CENTER"},
                    "fields": "alignment",
                }},
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
        new_end = get_tab_end(service)
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertText": {"location": loc(new_end), "text": "\n"}}]}
        ).execute()
        print("  Caja de imagen insertada.")

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
        print("  CTA insertado.")

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

if all_bold_ranges:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"updateTextStyle": {"range": rng(s, e), "textStyle": {"bold": True}, "fields": "bold"}}
            for s, e in all_bold_ranges
        ]}
    ).execute()
    print(f"  {len(all_bold_ranges)} rangos en negrita.")

if all_underline_ranges:
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"updateTextStyle": {"range": rng(s, e), "textStyle": {"underline": True}, "fields": "underline"}}
            for s, e in all_underline_ranges
        ]}
    ).execute()
    print(f"  {len(all_underline_ranges)} rangos subrayados.")

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

print("\nMailing Overline v2 completado.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
