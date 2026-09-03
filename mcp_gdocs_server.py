import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

mcp = FastMCP("Google Docs")


def get_docs_service():
    creds = get_google_credentials()
    return build("docs", "v1", credentials=creds)


@mcp.tool()
def gdocs_get(document_id: str) -> str:
    """Lee el contenido de un Google Doc y devuelve el texto plano con índices de posición."""
    service = get_docs_service()
    doc = service.documents().get(documentId=document_id).execute()
    lines = []
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            text = "".join(
                pe["textRun"]["content"]
                for pe in element["paragraph"].get("elements", [])
                if "textRun" in pe
            )
            lines.append(text)
        elif "table" in element:
            lines.append("[TABLA]")
    return "".join(lines)


@mcp.tool()
def gdocs_replace_text(document_id: str, old_text: str, new_text: str) -> str:
    """Reemplaza texto en un Google Doc (sensible a mayúsculas). Útil para corregir errores ortográficos."""
    service = get_docs_service()
    requests = [{
        "replaceAllText": {
            "containsText": {"text": old_text, "matchCase": True},
            "replaceText": new_text,
        }
    }]
    result = service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()
    n = result.get("replies", [{}])[0].get("replaceAllText", {}).get("occurrencesChanged", 0)
    return f"'{old_text}' → '{new_text}': {n} ocurrencia(s) reemplazada(s)."


@mcp.tool()
def gdocs_center_table_cells(document_id: str) -> str:
    """Centra horizontalmente el texto de todas las celdas de todas las tablas del documento."""
    service = get_docs_service()
    doc = service.documents().get(documentId=document_id).execute()

    requests = []

    def collect_requests(table):
        for row in table.get("tableRows", []):
            for cell in row.get("tableCells", []):
                for cell_element in cell.get("content", []):
                    if "paragraph" in cell_element:
                        start = cell_element.get("startIndex", 0)
                        end = cell_element.get("endIndex", 0)
                        if start < end:
                            requests.append({
                                "updateParagraphStyle": {
                                    "range": {"startIndex": start, "endIndex": end},
                                    "paragraphStyle": {"alignment": "CENTER"},
                                    "fields": "alignment",
                                }
                            })

    for element in doc.get("body", {}).get("content", []):
        if "table" in element:
            collect_requests(element["table"])

    if not requests:
        return "No se encontraron tablas en el documento."

    service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()
    return f"Texto centrado en {len(requests)} párrafo(s) de celdas de tabla."


@mcp.tool()
def gdocs_append_formatted(document_id: str, content: str, tab_id: str = "") -> str:
    """
    Inserta contenido formateado al final de un Google Doc o de una pestaña específica.
    Formato del contenido: líneas con '# ' = H1, '## ' = H2, '### ' = H3, resto = texto normal.
    Las líneas vacías y '---' se insertan como párrafos en blanco.
    tab_id: ID de la pestaña sin el prefijo 't.' (ej: 's1bg2uhcf7fd').
    """
    service = get_docs_service()

    # Leer el documento para encontrar el índice final de la pestaña
    get_kwargs = {"documentId": document_id}
    if tab_id:
        get_kwargs["includeTabsContent"] = True

    doc = service.documents().get(**get_kwargs).execute()

    # Determinar índice de inserción
    end_index = 1
    if tab_id:
        for tab in doc.get("tabs", []):
            if tab.get("tabProperties", {}).get("tabId") == tab_id:
                body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
                if body_content:
                    end_index = max(1, body_content[-1].get("endIndex", 2) - 1)
                break
    else:
        body_content = doc.get("body", {}).get("content", [])
        if body_content:
            end_index = max(1, body_content[-1].get("endIndex", 2) - 1)

    # Parsear el contenido en bloques (estilo, texto)
    blocks = []
    for line in content.split("\n"):
        line = line.rstrip()
        if line.startswith("### "):
            blocks.append(("HEADING_3", line[4:]))
        elif line.startswith("## "):
            blocks.append(("HEADING_2", line[3:]))
        elif line.startswith("# "):
            blocks.append(("HEADING_1", line[2:]))
        else:
            blocks.append(("NORMAL_TEXT", "" if line == "---" else line))

    if not blocks:
        return "No hay contenido para insertar."

    # Helpers para incluir tabId solo si aplica
    def loc(idx):
        obj = {"index": idx}
        if tab_id:
            obj["tabId"] = tab_id
        return obj

    def rng(start, end):
        obj = {"startIndex": start, "endIndex": end}
        if tab_id:
            obj["tabId"] = tab_id
        return obj

    def utf16_len(text):
        return sum(2 if ord(c) > 0xFFFF else 1 for c in text)

    # Construir requests de inserción y de estilo por separado
    insert_requests = []
    style_requests = []
    current_index = end_index

    for style, text in blocks:
        full_text = text + "\n"
        text_len = utf16_len(full_text)

        insert_requests.append({
            "insertText": {
                "location": loc(current_index),
                "text": full_text,
            }
        })

        if style != "NORMAL_TEXT" and text:
            style_requests.append({
                "updateParagraphStyle": {
                    "range": rng(current_index, current_index + text_len),
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            })

        current_index += text_len

    # Enviar todo en un solo batchUpdate (inserciones primero, estilos después)
    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": insert_requests + style_requests},
    ).execute()

    return (
        f"✓ Contenido insertado: {len(blocks)} bloques, "
        f"{current_index - end_index} caracteres añadidos."
    )


if __name__ == "__main__":
    mcp.run()
