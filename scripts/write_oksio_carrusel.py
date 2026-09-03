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

titol = "Troba el teu cotxe d'ocasió 🚗"

copy = (
    "Busques un cotxe d'ocasió però no saps quin s'adapta millor a tu? 🚗\n\n"
    "A OKSIÓ (Becier) tens un cotxe pensat per a cada necessitat: el Citroën C4 Spacetourer si busques espai per a tota la família, el Hyundai Tucson si vols un SUV complet, o el Seat Leon si prefereixes un compacte àgil pel dia a dia.\n\n"
    "Tria el teu i estrena'l amb tota la confiança d'una ocasió amb garantia.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

values = [["Juliol", "Vehicles", "", "OKSIÓ - Citroen C4 Spacetourer / Hyundai Tucson / Seat Leon"]]
result_meta = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!A98:D98",
    valueInputOption='RAW',
    body={'values': values}
).execute()

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!J98:K98",
    valueInputOption='RAW',
    body={'values': [[titol, copy]]}
).execute()

print(f"Celdas actualizadas metadata: {result_meta.get('updatedCells')}, copy: {result.get('updatedCells')}")
