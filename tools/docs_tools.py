from googleapiclient.discovery import build
from .calendar_tools import get_google_credentials


def get_docs_service():
    creds = get_google_credentials()
    return build("docs", "v1", credentials=creds)


def edit_google_doc(document_id: str, replacements: list) -> dict:
    """
    Aplica reemplazos de texto en un Google Doc.
    replacements: lista de {"find": str, "replace": str}
    """
    service = get_docs_service()

    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": r["find"], "matchCase": True},
                "replaceText": r["replace"],
            }
        }
        for r in replacements
    ]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()

    total = sum(
        r.get("replaceAllText", {}).get("occurrencesChanged", 0)
        for r in result.get("replies", [])
    )

    return {"occurrences_changed": total, "document_id": document_id}


def create_doc_tab(document_id: str, tab_title: str, content: str) -> dict:
    """Crea una nueva pestaña en un Google Doc e inserta contenido de texto."""
    service = get_docs_service()

    create_resp = service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": [{"createTab": {"tabProperties": {"title": tab_title}}}]}
    ).execute()

    tab_id = create_resp["replies"][0]["createTab"]["tabProperties"]["tabId"]

    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": [{"insertText": {"location": {"index": 1, "tabId": tab_id}, "text": content}}]}
    ).execute()

    return {"tab_id": tab_id, "tab_title": tab_title, "success": True}
