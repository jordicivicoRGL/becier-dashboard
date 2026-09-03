"""
Rellena las celdas de la tabla 'Resumen del tratamiento' en PRE-TEXTOS Diagonal CQ,
pone en negrita la fila de cabecera y colorea en azul los placeholders [añadir imagen:...].
"""
import sys
sys.path.insert(0, r"c:\Users\PC\Desktop\Curso Claude Code VSCode\claudito")

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1mbkD6hmmUm944_653ptryd9MGR4dgqZZWovMTC6wiRs"
TAB_ID = "t.0"

ROWS = [
    ('Liposucción abdomen y flancos', 'Detalles'),
    ('Tipo de intervención', 'Cirugía estética de contorno corporal'),
    ('Anestesia', 'General o sedación profunda'),
    ('Duración de la cirugía', '1-3 horas'),
    ('Recuperación laboral', '7-14 días'),
    ('Faja de compresión', '4-6 semanas'),
    ('Primeros resultados visibles', '4-8 semanas'),
    ('Resultado definitivo', '4-6 meses'),
    ('Cicatrices', 'Mínimas (milímetros), en zonas poco visibles'),
]


def get_service():
    creds = get_google_credentials()
    return build("docs", "v1", credentials=creds)


def get_doc(service):
    return service.documents().get(
        documentId=DOC_ID,
        includeTabsContent=True
    ).execute()


def find_table_cells(doc):
    """Recorre el contenido del tab t.0 y devuelve las celdas de la primera tabla."""
    tabs = doc.get("tabs", [])
    tab = next((t for t in tabs if t.get("tabProperties", {}).get("tabId") == TAB_ID), None)
    if not tab:
        raise RuntimeError(f"Tab {TAB_ID} no encontrado")

    content = tab.get("documentTab", {}).get("body", {}).get("content", [])

    for element in content:
        if "table" not in element:
            continue
        table = element["table"]
        cells = []
        for row in table.get("tableRows", []):
            row_cells = []
            for cell in row.get("tableCells", []):
                start = cell["startIndex"]
                row_cells.append(start + 1)  # +1 para insertar dentro
            cells.append(row_cells)
        return cells

    raise RuntimeError("No se encontró ninguna tabla en el tab")


def find_image_placeholder_ranges(doc):
    """Devuelve lista de (startIndex, endIndex) de texto '[añadir imagen:...'."""
    tabs = doc.get("tabs", [])
    tab = next((t for t in tabs if t.get("tabProperties", {}).get("tabId") == TAB_ID), None)
    if not tab:
        return []

    content = tab.get("documentTab", {}).get("body", {}).get("content", [])
    ranges = []

    def scan_elements(elements):
        for el in elements:
            if "paragraph" in el:
                for run in el["paragraph"].get("elements", []):
                    tr = run.get("textRun")
                    if tr and "[añadir imagen" in tr.get("content", "").lower():
                        ranges.append({
                            "startIndex": run["startIndex"],
                            "endIndex": run["endIndex"],
                        })
            elif "table" in el:
                for row in el["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        scan_elements(cell.get("content", []))

    scan_elements(content)
    return ranges


def main():
    service = get_service()

    # 1. Obtener estado actual del doc
    print("Obteniendo documento...")
    doc = get_doc(service)

    # 2. Encontrar celdas de la tabla
    print("Buscando tabla...")
    cells = find_table_cells(doc)
    print(f"Tabla encontrada: {len(cells)} filas x {len(cells[0])} columnas")
    for i, row in enumerate(cells):
        print(f"  fila {i}: {row}")

    if len(cells) != len(ROWS):
        print(f"ADVERTENCIA: la tabla tiene {len(cells)} filas pero ROWS tiene {len(ROWS)}")

    # 3. Insertar contenido en orden inverso para no desplazar índices
    insert_requests = []
    for row_i in range(len(ROWS) - 1, -1, -1):
        for col_j in range(len(cells[row_i]) - 1, -1, -1):
            text = ROWS[row_i][col_j]
            idx = cells[row_i][col_j]
            insert_requests.append({
                "insertText": {
                    "location": {"index": idx, "tabId": TAB_ID},
                    "text": text,
                }
            })

    print(f"\nInsertando {len(insert_requests)} textos en celdas...")
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": insert_requests}
    ).execute()
    print("Textos insertados.")

    # 4. Volver a obtener el doc para encontrar los rangos actualizados
    print("\nActualizando estado del doc para negrita y colores...")
    doc = get_doc(service)
    cells2 = find_table_cells(doc)

    # Negrita en fila de cabecera (fila 0)
    bold_requests = []
    for col_j in range(len(cells2[0])):
        cell_start = cells2[0][col_j]
        # El texto tiene len(ROWS[0][col_j]) caracteres; el endIndex es start + len
        text_len = len(ROWS[0][col_j])
        bold_requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": cell_start,
                    "endIndex": cell_start + text_len,
                    "tabId": TAB_ID,
                },
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        })

    print(f"Aplicando negrita a {len(bold_requests)} celdas de cabecera...")
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": bold_requests}
    ).execute()
    print("Negrita aplicada.")

    # 5. Colorear placeholders de imagen en azul
    print("\nBuscando placeholders [añadir imagen:...]...")
    img_ranges = find_image_placeholder_ranges(doc)
    print(f"Encontrados {len(img_ranges)} placeholders")

    if img_ranges:
        blue_requests = []
        for r in img_ranges:
            blue_requests.append({
                "updateTextStyle": {
                    "range": {
                        "startIndex": r["startIndex"],
                        "endIndex": r["endIndex"],
                        "tabId": TAB_ID,
                    },
                    "textStyle": {
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.07,
                                    "green": 0.47,
                                    "blue": 0.87,
                                }
                            }
                        }
                    },
                    "fields": "foregroundColor",
                }
            })
        print(f"Coloreando {len(blue_requests)} ranges en azul...")
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": blue_requests}
        ).execute()
        print("Color azul aplicado.")
    else:
        print("No se encontraron placeholders de imagen en el texto.")

    print("\n✓ Todo completado.")


if __name__ == "__main__":
    main()
