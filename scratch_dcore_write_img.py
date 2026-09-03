# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
SHEET_TAB = 'IMG'

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"'{SHEET_TAB}'!1:1"
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)
print("Headers:", headers)

ads = [
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '23',
        'Pain principal': 'Confianza y control', 'Pain': 'Imprevistos estructurales / instalaciones antiguas / humedades',
        'Texto principal en la imagen': 'Chalets con 20 años: sabemos qué esconden.',
        'Sub texto en la imagen': 'Detectamos imprevistos antes de empezar la obra.',
        'Comentarios': 'Imagen de chalet con obra en marcha (estructura/instalaciones a la vista) + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '24',
        'Pain principal': 'Calidad', 'Pain': 'Materiales y acabados premium reales',
        'Texto principal en la imagen': 'Piedra natural, ebanistería y luz de diseño.',
        'Sub texto en la imagen': 'Materiales premium, verificados en cada partida.',
        'Comentarios': 'Imagen de detalle de acabados premium en chalet reformado + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '25',
        'Pain principal': 'Confianza y control', 'Pain': 'Un solo responsable / interlocutor único',
        'Texto principal en la imagen': 'Tu chalet, con un único responsable.',
        'Sub texto en la imagen': 'Una sola persona, todo tu proyecto.',
        'Comentarios': 'Imagen de chalet reformado, espacio amplio y luminoso + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '26',
        'Pain principal': 'Confianza y control', 'Pain': 'Equipo dedicado (arquitecto + interiorista + jefe de obra)',
        'Texto principal en la imagen': 'Arquitecto, interiorista y jefe de obra, solo para ti.',
        'Sub texto en la imagen': 'Equipo dedicado en exclusiva a tu chalet.',
        'Comentarios': 'Imagen de chalet reformado con espacio de diseño destacado + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '27',
        'Pain principal': 'Transparencia económica', 'Pain': 'Precio cerrado incluso en proyectos grandes',
        'Texto principal en la imagen': 'Chalets grandes, presupuesto cerrado desde el primer día.',
        'Sub texto en la imagen': 'Precio fijo, aunque el proyecto sea grande.',
        'Comentarios': 'Imagen de chalet de gran tamaño reformado + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '28',
        'Pain principal': 'Confianza y control', 'Pain': 'Seguimiento en tiempo real vía app',
        'Texto principal en la imagen': 'Sigue tu chalet en obra, sin ir a verlo.',
        'Sub texto en la imagen': 'Seguimiento en tiempo real desde el móvil.',
        'Comentarios': 'Imagen de chalet en obra + mockup app de seguimiento en móvil + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '29',
        'Pain principal': 'Complejidad de la obra', 'Pain': 'Coordinar estructura, jardín, piscina e instalaciones a la vez',
        'Texto principal en la imagen': 'Estructura, jardín, piscina e instalaciones. Un solo equipo.',
        'Sub texto en la imagen': 'Coordinamos todos los frentes de tu chalet.',
        'Comentarios': 'Imagen de chalet con jardín/piscina reformados + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '30',
        'Pain principal': 'Estilo de vida', 'Pain': 'Chalet heredado o de segunda mano, antiguo, sin actualizar',
        'Texto principal en la imagen': 'De chalet heredado a casa soñada.',
        'Sub texto en la imagen': 'Reforma integral, de principio a fin.',
        'Comentarios': 'Imagen contraste antes/después de chalet heredado reformado + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '31',
        'Pain principal': 'Estilo de vida', 'Pain': 'Compra reciente, reformar antes de mudarse',
        'Texto principal en la imagen': 'Compraste el chalet. Nosotros lo dejamos listo para vivir.',
        'Sub texto en la imagen': 'Reforma integral antes de tu mudanza.',
        'Comentarios': 'Imagen de chalet recién reformado, listo para entrar a vivir + texto principal y sub texto en la imagen',
    },
    {
        'Campaña': 'Reforma de Chalets', 'Formato': 'Imagen', 'Target': 'B2C', 'Anuncio': '32',
        'Pain principal': 'Plazos', 'Pain': 'Obra de chalet más larga y compleja, riesgo de que se alargue',
        'Texto principal en la imagen': 'Chalets reformados en el plazo pactado. Por contrato.',
        'Sub texto en la imagen': '800 proyectos entregados, sin retrasos.',
        'Comentarios': 'Imagen de chalet terminado + texto principal y sub texto en la imagen',
    },
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
    range=f"'{SHEET_TAB}'!A:A",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas en la pestaña '{SHEET_TAB}'.")
