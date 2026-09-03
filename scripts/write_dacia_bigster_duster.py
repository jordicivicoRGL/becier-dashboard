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

titol = "Bigster i Duster — Dies Únics Dacia 🚙"

copy_a = (
    "Els Dies Únics Dacia s'allarguen, però no per sempre. 🚙\n\n"
    "Si buscaves un SUV Dacia —gran i espaiós amb el Bigster, o robust i tot terreny amb el Duster— ara tens una mica més de temps per aprofitar les condicions especials a Becier.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

copy_b = (
    "Un SUV gran o un tot terreny robust: tu tries, Dacia t'ho posa fàcil. 🚙\n\n"
    "El Bigster porta espai i equipament per a tota la família; el Duster, la robustesa que mai falla a les carreteres d'Andorra. Els dos, amb els Dies Únics Dacia allargats a Becier.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

copy_c = (
    "S'allarguen els Dies Únics Dacia: Bigster i Duster, encara amb condicions especials. 🚙\n\n"
    "A Becier t'ho expliquem tot sense compromís.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."
)

meta = [["Juliol", "Vehicles", "", "Dacia Bigster / Dacia Duster (Dies Únics Dacia)"]]
result_meta = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!A100:D100",
    valueInputOption='RAW',
    body={'values': meta}
).execute()

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!J100:M100",
    valueInputOption='RAW',
    body={'values': [[titol, copy_a, copy_b, copy_c]]}
).execute()

print(f"Celdas actualizadas metadata: {result_meta.get('updatedCells')}, copy: {result.get('updatedCells')}")
