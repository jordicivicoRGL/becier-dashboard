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

titol = "Assegurança de viatge 🧳"

copy_a = (
    "Un imprevist mèdic o un vol cancel·lat pot costar-te més que tot el viatge junt. 🌍\n\n"
    "Sense assegurança, cada contratemps a l'estranger surt directament de la teva butxaca — i els preus fora de casa es disparen ràpid.\n\n"
    "A Becser personalitzem la teva assegurança de viatge segons el teu perfil: Vacacional, Integral o Prestige, per cobrir exactament el que necessites.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becser.\n"
    "*Consulta les condicions amb els nostres assessors comercials."
)

copy_b = (
    "Viatjar hauria de ser desconnectar, no patir per si passa alguna cosa. 🧳\n\n"
    "A Becser dissenyem la teva assegurança de viatge perquè gaudeixis de cada moment amb tranquil·litat real, sigui quina sigui la teva destinació.\n\n"
    "Vacacional, Integral o Prestige: tu tries el nivell de cobertura que necessites per al teu viatge.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becser.\n"
    "*Consulta les condicions amb els nostres assessors comercials."
)

copy_c = (
    "Vacacional, Integral o Prestige: tres nivells de cobertura, un sol viatge tranquil. 🌍\n\n"
    "A Becser personalitzem la teva assegurança de viatge segons on vas, quant de temps hi ets i què vols tenir cobert.\n\n"
    "Així no pagues per allò que no et cal, i vas cobert en allò que sí importa.\n\n"
    "📩 Informa't sense compromís amb l'equip de Becser.\n"
    "*Consulta les condicions amb els nostres assessors comercials."
)

values = [[titol, copy_a, copy_b, copy_c]]

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_NAME}'!J97:M97",
    valueInputOption='RAW',
    body={'values': values}
).execute()

print(f"Celdas actualizadas: {result.get('updatedCells')}")
