# -*- coding: utf-8 -*-
"""Añade el análisis de ángulos para Living, Cocinas y B2B en el Google Doc DCORE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1CYJyg4ca6xUM1raULMPhXQ2ZOx92DwJi2EFJ5VkM67g"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

ACCENT = {"red": 0xB5 / 255, "green": 0x50 / 255, "blue": 0x2F / 255}

INSERT_AT = 6504  # justo después de la tabla Living/Cocinas/B2B, antes del pie de página

END = INSERT_AT


def insert(text, bold=False, italic=False, size=9.5, space_after=2, space_before=0):
    global END
    full = text + "\n"
    s = END
    e = s + len(full)
    requests = [{"insertText": {"location": {"index": s}, "text": full}}]
    text_style = {"fontSize": {"magnitude": size, "unit": "PT"}, "bold": bold, "italic": italic}
    fields = "fontSize,bold,italic"
    if bold:
        text_style["foregroundColor"] = {"color": {"rgbColor": ACCENT}}
        fields += ",foregroundColor"
    requests.append({
        "updateTextStyle": {
            "range": {"startIndex": s, "endIndex": e},
            "textStyle": text_style,
            "fields": fields,
        }
    })
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": s, "endIndex": e},
            "paragraphStyle": {"spaceBelow": {"magnitude": space_after, "unit": "PT"}, "spaceAbove": {"magnitude": space_before, "unit": "PT"}},
            "fields": "spaceBelow,spaceAbove",
        }
    })
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    END = e


def heading(text):
    insert(text, bold=True, size=13, space_before=12, space_after=12)


def bullet(text):
    insert("•  " + text)


heading("Análisis de ángulos — Living, Cocinas y B2B")
insert("Agrupando por ángulo o mensaje, esto es lo que mejor funciona en este bloque:")

bullet("Diagnóstico / riesgo oculto (Living Check): las dos versiones alertan de que comprar sin un diagnóstico previo puede salir caro (\"algo no cuadra\", \"el mayor error no es el precio, es no saber lo que compras\"). Es el ángulo con el CPL más bajo de toda la cuenta (19,11-19,86€, 24-25 leads cada uno), pero también el hook rate más bajo (9,36-14,25%) — el público que ve el anuncio probablemente ya está buscando comprar piso, así que convierte barato sin depender de enganchar con el vídeo. La ejecución sí importa: mismo ángulo, pero el hook cae a la mitad en la versión rodada en la obra frente a la de calle.")
bullet("Regalo / incentivo directo (cocina de regalo): mensaje simple de incentivo económico (\"reforma hoy y la cocina de regalo\"). Buen equilibrio: hook decente (25,23%) y el hold rate más alto del bloque (29,35%), con CPL medio (30,37€) y el volumen más alto de Cocinas (22 leads).")
bullet("Servicio integral / evitar la complejidad de coordinar (Campaña Cocinas): mensaje racional sobre no tener que coordinar tú mismo arquitecto, obra y proveedores (\"en Dcore lo tienes todo en uno\"). Es el anuncio con mejor hook rate de todo el bloque (31,85%) y buen hold (29,42%), aunque con menos volumen (10 leads) y el CPL más alto de Cocinas (33,25€) — engancha muy bien, pero le falta más inversión para confirmar si escala.")
bullet("Evitar errores / listicle de riesgos (B2B, \"las 3 reformas que pueden arruinar tu local\"): genera el CTR más alto del bloque (2,27%) — el formato lista despierta mucha curiosidad y clics — pero el hook rate es de los más bajos (15,62%), señal de que el titular atrae más que el propio arranque del vídeo. Es también el CPL más alto del bloque (37,45€): el clic es fácil de conseguir, la conversión a lead cuesta más.")

print("Listo:", "https://docs.google.com/document/d/%s/edit" % DOC_ID)
