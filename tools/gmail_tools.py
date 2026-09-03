import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from tools.calendar_tools import get_google_credentials, _service_cache


def get_gmail_service():
    if "gmail" not in _service_cache:
        creds = get_google_credentials()
        _service_cache["gmail"] = build("gmail", "v1", credentials=creds)
    return _service_cache["gmail"]


def search_emails(query: str, max_results: int = 10) -> dict:
    try:
        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            return {"emails": [], "message": f"No se encontraron emails con la búsqueda: '{query}'"}

        emails = []
        for msg_ref in messages:
            msg = service.users().messages().get(
                userId="me",
                id=msg_ref["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"]
            ).execute()

            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            snippet = msg.get("snippet", "")

            emails.append({
                "id": msg_ref["id"],
                "from": headers.get("From", ""),
                "to": headers.get("To", ""),
                "subject": headers.get("Subject", "Sin asunto"),
                "date": headers.get("Date", ""),
                "snippet": snippet
            })

        return {"emails": emails, "total": len(emails)}

    except Exception as e:
        return {"error": str(e)}


def send_email(to: str, subject: str, body: str) -> dict:
    try:
        service = get_gmail_service()

        message = MIMEMultipart("alternative")
        message["To"] = to
        message["Subject"] = subject

        if "<" in body and ">" in body:
            part = MIMEText(body, "html")
        else:
            part = MIMEText(body, "plain")

        message.attach(part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()

        return {
            "success": True,
            "message_id": sent["id"],
            "to": to,
            "subject": subject,
            "message": f"Email enviado correctamente a {to}."
        }

    except Exception as e:
        return {"error": str(e)}
