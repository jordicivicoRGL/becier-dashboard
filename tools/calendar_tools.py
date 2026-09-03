import os
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/adwords",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/analytics.edit",
    "https://www.googleapis.com/auth/drive.readonly",
]

CREDENTIALS_DIR = Path(__file__).parent.parent / "credentials"
CLIENT_SECRET_PATH = CREDENTIALS_DIR / "client_secret.json"
TOKEN_PATH = CREDENTIALS_DIR / "token.json"
MADRID_TZ = ZoneInfo("Europe/Madrid")

_service_cache = {}


def get_google_credentials() -> Credentials:
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_PATH.exists():
                raise FileNotFoundError(
                    f"No se encontró el archivo de credenciales de Google en {CLIENT_SECRET_PATH}. "
                    "Descárgalo desde Google Cloud Console y ponlo en la carpeta 'credentials'."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return creds


def get_calendar_service():
    if "calendar" not in _service_cache:
        creds = get_google_credentials()
        _service_cache["calendar"] = build("calendar", "v3", credentials=creds)
    return _service_cache["calendar"]


def get_events(days_ahead: int = 7) -> dict:
    try:
        service = get_calendar_service()
        now = datetime.now(MADRID_TZ)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=days_ahead)).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return {"events": [], "message": f"No hay eventos en los próximos {days_ahead} días."}

        formatted_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            formatted_events.append({
                "id": event["id"],
                "title": event.get("summary", "Sin título"),
                "start": start,
                "end": end,
                "description": event.get("description", ""),
                "location": event.get("location", "")
            })

        return {"events": formatted_events, "total": len(formatted_events)}

    except Exception as e:
        return {"error": str(e)}


def create_event(title: str, start_datetime: str, end_datetime: str,
                 description: str = "", location: str = "") -> dict:
    try:
        service = get_calendar_service()

        event_body = {
            "summary": title,
            "start": {
                "dateTime": start_datetime,
                "timeZone": "Europe/Madrid"
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "Europe/Madrid"
            }
        }

        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location

        created = service.events().insert(calendarId="primary", body=event_body).execute()

        return {
            "success": True,
            "event_id": created["id"],
            "title": title,
            "start": start_datetime,
            "end": end_datetime,
            "link": created.get("htmlLink", "")
        }

    except Exception as e:
        return {"error": str(e)}


def update_event(event_id: str, title: str = None, start_datetime: str = None,
                 end_datetime: str = None, description: str = None, location: str = None) -> dict:
    try:
        service = get_calendar_service()
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        if title is not None:
            event["summary"] = title
        if start_datetime is not None:
            event["start"] = {"dateTime": start_datetime, "timeZone": "Europe/Madrid"}
        if end_datetime is not None:
            event["end"] = {"dateTime": end_datetime, "timeZone": "Europe/Madrid"}
        if description is not None:
            event["description"] = description
        if location is not None:
            event["location"] = location

        updated = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()

        return {
            "success": True,
            "event_id": event_id,
            "title": updated.get("summary", ""),
            "start": updated["start"].get("dateTime", updated["start"].get("date")),
            "end": updated["end"].get("dateTime", updated["end"].get("date"))
        }

    except Exception as e:
        return {"error": str(e)}


def delete_event(event_id: str) -> dict:
    try:
        service = get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return {"success": True, "event_id": event_id, "message": "Evento eliminado correctamente."}
    except Exception as e:
        return {"error": str(e)}
