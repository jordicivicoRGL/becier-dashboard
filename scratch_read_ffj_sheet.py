# -*- coding: utf-8 -*-
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "1AgwIcMquUefw9FtDM7IDf2Ttdh4lXvnnGtPNV0xJMvg"


def get_service():
    token_path = os.path.join("credentials", "token.json")
    secret_path = os.path.join("credentials", "client_secret.json")

    with open(token_path) as f:
        token_data = json.load(f)
    with open(secret_path) as f:
        secret_data = json.load(f)

    web_or_installed = secret_data.get("web") or secret_data.get("installed")

    credentials = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web_or_installed["client_id"],
        client_secret=web_or_installed["client_secret"],
        scopes=token_data.get("scopes"),
    )
    credentials.refresh(Request())
    return build("sheets", "v4", credentials=credentials)


service = get_service()
meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
print("TITULO:", meta["properties"]["title"])
print("PESTAÑAS:")
for s in meta["sheets"]:
    p = s["properties"]
    print(f"  - {p['title']} (gid={p['sheetId']}, filas={p['gridProperties'].get('rowCount')}, cols={p['gridProperties'].get('columnCount')})")
