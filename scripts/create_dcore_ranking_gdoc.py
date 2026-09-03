# -*- coding: utf-8 -*-
"""Crea un Google Doc de ranking de creatividades DCORE en una carpeta de Drive."""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "10nsEVlzCNNbIuLsGiz4pN3OkVDGIqWYUUuhglZ0I9I8"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

doc = docs.documents().get(documentId=DOC_ID).execute()
END = doc["body"]["content"][-1]["endIndex"] - 1  # punto de inserción actual


def refresh_end():
    global END
    d = docs.documents().get(documentId=DOC_ID).execute()
    END = d["body"]["content"][-1]["endIndex"] - 1
    return d


def append_block(text, style="NORMAL", bullet=False):
    """Inserta un bloque de texto al final, aplica estilo de párrafo y negrita para **texto**."""
    global END
    bold_spans = []
    clean = ""
    i = 0
    while i < len(text):
        if text[i:i+2] == "**":
            j = text.index("**", i + 2)
            start = len(clean)
            clean += text[i+2:j]
            bold_spans.append((start, len(clean)))
            i = j + 2
        else:
            clean += text[i]
            i += 1

    full_text = clean + "\n"
    start_idx = END
    end_idx = start_idx + len(full_text)

    requests = [
        {"insertText": {"location": {"index": start_idx}, "text": full_text}}
    ]

    if style == "HEADING_1":
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start_idx, "endIndex": end_idx},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType",
            }
        })
    elif style == "HEADING_2":
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start_idx, "endIndex": end_idx},
                "paragraphStyle": {"namedStyleType": "HEADING_2"},
                "fields": "namedStyleType",
            }
        })
    elif style == "NORMAL_TEXT":
        pass

    if bullet:
        requests.append({
            "createParagraphBullets": {
                "range": {"startIndex": start_idx, "endIndex": end_idx},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })

    for b_start, b_end in bold_spans:
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start_idx + b_start, "endIndex": start_idx + b_end},
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        })

    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    END = end_idx


def insert_table(headers, rows):
    """Inserta una tabla al final y la rellena. Devuelve tras completarla."""
    global END
    n_cols = len(headers)
    n_rows = len(rows) + 1

    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
        {"insertTable": {"location": {"index": END}, "rows": n_rows, "columns": n_cols}}
    ]}).execute()

    d = refresh_end()
    # localizar la tabla recién insertada (última tabla del body)
    table_el = None
    for el in d["body"]["content"]:
        if "table" in el:
            table_el = el
    cells = []  # lista de (row, col, startIndex)
    for r_idx, row in enumerate(table_el["table"]["tableRows"]):
        for c_idx, cell in enumerate(row["tableCells"]):
            cell_start = cell["content"][0]["startIndex"]
            cells.append((r_idx, c_idx, cell_start))

    all_rows = [headers] + rows
    # rellenar de última celda a primera para no invalidar índices
    cells_sorted = sorted(cells, key=lambda x: x[2], reverse=True)
    requests = []
    header_bold_ranges = []
    for r_idx, c_idx, cell_start in cells_sorted:
        text = str(all_rows[r_idx][c_idx])
        if text:
            requests.append({"insertText": {"location": {"index": cell_start}, "text": text}})
        if r_idx == 0 and text:
            header_bold_ranges.append((cell_start, cell_start + len(text)))
    if requests:
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

    if header_bold_ranges:
        bold_requests = [
            {"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "textStyle": {"bold": True},
                "fields": "bold",
            }}
            for s, e in header_bold_ranges
        ]
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": bold_requests}).execute()

    refresh_end()


# =========================================================
# CONTENIDO
# =========================================================

append_block("Ranking de creatividades — DCORE", style="HEADING_1")
append_block("Periodo: 13 jul – 12 ago 2026")
append_block("Filtro: anuncios activos, gasto ≥ 150€, campañas Lead Ad (sin posts impulsados)")

append_block("Campañas REFORMAS", style="HEADING_2")

headers = ["Anuncio", "Comentario (¿de qué trata?)", "Coste", "Leads", "CPL", "CTR", "Hook Rate", "Hold Rate"]

