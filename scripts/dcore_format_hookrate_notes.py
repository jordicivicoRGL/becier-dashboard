# -*- coding: utf-8 -*-
"""Da formato a las notas de hook rate que Jordi escribió a mano en el Google Doc DCORE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1CYJyg4ca6xUM1raULMPhXQ2ZOx92DwJi2EFJ5VkM67g"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

ACCENT = {"red": 0xB5 / 255, "green": 0x50 / 255, "blue": 0x2F / 255}

# El borrado ya se ejecutó en una corrida anterior; el punto de inserción es 3316.
END = 3316


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


entries = [
    {
        "title": "Chalet verano — 42,54%",
        "hook": "“¡No puedo! ¡Con esta piscina aquí no se puede trabajar! ¿Te imaginas?” — afirmación directa enseñando la piscina, incitando al usuario a imaginarse la casa de ensueño: disfrutando con amigos, familia, en verano.",
        "adapt": "Que el usuario se imagine su piso/casa reformada a su gusto en una situación cotidiana “soñada”: disfrutando con amigos, trabajando en casa, en una oficina o salón de diseño…",
    },
    {
        "title": "Subvenciones redes — 35,42%",
        "hook": "“¿Sabías que puedes ahorrarte más de 15.000€ en tu reforma?” — pregunta + cantidad alta de ahorro. Es el hook perfecto para esta situación (subvenciones del estado): capta la atención de inmediato.",
        "adapt": "Aplicarlo a las formas que tiene Dcore de ahorrar frente a otras empresas: presupuesto cerrado desde el primer día (sin sobrecostes ocultos), un mismo equipo lleva el proyecto (evita sobrecostes de subcontratas)…",
    },
    {
        "title": "Chalet redes (+5M€) — 32,43%",
        "hook": "“Si tu chalet vale 2 millones de euros, no puedes reformarlo como un piso cualquiera.”",
        "adapt": "Parecido al chalet verano: mencionar una cantidad de dinero concreta en el hook retiene al usuario para ver qué hay después.",
    },
]

for i, entry in enumerate(entries):
    insert(entry["title"], bold=True, size=11, space_before=10 if i > 0 else 4)
    insert("Hook: " + entry["hook"], italic=True)
    insert("Cómo adaptarlo: " + entry["adapt"], space_after=6)

print("Listo:", "https://docs.google.com/document/d/%s/edit" % DOC_ID)
