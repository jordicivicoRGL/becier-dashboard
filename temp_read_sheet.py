# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1RHtUA5Jzu330SmL0OogU2rN7UIJ_qe3e1Wr_DO_9vs4'

# Listar pestañas disponibles
spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
for sheet in spreadsheet['sheets']:
    props = sheet['properties']
    print(f"Pestaña: '{props['title']}' | gid: {props['sheetId']}")

# Leer la pestaña con gid=337648136
# Primero encontrar su nombre
target_gid = 337648136
target_name = None
for sheet in spreadsheet['sheets']:
    if sheet['properties']['sheetId'] == target_gid:
        target_name = sheet['properties']['title']
        break

print(f"\nPestaña objetivo: '{target_name}'")

result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"'{target_name}'!A1:Z50"
).execute()

rows = result.get('values', [])
print(f"Total filas leídas: {len(rows)}")
for i, row in enumerate(rows, start=1):
    print(f"Fila {i}: {row}")
