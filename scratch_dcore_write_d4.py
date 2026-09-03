# -*- coding: utf-8 -*-
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k"
TAB = "Copies"


def get_service():
    token_path = os.path.join(os.path.dirname(__file__), "credentials", "token.json")
    secret_path = os.path.join(os.path.dirname(__file__), "credentials", "client_secret.json")
    with open(token_path) as f:
        token_data = json.load(f)
    with open(secret_path) as f:
        secret_data = json.load(f)
    web_or_installed = secret_data.get("web") or secret_data.get("installed")
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web_or_installed["client_id"],
        client_secret=web_or_installed["client_secret"],
        scopes=token_data.get("scopes"),
    )
    creds.refresh(Request())
    return build("sheets", "v4", credentials=creds)


CTA_B = 'Haz clic en "Cotizar", cuéntanos tu proyecto en el formulario y te llamamos.'

texto_d4 = "\n\n".join([
    "En DCORE diseñamos, decidimos materiales y cerramos la distribución antes "
    "de que empiece la obra, así no rehacemos nada ni improvisamos nada.",
    "Arquitecto, interiorista y jefe de obra trabajan coordinados por un project "
    "manager que lleva tu proyecto de principio a fin, sin que tengas que hacer "
    "de intermediario entre nadie.",
    "Reformas integrales de chalets en Madrid, con presupuesto fijo y un único "
    "equipo.",
    CTA_B,
])

service = get_service()
result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{TAB}'!D4",
    valueInputOption="USER_ENTERED",
    body={"values": [[texto_d4]]},
).execute()
print(json.dumps(result, indent=2, ensure_ascii=False))
