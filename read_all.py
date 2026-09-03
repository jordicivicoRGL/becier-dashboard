# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
from tools.calendar_tools import get_google_credentials

creds = get_google_credentials()
service = build('sheets', 'v4', credentials=creds)

result = service.spreadsheets().values().get(
    spreadsheetId='1RHtUA5Jzu330SmL0OogU2rN7UIJ_qe3e1Wr_DO_9vs4',
    range='Copies!A2:C10'
).execute()

rows = result.get('values', [])
for i, row in enumerate(rows):
    print(f'=== FILA {i+2} | {row[0]} ===')
    print(f'TEXTO: {row[1] if len(row) > 1 else ""}')
    print(f'TITULO: {row[2] if len(row) > 2 else ""}')
    print()
