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

base = {'Negocio': 'B2C', 'Target': 'Zonas premium Madrid', 'Utilizado': False}

pains = [
    ('Obra visible desde fuera: furgonetas, obreros y ruido que exponen la vivienda y comprometen su privacidad/seguridad',
     'Que se vea la obra desde la calle no es una opción en tu casa.',
     '¿Quieres que todo el barrio vea la obra de tu casa?'),
    ('Reforma que desentona con la zona: miedo a que el resultado no esté a la altura del entorno',
     'Una reforma que desentona con tu zona, se paga en reputación.',
     '¿Y si tu reforma no está a la altura de tu zona?'),
    ('Cero tiempo para gestionar, cero margen de error: delega sin supervisar pero no puede permitirse que algo salga mal',
     'Aquí, un error en la reforma no es una opción.',
     '¿Puedes permitirte un error en la reforma de tu casa?'),
    ('Estar a la altura de su círculo: quiere un resultado al nivel de las viviendas de referencia de su entorno',
     'Tu casa debe hablar tan bien de ti como tu dirección.',
     '¿Tu casa habla tan bien de ti como tu dirección?'),
    ('Domótica, seguridad y climatización de nivel alto, no solo estética',
     'Una vivienda como la tuya exige más que buen gusto.',
     '¿Tu vivienda tiene la domótica y seguridad que merece?'),
    ('Interlocutor de máxima confianza para quien gestiona por él (pareja, asistente, family office)',
     'Gestionar la reforma de otra persona sin confianza total, es un riesgo.',
     '¿Confiarías la reforma de tu casa a cualquiera?'),
    ('Proyecto "de catálogo": miedo a recibir el mismo diseño y materiales estándar que cualquier reforma',
     'Tu casa no es un proyecto más de catálogo.',
     '¿Quieres el mismo proyecto de catálogo que cualquier reforma?'),
    ('Constructoras generalistas sin trayectoria en vivienda de alto standing',
     'No cualquier constructora está a la altura de tu vivienda.',
     '¿Está tu constructora preparada para una vivienda como la tuya?'),
]

rows = []
for problema, hook_afirm, hook_preg in pains:
    for hook in (hook_afirm, hook_preg):
        ad = {**base, 'Problema': problema, 'Hook': hook}
        row = [''] * n_cols
        for field, value in ad.items():
            if field in col:
                row[col[field]] = value
        rows.append(row)

# Sobrescribe las 8 filas antiguas (60-67) con las 16 nuevas, en orden por pain point
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_TAB}'!A60",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas (16) en '{SHEET_TAB}' a partir de la fila 60, ordenadas por pain point.")
