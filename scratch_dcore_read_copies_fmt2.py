# -*- coding: utf-8 -*-
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'

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
    fields="sheets(data(rowData(values(formattedValue,effectiveFormat.backgroundColor))))"
).execute()

rows = result['sheets'][0]['data'][0].get('rowData', [])
colors_seen = {}
for i, row in enumerate(rows, start=1):
    values = row.get('values', [])
    for j, cell in enumerate(values):
        bg = cell.get('effectiveFormat', {}).get('backgroundColor', {})
        r = round(bg.get('red', 1),2); g = round(bg.get('green', 1),2); b = round(bg.get('blue', 1),2)
        key = (r,g,b)
        if key != (1,1,1) and key != (0,0,0):
            colors_seen.setdefault(key, []).append((i,j))

for k,v in colors_seen.items():
    print(k, len(v), v[:10])
