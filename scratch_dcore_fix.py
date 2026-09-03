# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
VID_GID = 389607696
IMG_TAB = 'IMG'

# 1. Borrar las 12 filas erróneas de VID (filas 52-63, 1-indexed -> startIndex=51, endIndex=63)
service.spreadsheets().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={
        'requests': [{
            'deleteDimension': {
                'range': {
                    'sheetId': VID_GID,
                    'dimension': 'ROWS',
                    'startIndex': 51,
                    'endIndex': 63
                }
            }
        }]
    }
).execute()
print("Filas 52-63 borradas de VID.")

# 2. Añadir las 12 filas equivalentes como imágenes en IMG
header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"'{IMG_TAB}'!1:1"
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)
print("Headers IMG:", headers)

base = {'Formato': 'Imagen', 'Target': 'B2C'}

ads = [
    {**base, 'Anuncio': '33', 'Pain principal': 'Confianza y control',
     'Pain': 'Imprevistos estructurales / instalaciones antiguas / humedades',
     'Texto principal en la imagen': 'Los imprevistos ocultos encarecen la reforma de tu chalet.',
     'Sub texto en la imagen': 'Evaluamos tu chalet antes de presupuestar.'},

    {**base, 'Anuncio': '34', 'Pain principal': 'Calidad',
     'Pain': 'Necesidad de materiales y acabados de alta gama a la altura de un chalet premium',
     'Texto principal en la imagen': 'Cada acabado de tu chalet, a la altura de tu inversión.',
     'Sub texto en la imagen': 'Materiales de alta gama en cada detalle.'},

    {**base, 'Anuncio': '35', 'Pain principal': 'Calidad',
     'Pain': 'Necesidad de materiales y acabados de alta gama a la altura de un chalet premium',
     'Texto principal en la imagen': 'Solo materiales de alta gama en la reforma de tu chalet.',
     'Sub texto en la imagen': 'Los mismos que exigiríamos en la nuestra.'},

    {**base, 'Anuncio': '36', 'Pain principal': 'Calidad',
     'Pain': 'Necesidad de especialización en reformas de chalets de alto nivel',
     'Texto principal en la imagen': 'Especialistas en reformas de chalets de alto nivel en Madrid.',
     'Sub texto en la imagen': '+800 proyectos, +20 años de experiencia.'},

    {**base, 'Anuncio': '37', 'Pain principal': 'Confianza y control',
     'Pain': 'Un solo responsable / interlocutor único',
     'Texto principal en la imagen': 'En la reforma de tu chalet, sin responsable, pagas tú.',
     'Sub texto en la imagen': 'Un jefe de obra dedicado, siempre disponible.'},

    {**base, 'Anuncio': '38', 'Pain principal': 'Confianza y control',
     'Pain': 'Equipo dedicado (arquitecto + interiorista + jefe de obra)',
     'Texto principal en la imagen': 'Empresas sin coordinar retrasan la reforma de tu chalet.',
     'Sub texto en la imagen': 'Equipo propio: arquitecto, interiorista y jefe de obra.'},

    {**base, 'Anuncio': '39', 'Pain principal': 'Transparencia económica',
     'Pain': 'Precio cerrado incluso en proyectos grandes',
     'Texto principal en la imagen': 'Los sobrecostes duelen en la reforma de un chalet.',
     'Sub texto en la imagen': 'Presupuesto cerrado, sin importar el tamaño.'},

    {**base, 'Anuncio': '40', 'Pain principal': 'Confianza y control',
     'Pain': 'Seguimiento en tiempo real vía app',
     'Texto principal en la imagen': 'No saber cómo va la reforma de tu chalet, desespera.',
     'Sub texto en la imagen': 'Sigue tu obra en tiempo real desde el móvil.'},

    {**base, 'Anuncio': '41', 'Pain principal': 'Complejidad de la obra',
     'Pain': 'Coordinar estructura, jardín, piscina e instalaciones a la vez',
     'Texto principal en la imagen': 'Coordinarlo todo en la reforma de un chalet, se descontrola.',
     'Sub texto en la imagen': 'Estructura, jardín, piscina e instalaciones, un solo equipo.'},

    {**base, 'Anuncio': '42', 'Pain principal': 'Estilo de vida',
     'Pain': 'Chalet heredado o de segunda mano, antiguo, sin actualizar',
     'Texto principal en la imagen': 'La reforma de un chalet heredado, pesa.',
     'Sub texto en la imagen': 'Reforma integral, de principio a fin.'},

    {**base, 'Anuncio': '43', 'Pain principal': 'Estilo de vida',
     'Pain': 'Compra reciente, reformar antes de mudarse',
     'Texto principal en la imagen': 'Reformar tu chalet antes de mudarte, retrasa todo.',
     'Sub texto en la imagen': 'Nos encargamos de todo antes de tu mudanza.'},

    {**base, 'Anuncio': '44', 'Pain principal': 'Plazos',
     'Pain': 'Obra de chalet más larga y compleja, riesgo de que se alargue',
     'Texto principal en la imagen': 'El retraso en la reforma de tu chalet, frustra.',
     'Sub texto en la imagen': '800 proyectos entregados en el plazo pactado.'},
]

rows = []
for ad in ads:
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f"'{IMG_TAB}'!A:A",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas nuevas en IMG (Anuncio 33-44).")