reformas_rows = [
    ["Copy of SUBVENCIONES REDES", "Hablando a cámara en la calle: ahorrar más de 15.000€ en tu reforma gracias a las subvenciones del estado", "1.028,33€", "42", "24,48€", "1,62%", "35,42%", "20,30%"],
    ["CHALET VERANO", "Hablando a cámara en un chalet: reformar el chalet en verano mientras el dueño disfruta de sus vacaciones", "200,68€", "7", "28,67€", "0,95%", "42,54%", "15,91%"],
    ["DETALLADO-Campaña presupuesto detallado.MOV", "Hablando a cámara en la oficina: en Dcore se entregan los presupuestos detallados partida por partida. Estudio de arquitectura y constructora propia", "3.136,29€", "106", "29,59€", "0,79%", "19,27%", "16,68%"],
    ["SERVICIO EVO-EVO Lourdes.MOV", "Tipo entrevista en la oficina: improvisar durante la obra tiene un precio y acaba encareciendo la obra", "1.845,29€", "54", "34,17€", "4,12%", "14,17%", "26,53%"],
    ["FALTA DE TIEMPO-Falta de tiempo para supervisar.MOV", "Hablando a cámara en la oficina: ¿no tienes tiempo de estar pendiente de la obra? Dcore se encarga de todo", "221,80€", "5", "44,36€", "0,95%", "21,26%", "20,72%"],
    ["QUIERES REFORMAR HOY MISMO", "Hablando a cámara en la oficina: presupuesto detallado", "268,99€", "5", "53,80€", "0,39%", "17,60%", "16,77%"],
    ["24072026-CAMPAÑA COCINA VIDEO 2 FORMATO 2", "Hablando a cámara en una cocina: si quieres reformar, te regalamos la cocina", "350,41€", "6", "58,40€", "0,78%", "21,23%", "21,69%"],
    ["Copy of CHALET REDES", "Hablando en la calle: si un chalet vale más de 5M€ no puedes reformarlo de cualquier manera. Dcore entiende de arquitectura y diseño", "631,01€", "10", "63,10€", "1,37%", "32,43%", "30,30%"],
    ["9-16-REFORMA OK - Copia", "Hablando a cámara en una casa: ¿llevas meses pensando en reformar? Empieza hoy mismo", "165,52€", "2", "82,76€", "0,93%", "31,52%", "19,84%"],
    ["Vi_deo_chalet_4x5.mp4", "Hablando en la calle: lo caro de un chalet es reformarlo dos veces por decisiones improvisadas. En Dcore lo cerramos todo antes de empezar", "177,94€", "0", "—", "1,23%", "24,99%", "24,01%"],
]

insert_table(headers, reformas_rows)

append_block("Análisis de ángulos — REFORMAS", style="HEADING_2")
append_block("Agrupando los anuncios por el ángulo o mensaje que usan (más allá del vídeo concreto), esto es lo que mejor funciona:")

append_block(
    "**Ahorro y subvenciones (beneficio económico concreto):** ángulo con el mejor equilibrio de la cuenta — CPL más bajo con volumen real (24,48€ / 42 leads) y el segundo mejor hook rate (35,42%). Decir un ahorro concreto en euros, dicho en la calle, es el mensaje más rentable de todos.",
    bullet=True,
)
append_block(
    "**Presupuesto detallado / transparencia (racional):** es el ángulo que más volumen aporta con diferencia — 111 leads combinados entre sus dos anuncios, con un CPL medio de ~30,7€. El hook rate es de los más bajos (17-19%), así que el enganche inicial es débil, pero el argumento racional convence a quien se queda a verlo. La ejecución importa mucho dentro del mismo ángulo: el CPL varía de 29,59€ a 53,80€ entre sus dos versiones.",
    bullet=True,
)
append_block(
    "**Chalets (premium / estacional):** es el ángulo que más engancha visualmente — agrupa los mejores hook rates de la cuenta (32-43%) y también el mejor hold rate (30,30%, versión chalet +5M€). A cambio el volumen es bajo (0-10 leads por anuncio) y el CPL premium es de los más altos (63,10€), coherente con un target de ticket alto: menos leads, pero previsiblemente más cualificados.",
    bullet=True,
)
append_block(
    "**Servicio y gestión sin esfuerzo (evitar improvisar, ahorrar tiempo):** el formato entrevista (Servicio EVO) genera el CTR más alto de toda la cuenta (4,12%, el resto ronda 1%), pero el hook rate es el más bajo (14,17%) — el copy/miniatura interesa mucho antes del clic, pero el arranque del vídeo no retiene. El resto del ángulo (falta de tiempo) rinde de forma más discreta (CPL 44,36€).",
    bullet=True,
)
append_block(
    "**Urgencia sin beneficio racional:** es el ángulo más caro que sí convierte (CPL 82,76€, solo 2 leads) — engancha razonablemente (hook 31,52%) pero no cierra. Mejor combinarlo siempre con un beneficio racional (ahorro, transparencia, tranquilidad) que usarlo solo.",
    bullet=True,
)

