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

titol = "3 ocasions, 3 mons diferents 🏁"

copy_a = (
    "Pagar preu de nou per un cotxe que ja no ho és, no té sentit. 🏁\n\n"
    "A Becier Oksió trobes ocasions certificades —un SUV potent, un clàssic descapotable, un esportiu pur— per molt menys del que et costaria estrenar-los. La mateixa exclusivitat, sense pagar l'etiqueta de nou.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

copy_b = (
    "La potència d'un BMW X3 M50, l'ànima artesanal d'un Morgan Plus4 o l'adrenalina d'un Porsche Boxster 718 GTS. 🏁\n\n"
    "A Becier Oksió no triem cotxes a l'atzar: seleccionem ocasions certificades que mereixen ser conduïdes, no guardades.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

copy_c = (
    "BMW X3 M50, Morgan Plus4, Porsche Boxster 718 GTS: 3 icones, 3 estils, un sol lloc. 🏁\n\n"
    "Selecció premium d'ocasió a Becier Oksió, certificada i llesta per estrenar-la tu.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

meta = [["Juliol", "Vehicles", "", "OKSIÓ - BMW X3 M50 / Morgan Plus4 / Porsche Boxster 718 GTS"]]
result_meta = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!A99:D99",
    valueInputOption='RAW',
    body={'values': meta}
).execute()

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!J99:M99",
    valueInputOption='RAW',
    body={'values': [[titol, copy_a, copy_b, copy_c]]}
).execute()

print(f"Celdas actualizadas metadata: {result_meta.get('updatedCells')}, copy: {result.get('updatedCells')}")
