# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
SHEET_TAB = 'VID'

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"'{SHEET_TAB}'!3:3"
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)
print("Headers:", headers)

base = {'Negocio': 'B2C', 'Target': 'Zonas premium Madrid', 'Utilizado': False}

pains = [
    'Obra visible desde fuera: furgonetas, obreros y ruido que exponen la vivienda y comprometen su privacidad/seguridad',
    'Reforma que desentona con la zona: miedo a que el resultado no esté a la altura del entorno',
    'Cero tiempo para gestionar, cero margen de error: delega sin supervisar pero no puede permitirse que algo salga mal',
    'Estar a la altura de su círculo: quiere un resultado al nivel de las viviendas de referencia de su entorno',
    'Domótica, seguridad y climatización de nivel alto, no solo estética',
    'Interlocutor de máxima confianza para quien gestiona por él (pareja, asistente, family office)',
    'Proyecto "de catálogo": miedo a recibir el mismo diseño y materiales estándar que cualquier reforma',
    'Constructoras generalistas sin trayectoria en vivienda de alto standing',
]

rows = []
for pain in pains:
    ad = {**base, 'Problema': pain}
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_TAB}'!A:A",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas (solo Negocio/Target/Utilizado/Problema) en '{SHEET_TAB}'.")
