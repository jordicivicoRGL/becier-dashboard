# -*- coding: utf-8 -*-
"""Aplica estilo (cabecera oscura, filas crema, CPL en color) a las tablas del doc DCORE ya rellenado."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "10nsEVlzCNNbIuLsGiz4pN3OkVDGIqWYUUuhglZ0I9I8"

creds = get_google_credentials()
docs = build("docs", "v1", credentials=creds)

doc = docs.documents().get(documentId=DOC_ID).execute()

tables = []
for el in doc["body"]["content"]:
    if "table" in el:
        tables.append(el)

print("Tablas encontradas:", len(tables))

DARK = {"color": {"rgbColor": {"red": 0x22 / 255, "green": 0x1D / 255, "blue": 0x16 / 255}}}
CREAM = {"color": {"rgbColor": {"red": 0xFB / 255, "green": 0xF7 / 255, "blue": 0xF0 / 255}}}
WHITE = {"color": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}}
ACCENT = {"color": {"rgbColor": {"red": 0xB5 / 255, "green": 0x50 / 255, "blue": 0x2F / 255}}}

requests = []

for t_el in tables:
    table_start = t_el["startIndex"]
    n_rows = len(t_el["table"]["tableRows"])
    n_cols = len(t_el["table"]["tableRows"][0]["tableCells"])

    # Cabecera: fondo oscuro
    requests.append({
        "updateTableCellStyle": {
            "tableRange": {
                "tableCellLocation": {"tableStartLocation": {"index": table_start}, "rowIndex": 0, "columnIndex": 0},
                "rowSpan": 1,
                "columnSpan": n_cols,
            },
            "tableCellStyle": {"backgroundColor": DARK},
            "fields": "backgroundColor",
        }
    })

    # Filas de datos: fondo crema
    if n_rows > 1:
        requests.append({
            "updateTableCellStyle": {
                "tableRange": {
                    "tableCellLocation": {"tableStartLocation": {"index": table_start}, "rowIndex": 1, "columnIndex": 0},
                    "rowSpan": n_rows - 1,
                    "columnSpan": n_cols,
                },
                "tableCellStyle": {"backgroundColor": CREAM},
                "fields": "backgroundColor",
            }
        })

    # Texto de cabecera en blanco (negrita ya aplicada al insertar)
    header_row = t_el["table"]["tableRows"][0]
    for cell in header_row["tableCells"]:
        for content_el in cell["content"]:
            if "paragraph" not in content_el:
                continue
            for run in content_el["paragraph"].get("elements", []):
                if "textRun" in run:
                    requests.append({
                        "updateTextStyle": {
                            "range": {"startIndex": run["startIndex"], "endIndex": run["endIndex"]},
                            "textStyle": {"foregroundColor": WHITE},
                            "fields": "foregroundColor",
                        }
                    })

    # CPL (columna índice 4) en negrita + color acento, en filas de datos
    for r_idx in range(1, n_rows):
        row = t_el["table"]["tableRows"][r_idx]
        if len(row["tableCells"]) <= 4:
            continue
        cpl_cell = row["tableCells"][4]
        for content_el in cpl_cell["content"]:
            if "paragraph" not in content_el:
                continue
            for run in content_el["paragraph"].get("elements", []):
                if "textRun" in run:
                    requests.append({
                        "updateTextStyle": {
                            "range": {"startIndex": run["startIndex"], "endIndex": run["endIndex"]},
                            "textStyle": {"bold": True, "foregroundColor": ACCENT},
                            "fields": "bold,foregroundColor",
                        }
                    })

if requests:
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

print("Estilo aplicado:", len(requests), "requests")
