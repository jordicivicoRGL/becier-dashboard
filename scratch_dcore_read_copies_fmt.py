# -*- coding: utf-8 -*-
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
TAB_GID = 1096631747

def get_service():
    with open('credentials/token.json') as f:
        token_data = json.load(f)
    with open('credentials/client_secret.json') as f:
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

result = service.spreadsheets().get(
    spreadsheetId=SHEET_ID,
    ranges=["'Copies'!A1:Z200"],
    fields="sheets(data(rowData(values(formattedValue,userEnteredFormat.backgroundColor))))"
).execute()

rows = result['sheets'][0]['data'][0].get('rowData', [])
for i, row in enumerate(rows, start=1):
    values = row.get('values', [])
    for j, cell in enumerate(values):
        bg = cell.get('userEnteredFormat', {}).get('backgroundColor', {})
        r = bg.get('red', 1); g = bg.get('green', 1); b = bg.get('blue', 1)
        # detect orange-ish: high red, mid green, low blue
        if r > 0.85 and 0.4 < g < 0.85 and b < 0.5:
            val = cell.get('formattedValue', '')
            col_letter = chr(65+j) if j < 26 else 'A'+chr(65+j-26)
            print(f"Fila {i} Col {col_letter}: RGB({r:.2f},{g:.2f},{b:.2f}) -> {val[:80]}")
