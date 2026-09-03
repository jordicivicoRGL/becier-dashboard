# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
SHEET_TAB = 'VID'

result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_TAB}'!A1:Z100"
).execute()

rows = result.get('values', [])
print(f"Total filas leídas: {len(rows)}")
for i, row in enumerate(rows, start=1):
    print(f"Fila {i}: {row}")
