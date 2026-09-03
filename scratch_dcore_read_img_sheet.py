# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'

img = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range="'IMG'!A1:L45"
).execute().get('values', [])
print("=== IMG (todas las filas) ===")
for i, row in enumerate(img, start=1):
    print(f"{i}: {row}")

vid = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range="'VID'!A1:N30"
).execute().get('values', [])
print("\n=== VID (filas 1-30) ===")
for i, row in enumerate(vid, start=1):
    print(f"{i}: {row}")