append_block("Anuncios con mejor Hook Rate", style="HEADING_2")
append_block("Los 3 anuncios con mejor hook rate de la tabla REFORMAS, para revisar el vídeo y valorar qué hace que funcionen:")
append_block("**Chalet verano** — 42,54%", bullet=True)
append_block("**Subvenciones redes** — 35,42%", bullet=True)
append_block("**Chalet redes (+5M€)** — 32,43%", bullet=True)
append_block("Notas:")
append_block("")
append_block("")
append_block("")
append_block("")

append_block("Otras conclusiones", style="HEADING_2")
append_block(
    "Grabar en la calle tiende a dar mejor hook rate que grabar en la oficina; el único caso que rompe el patrón es el formato entrevista (EVO), que gana en CTR pero no en hook rate.",
    bullet=True,
)
append_block(
    "Living tiene el CPL más bajo de toda la cuenta (19-20€) pero también el hook rate más bajo (9-14%) — capta leads baratos sin depender del enganche del vídeo, probablemente por un público ya predispuesto.",
    bullet=True,
)
append_block(
    "Cocinas rinde de forma sólida y consistente (CPL 30-33€, hook 21-32%), sin outliers destacables.",
    bullet=True,
)
append_block(
    "B2B tiene el segundo CTR más alto de la cuenta (2,27%) pero un CPL más alto que Living o Cocinas (37,45€) — el clic es fácil de conseguir, la conversión a lead cuesta más.",
    bullet=True,
)
append_block(
    "El vídeo de chalet en 4x5 (177,94€ gastados, 0 leads) tiene buen hook/hold rate — vigilar si el formato 4x5 rinde peor que el 9:16 para el ángulo chalet, o si simplemente falta volumen todavía.",
    bullet=True,
)

append_block("Living, Cocinas y B2B", style="HEADING_2")

lcb_rows = [
    ["9-16-VID-LIVING-Copy of LIVING CHECK PATI.mov (MAD PROS LIVING)", "", "477,84€", "25", "19,11€", "1,88%", "14,25%", "20,24%"],
    ["9-16-VID-LIVING-0126 (5)(3).mov (MAD PROS LIVING)", "", "476,57€", "24", "19,86€", "0,98%", "9,36%", "17,18%"],
    ["4-5-9-16-COCINA-VIDEO COCINA DCORE.mov (MAD PROS COCINAS)", "", "668,10€", "22", "30,37€", "1,14%", "25,23%", "29,35%"],
    ["9-16-VID-COCINAS-Campaña Cocinas.MOV (MAD PROS COCINAS)", "", "332,52€", "10", "33,25€", "1,00%", "31,85%", "29,42%"],
    ["9-16-VID-LOCAL-Copy of VÍDEO FINAL.mov (MAD PROS B2B)", "", "861,40€", "23", "37,45€", "2,27%", "15,62%", "29,02%"],
]

insert_table(headers, lcb_rows)

append_block("Ordenado por CPL ascendente (mejor a peor). Hook Rate = video views (3s) / impresiones · Hold Rate = ThruPlays / video views (3s).")

print("Documento listo: https://docs.google.com/document/d/%s/edit" % DOC_ID)
