# -*- coding: utf-8 -*-
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
GID = 1096631747

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
meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
for s in meta['sheets']:
    props = s['properties']
    print(props['sheetId'], props['title'])
