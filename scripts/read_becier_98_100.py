# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE'
SHEET_NAME = 'Copies Ads'

rows_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!A97:M102"
).execute()
rows = rows_result.get('values', [])
for i, row in enumerate(rows, start=97):
    print(f"Fila {i}: {row}")
