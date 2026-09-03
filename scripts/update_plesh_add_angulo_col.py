# -*- coding: utf-8 -*-
# Reestructura el Sheet de Plesh:
# - Inserta columna E "Angulo" (desplaza Hook, CTA, Landing a F, G, H)
# - Columna D "Tipo" pasa a ser el tipo creativo (UGC, Founder, Producto, Lifestyle, Diseno, Infografia)
# - Columna E "Angulo" contiene el angulo estrategico (lo que antes estaba en D)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'

# ── PASO 1: Insertar columna en blanco en posicion E (indice 4) ──────────────
service.spreadsheets().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={
        'requests': [{
            'insertDimension': {
                'range': {
                    'sheetId': 1322553101,
                    'dimension': 'COLUMNS',
                    'startIndex': 4,  # columna E (0-based)
                    'endIndex': 5
                },
                'inheritFromBefore': False
            }
        }]
    }
).execute()
print('Columna E insertada.')

# ── PASO 2: Actualizar cabecera E1 = "Angulo" ─────────────────────────────────
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='Creatividades!E1',
    valueInputOption='RAW',
    body={'values': [['Angulo']]}
).execute()
print('Cabecera E1 = Angulo.')

# ── PASO 3: Escribir tipos creativos en D7:D26 y angulos en E7:E26 ───────────
# Formato: [Tipo_creativo, Angulo_estrategico]
# El angulo era lo que teniamos en D antes (ahora va a E)
# El tipo creativo es nuevo en D

ad_data = [
    # Target era cafeterias
    ['Lifestyle',   'Problema - Solucion'],       # AD 1
    ['Diseno',      'Social proof'],              # AD 2
    ['Lifestyle',   'Demostracion'],              # AD 3
    ['Lifestyle',   'Comparativo'],               # AD 4
    ['Diseno',      'Margen'],                    # AD 5
    ['UGC',         'Testimonial'],               # AD 6
    ['Lifestyle',   'Before / After'],            # AD 7
    ['Lifestyle',   'Emocional'],                 # AD 8
    ['Founder',     'Founder'],                   # AD 9
    ['Infografia',  'Tutorial'],                  # AD 10
    # Target era gimnasios
    ['Diseno',      'Ingresos pasivos'],          # AD 11
    ['Producto',    'Social proof'],              # AD 12
    ['Lifestyle',   'Objecion: espacio'],         # AD 13
    ['Lifestyle',   'Objecion: socios'],          # AD 14
    ['Lifestyle',   'Momento post-entreno'],      # AD 15
    ['UGC',         'Testimonial'],               # AD 16
    ['Lifestyle',   'Before / After'],            # AD 17
    ['Producto',    'Sin riesgo de entrada'],     # AD 18
    ['Founder',     'Founder'],                   # AD 19
    ['Infografia',  'Tutorial'],                  # AD 20
]

tipos   = [[row[0]] for row in ad_data]
angulos = [[row[1]] for row in ad_data]

service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='Creatividades!D7:D26',
    valueInputOption='RAW',
    body={'values': tipos}
).execute()
print('Columna D (Tipo creativo) actualizada.')

service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='Creatividades!E7:E26',
    valueInputOption='RAW',
    body={'values': angulos}
).execute()
print('Columna E (Angulo) actualizada.')

# ── PASO 4: Verificacion rapida ───────────────────────────────────────────────
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A1:H1'
).execute()
headers = result.get('values', [[]])[0]
print(f'\nCabeceras finales: {headers}')

result2 = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A7:H8'
).execute()
for row in result2.get('values', []):
    print(f'Ejemplo fila: {row}')
