# -*- coding: utf-8 -*-
"""Reemplaza la sección de análisis del Google Doc (conversión del Word) por el análisis de ángulos."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1CYJyg4ca6xUM1raULMPhXQ2ZOx92DwJi2EFJ5VkM67g"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

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
    if "Análisis" in text and "REFORMAS" in text:
        start_idx = s
    if "pese a enganchar peor en el arranque" in text:
        end_idx = e
        break

assert start_idx is not None, "No se encontró el inicio del análisis"
assert end_idx is not None, "No se encontró el final del análisis"

ACCENT = {"red": 0xB5 / 255, "green": 0x50 / 255, "blue": 0x2F / 255}

# --- 1. Borrar el bloque antiguo ---
docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
    {"deleteContentRange": {"range": {"startIndex": start_idx, "endIndex": end_idx}}}
]}).execute()

# --- 2. Insertar el nuevo bloque ---
END = start_idx


def append(text, heading=False, bullet=False):
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
append("Agrupando los anuncios por el ángulo o mensaje que usan (más allá del vídeo concreto), esto es lo que mejor funciona:")
bullet("Ahorro y subvenciones (beneficio económico concreto): ángulo con el mejor equilibrio de la cuenta — CPL más bajo con volumen real (24,48€ / 42 leads) y el segundo mejor hook rate (35,42%). Decir un ahorro concreto en euros, dicho en la calle, es el mensaje más rentable de todos.")
bullet("Presupuesto detallado / transparencia (racional): es el ángulo que más volumen aporta con diferencia — 111 leads combinados entre sus dos anuncios, con un CPL medio de ~30,7€. El hook rate es de los más bajos (17-19%), así que el enganche inicial es débil, pero el argumento racional convence a quien se queda a verlo. La ejecución importa mucho dentro del mismo ángulo: el CPL varía de 29,59€ a 53,80€ entre sus dos versiones.")
bullet("Chalets (premium / estacional): es el ángulo que más engancha visualmente — agrupa los mejores hook rates de la cuenta (32-43%) y también el mejor hold rate (30,30%, versión chalet +5M€). A cambio el volumen es bajo (0-10 leads por anuncio) y el CPL premium es de los más altos (63,10€), coherente con un target de ticket alto: menos leads, pero previsiblemente más cualificados.")
bullet("Servicio y gestión sin esfuerzo (evitar improvisar, ahorrar tiempo): el formato entrevista (Servicio EVO) genera el CTR más alto de toda la cuenta (4,12%, el resto ronda 1%), pero el hook rate es el más bajo (14,17%) — el copy/miniatura interesa mucho antes del clic, pero el arranque del vídeo no retiene. El resto del ángulo (falta de tiempo) rinde de forma más discreta (CPL 44,36€).")
bullet("Urgencia sin beneficio racional: es el ángulo más caro que sí convierte (CPL 82,76€, solo 2 leads) — engancha razonablemente (hook 31,52%) pero no cierra. Mejor combinarlo siempre con un beneficio racional (ahorro, transparencia, tranquilidad) que usarlo solo.")

append("Anuncios con mejor Hook Rate", heading=True)
append("Los 3 anuncios con mejor hook rate de la tabla REFORMAS, para revisar el vídeo y valorar qué hace que funcionen:")
bullet("Chalet verano — 42,54%")
bullet("Subvenciones redes — 35,42%")
bullet("Chalet redes (+5M€) — 32,43%")
append("Notas:")
for _ in range(4):
    append("")

append("Otras conclusiones", heading=True)
bullet("Grabar en la calle tiende a dar mejor hook rate que grabar en la oficina; el único caso que rompe el patrón es el formato entrevista (EVO), que gana en CTR pero no en hook rate.")
bullet("Living tiene el CPL más bajo de toda la cuenta (19-20€) pero también el hook rate más bajo (9-14%) — capta leads baratos sin depender del enganche del vídeo, probablemente por un público ya predispuesto.")
bullet("Cocinas rinde de forma sólida y consistente (CPL 30-33€, hook 21-32%), sin outliers destacables.")
bullet("B2B tiene el segundo CTR más alto de la cuenta (2,27%) pero un CPL más alto que Living o Cocinas (37,45€) — el clic es fácil de conseguir, la conversión a lead cuesta más.")
bullet("El vídeo de chalet en 4x5 (177,94€ gastados, 0 leads) tiene buen hook/hold rate — vigilar si el formato 4x5 rinde peor que el 9:16 para el ángulo chalet, o si simplemente falta volumen todavía.")

print("Listo:", "https://docs.google.com/document/d/%s/edit" % DOC_ID)
