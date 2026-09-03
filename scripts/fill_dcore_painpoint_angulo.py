# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1y-mNrDrhmr7tjubDh_01hp8eZ9g1wpRyQHUyqNImkB4'

GENERICO = 'Reforma integral en Madrid (genérico)'

# filas 2-11, columnas D (Pain Point) y E (Ángulo)
values = [
    ['Peleas/conflictos en la obra', 'Founder'],                  # 2 - equipo dedicado
    [GENERICO, 'Problema → Solución'],                             # 3
    [GENERICO, 'Problema → Solución'],                             # 4
    ['Proceso de reforma (transparencia del método)', 'Tutorial'], # 5 - pasos 1-4
    ['Peleas/conflictos en la obra', 'Founder'],                   # 6 - equipo dedicado
    [GENERICO, 'Emocional'],                                       # 7
    [GENERICO, 'Problema → Solución'],                             # 8
    [GENERICO, 'Emocional'],                                       # 9
    [GENERICO, 'Emocional'],                                       # 10
    [GENERICO, 'Problema → Solución'],                             # 11
]

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range="'Hoja 1'!D2:E11",
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

print(result)
