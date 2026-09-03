# -*- coding: utf-8 -*-
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k"


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


service = get_service()
meta = service.spreadsheets().get(
    spreadsheetId=SHEET_ID,
    ranges=["'Copies'!A1:H8"],
    includeGridData=True,
).execute()
sheet = meta["sheets"][0]
grid = sheet["data"][0]
rowmeta = grid.get("rowMetadata", [])
colmeta = grid.get("columnMetadata", [])
print("rowMetadata heights:", [r.get("pixelSize") for r in rowmeta])
print("colMetadata widths:", [c.get("pixelSize") for c in colmeta])

for ridx, row in enumerate(grid.get("rowData", []), start=1):
    values = row.get("values", [])
    for cidx, cell in enumerate(values, start=1):
        note = cell.get("note")
        val = cell.get("formattedValue")
        wrap = cell.get("userEnteredFormat", {}).get("wrapStrategy")
        if note or val or wrap:
            print(f"row{ridx} col{cidx}: val={val!r} note={note!r} wrap={wrap!r}")
