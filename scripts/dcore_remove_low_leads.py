# -*- coding: utf-8 -*-
"""Elimina filas con <4 leads de la tabla REFORMAS y reescribe el análisis del Google Doc DCORE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1CYJyg4ca6xUM1raULMPhXQ2ZOx92DwJi2EFJ5VkM67g"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

TO_REMOVE = ["9-16-REFORMA OK", "Vi_deo_chalet_4x5"]

# --- 1. localizar la tabla REFORMAS y las filas a borrar ---
doc = docs.documents().get(documentId=DOC_ID).execute()

table_el = None
for el in doc["body"]["content"]:
    if "table" in el:
        table_el = el
        break  # la primera tabla del doc es REFORMAS

table_start = table_el["startIndex"]
rows_to_delete = []
for r_idx, row in enumerate(table_el["table"]["tableRows"]):
    row_text = ""
    for cell in row["tableCells"]:
        for content_el in cell["content"]:
            if "paragraph" not in content_el:
                continue
            for run in content_el["paragraph"].get("elements", []):
                row_text += run.get("textRun", {}).get("content", "")
    if any(name in row_text for name in TO_REMOVE):
        rows_to_delete.append(r_idx)

print("Filas a borrar (índices):", rows_to_delete)

requests = []
for r_idx in sorted(rows_to_delete, reverse=True):
    requests.append({
        "deleteTableRow": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start},
                "rowIndex": r_idx,
                "columnIndex": 0,
            }
        }
    })

if requests:
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    print("Filas borradas.")
else:
    print("No se encontraron filas para borrar.")

# --- 2. Reescribir el bloque de análisis (ahora sin el ángulo de urgencia ni la mención al 4x5) ---
doc = docs.documents().get(documentId=DOC_ID).execute()


def iter_paragraphs(content):
    for el in content:
        if "paragraph" in el:
            text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in el["paragraph"].get("elements", [])
            )
            yield el["startIndex"], el["endIndex"], text
        elif "table" in el:
            for row in el["table"]["tableRows"]:
                for cell in row["tableCells"]:
                    yield from iter_paragraphs(cell["content"])


paras = list(iter_paragraphs(doc["body"]["content"]))

start_idx = None
end_idx = None
for s, e, text in paras:
    if "Análisis de ángulos" in text and "REFORMAS" in text:
        start_idx = s
    if "vigilar si el formato 4x5" in text or "Otras conclusiones" in text:
        pass
    if "El clic es fácil de conseguir" in text or "la conversión a lead cuesta más" in text:
        end_idx = e

assert start_idx is not None, "No se encontró el inicio del análisis"
assert end_idx is not None, "No se encontró el final del análisis"

ACCENT = {"red": 0xB5 / 255, "green": 0x50 / 255, "blue": 0x2F / 255}

docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
    {"deleteContentRange": {"range": {"startIndex": start_idx, "endIndex": end_idx}}}
]}).execute()

END = start_idx


def append(text, heading=False):
    global END
    full = text + "\n"
    s = END
    e = s + len(full)
    requests = [{"insertText": {"location": {"index": s}, "text": full}}]
    if heading:
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "textStyle": {"bold": True, "fontSize": {"magnitude": 13, "unit": "PT"}, "foregroundColor": {"color": {"rgbColor": ACCENT}}},
                "fields": "bold,fontSize,foregroundColor",
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"spaceAbove": {"magnitude": 12, "unit": "PT"}, "spaceBelow": {"magnitude": 12, "unit": "PT"}},
                "fields": "spaceAbove,spaceBelow",
            }
        })
    else:
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "textStyle": {"fontSize": {"magnitude": 9.5, "unit": "PT"}, "bold": False},
                "fields": "fontSize,bold",
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"spaceBelow": {"magnitude": 4, "unit": "PT"}},
                "fields": "spaceBelow",
            }
        })
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    END = e


def bullet(text):
    append("•  " + text)


append("Análisis de ángulos — REFORMAS", heading=True)
append("Agrupando los anuncios por el ángulo o mensaje que usan (más allá del vídeo concreto), esto es lo que mejor funciona. Se excluyen los anuncios con menos de 4 leads por falta de datos suficientes.")
bullet("Ahorro y subvenciones (beneficio económico concreto): ángulo con el mejor equilibrio de la cuenta — CPL más bajo con volumen real (24,48€ / 42 leads) y el segundo mejor hook rate (35,42%). Decir un ahorro concreto en euros, dicho en la calle, es el mensaje más rentable de todos.")
bullet("Presupuesto detallado / transparencia (racional): es el ángulo que más volumen aporta con diferencia — 111 leads combinados entre sus dos anuncios, con un CPL medio de ~30,7€. El hook rate es de los más bajos (17-19%), así que el enganche inicial es débil, pero el argumento racional convence a quien se queda a verlo. La ejecución importa mucho dentro del mismo ángulo: el CPL varía de 29,59€ a 53,80€ entre sus dos versiones.")
bullet("Chalets (premium / estacional): es el ángulo que más engancha visualmente — agrupa los mejores hook rates de la cuenta (32-43%) y también el mejor hold rate (30,30%, versión chalet +5M€). El volumen es moderado (7-10 leads por anuncio) y el CPL premium es de los más altos (63,10€), coherente con un target de ticket alto: menos leads, pero previsiblemente más cualificados.")
bullet("Servicio y gestión sin esfuerzo (evitar improvisar, ahorrar tiempo): el formato entrevista (Servicio EVO) genera el CTR más alto de toda la cuenta (4,12%, el resto ronda 1%), pero el hook rate es el más bajo (14,17%) — el copy/miniatura interesa mucho antes del clic, pero el arranque del vídeo no retiene. El resto del ángulo (falta de tiempo) rinde de forma más discreta (CPL 44,36€).")

append("Anuncios con mejor Hook Rate", heading=True)
append("Los 3 anuncios con mejor hook rate de la tabla REFORMAS, para revisar el vídeo y valorar qué hace que funcionen:")
bullet("Chalet verano — 42,54%")
bullet("Subvenciones redes — 35,42%")
bullet("Chalet redes (+5M€) — 32,43%")
append("Notas:")
for _ in range(4):
    append("")

append("Otras conclusiones", heading=True)
bullet("Living tiene el CPL más bajo de toda la cuenta (19-20€) pero también el hook rate más bajo (9-14%) — capta leads baratos sin depender del enganche del vídeo, probablemente por un público ya predispuesto.")
bullet("Cocinas rinde de forma sólida y consistente (CPL 30-33€, hook 21-32%), sin outliers destacables.")
bullet("B2B tiene el segundo CTR más alto de la cuenta (2,27%) pero un CPL más alto que Living o Cocinas (37,45€) — el clic es fácil de conseguir, la conversión a lead cuesta más.")

print("Listo:", "https://docs.google.com/document/d/%s/edit" % DOC_ID)
