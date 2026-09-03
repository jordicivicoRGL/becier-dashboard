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

copy_v2 = (
    "Cada cotxe té la seva història, i el teu proper cotxe pot començar avui. 🚗\n\n"
    "A OKSIÓ (Becier) trobaràs des d'un monovolum pensat per a la família —el Citroën C4 Spacetourer— fins a un SUV versàtil —el Hyundai Tucson— o un compacte àgil pel dia a dia —el Seat Leon.\n\n"
    "Cadascun amb la confiança d'una ocasió amb garantia, a punt per començar amb tu.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

copy_v3 = (
    "3 cotxes, 3 estils diferents: monovolum, SUV i compacte. 🚗\n\n"
    "A OKSIÓ (Becier) tens el Citroën C4 Spacetourer, el Hyundai Tucson i el Seat Leon, tots d'ocasió i amb garantia. Tria el que millor s'adapta al que necessites.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!L98:M98",
    valueInputOption='RAW',
    body={'values': [[copy_v2, copy_v3]]}
).execute()

print(f"Celdas actualizadas: {result.get('updatedCells')}")
