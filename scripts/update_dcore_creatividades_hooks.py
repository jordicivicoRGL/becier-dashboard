# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1y-mNrDrhmr7tjubDh_01hp8eZ9g1wpRyQHUyqNImkB4'

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range='1:1'
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)

TARGET = 'Comunidad de Madrid - Propietarios 35-64 (piso/chalet)'
CAMPANA = 'Reforma Integral B2C'

ads = [
    {
        'Formato': 'Vídeo', 'Pain Point': 'Presupuesto sin sobrecostes', 'Ángulo': 'Problema → Solución',
        'Hook/problema (texto principal en la imagen)': 'Reformar tu casa sin sustos en el presupuesto',
        'Beneficio (sub texto en la imagen)': 'Presupuesto cerrado por partidas, constructora propia',
        'CTA': 'Pide tu presupuesto cerrado',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Presupuesto sin sobrecostes', 'Ángulo': 'Testimonial',
        'Hook/problema (texto principal en la imagen)': 'Reformamos su casa sin costes ocultos',
        'Beneficio (sub texto en la imagen)': 'Cumplimos lo pactado, siempre',
        'CTA': 'Solicita tu presupuesto sin compromiso',
    },
    {
        'Formato': 'Carrusel', 'Pain Point': 'Peleas/conflictos en la obra', 'Ángulo': 'Comparativo',
        'Hook/problema (texto principal en la imagen)': 'Reformar tu casa con 3 empresas distintas: caos garantizado',
        'Beneficio (sub texto en la imagen)': 'Un solo equipo para tu reforma',
        'CTA': 'Conoce a tu equipo dedicado',
    },
    {
        'Formato': 'Vídeo', 'Pain Point': 'Peleas/conflictos en la obra', 'Ángulo': 'Founder',
        'Hook/problema (texto principal en la imagen)': 'Tu reforma, un solo equipo responsable',
        'Beneficio (sub texto en la imagen)': 'Arquitecto, interiorista y obra, juntos',
        'CTA': 'Habla con tu equipo de proyecto',
    },
    {
        'Formato': 'Vídeo', 'Pain Point': 'Supervisión y seguimiento de obra', 'Ángulo': 'Demostración',
        'Hook/problema (texto principal en la imagen)': '¿Sabes cómo va tu reforma esta semana?',
        'Beneficio (sub texto en la imagen)': 'Seguimiento de tu obra en tiempo real',
        'CTA': 'Descubre el seguimiento en tiempo real',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Supervisión y seguimiento de obra', 'Ángulo': 'Emocional',
        'Hook/problema (texto principal en la imagen)': 'Reformar tu casa sin noches sin dormir',
        'Beneficio (sub texto en la imagen)': 'Sabes en todo momento cómo va tu reforma',
        'CTA': 'Empieza tu reforma sin sorpresas',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Disponibilidad/tiempos de ejecución', 'Ángulo': 'Dato/Estadística',
        'Hook/problema (texto principal en la imagen)': '+800 reformas en Madrid, en los plazos pactados',
        'Beneficio (sub texto en la imagen)': 'Diseño y obra, mismo equipo',
        'CTA': 'Pide tu calendario de obra estimado',
    },
    {
        'Formato': 'Carrusel', 'Pain Point': 'Disponibilidad/tiempos de ejecución', 'Ángulo': 'Social proof',
        'Hook/problema (texto principal en la imagen)': '20 años reformando casas en Madrid',
        'Beneficio (sub texto en la imagen)': 'Plazos reales, constructora propia',
        'CTA': 'Conoce nuestros proyectos ejecutados',
    },
]

rows = []
for ad in ads:
    row = [''] * n_cols
    row[col['Campaña']] = CAMPANA
    row[col['Target']] = TARGET
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range="'Hoja 1'!A13:I20",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(result)
