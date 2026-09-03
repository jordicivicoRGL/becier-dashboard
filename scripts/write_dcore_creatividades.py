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
        'Hook/problema (texto principal en la imagen)': 'Presupuesto cerrado. Sin sorpresas.',
        'Beneficio (sub texto en la imagen)': 'Constructora propia, sin intermediarios',
        'CTA': 'Pide tu presupuesto cerrado',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Presupuesto sin sobrecostes', 'Ángulo': 'Testimonial',
        'Hook/problema (texto principal en la imagen)': 'Sin costes ocultos',
        'Beneficio (sub texto en la imagen)': 'Cumplimos lo pactado, siempre',
        'CTA': 'Solicita tu presupuesto sin compromiso',
    },
    {
        'Formato': 'Carrusel', 'Pain Point': 'Peleas/conflictos en la obra', 'Ángulo': 'Comparativo',
        'Hook/problema (texto principal en la imagen)': '3 profesionales, 0 responsables',
        'Beneficio (sub texto en la imagen)': 'Un solo equipo para tu proyecto',
        'CTA': 'Conoce a tu equipo dedicado',
    },
    {
        'Formato': 'Vídeo', 'Pain Point': 'Peleas/conflictos en la obra', 'Ángulo': 'Founder',
        'Hook/problema (texto principal en la imagen)': 'Un equipo. Un proyecto.',
        'Beneficio (sub texto en la imagen)': 'Arquitecto, interiorista y obra, juntos',
        'CTA': 'Habla con tu equipo de proyecto',
    },
    {
        'Formato': 'Vídeo', 'Pain Point': 'Supervisión y seguimiento de obra', 'Ángulo': 'Demostración',
        'Hook/problema (texto principal en la imagen)': '¿Sabes qué pasa en tu obra?',
        'Beneficio (sub texto en la imagen)': 'Seguimiento en tiempo real',
        'CTA': 'Descubre el seguimiento en tiempo real',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Supervisión y seguimiento de obra', 'Ángulo': 'Emocional',
        'Hook/problema (texto principal en la imagen)': 'Reformar sin noches sin dormir',
        'Beneficio (sub texto en la imagen)': 'Sabes en todo momento cómo va tu obra',
        'CTA': 'Empieza tu reforma sin sorpresas',
    },
    {
        'Formato': 'Imagen', 'Pain Point': 'Disponibilidad/tiempos de ejecución', 'Ángulo': 'Dato/Estadística',
        'Hook/problema (texto principal en la imagen)': '+800 proyectos. Plazos que se cumplen',
        'Beneficio (sub texto en la imagen)': 'Diseño y obra, mismo equipo',
        'CTA': 'Pide tu calendario de obra estimado',
    },
    {
        'Formato': 'Carrusel', 'Pain Point': 'Disponibilidad/tiempos de ejecución', 'Ángulo': 'Social proof',
        'Hook/problema (texto principal en la imagen)': '20 años. 800+ proyectos.',
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

result = service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='A:A',
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(result.get('updates', {}))
