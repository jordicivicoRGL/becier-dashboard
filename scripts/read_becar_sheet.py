# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE'

spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
target_gid = 1561536142
target_name = None
for sheet in spreadsheet['sheets']:
    props = sheet['properties']
    print(f"Pestaña: '{props['title']}' | gid: {props['sheetId']}")
    if props['sheetId'] == target_gid:
        target_name = props['title']

print(f"\nPestaña objetivo: '{target_name}'")

# Cabeceras
header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"'{target_name}'!1:1"
).execute()
headers = header_result.get('values', [[]])[0]
print(f"\nCabeceras: {headers}")

# Filas 88-97 para ver contexto alrededor de 93-96
rows_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"'{target_name}'!A88:Z97"
).execute()
rows = rows_result.get('values', [])
for i, row in enumerate(rows, start=88):
    print(f"Fila {i}: {row}")
