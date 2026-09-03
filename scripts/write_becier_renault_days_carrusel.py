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

cotxe = ('Rafale Atelier E-Tech 4x4 / Twingo E-Tech Evolution / Scenic ZE Evolution / '
         'Renault 5 Evolution 95cv / Megane ZE Techno / Renault 4 E-Tech Evolution '
         '(Renault Days ampliats)')

titol = 'Renault Days ampliats 🚗'

copy_a = (
    "Encara no has decidit quin Renault vols? 🤔\n\n"
    "Els Renault Days s'allarguen a Becier, amb 6 models diferents per triar: des de la ciutat fins al SUV familiar.\n\n"
    "Fes un cop d'ull al carrussel i troba el que millor s'adapta a tu.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu sense IGI."
)

copy_b = (
    "T'imagines estrenant Renault aquesta tardor? 🍂\n\n"
    "A Becier els Renault Days segueixen actius, amb 6 models diferents esperant-te: elèctrics, híbrids i de sempre.\n\n"
    "Descobreix-los al carrussel i digues-nos quin t'agrada més.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu sense IGI."
)

copy_c = (
    "6 models Renault, disponibles ara mateix a Becier. 🚗\n\n"
    "Els Renault Days s'allarguen i la varietat continua: ciutat, familiar, elèctric... el teu hi és.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becier.\n"
    "*Consulta les condicions amb els nostres assessors comercials. Preu sense IGI."
)

row = ['Juliol', 'Vehicles', '', cotxe, '', '', '', '', '', titol, copy_a, copy_b, copy_c]

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!A103:M103",
    valueInputOption='RAW',
    body={'values': [row]}
).execute()

print(f"Celdas actualizadas: {result.get('updatedCells')}")
