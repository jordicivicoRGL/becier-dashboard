# -*- coding: utf-8 -*-
# Ronda 3 — fix de hooks largos en AD 12, AD 14 y AD 18
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'
URL_GYM = 'https://plesh-gimnasio.vercel.app'

# AD 12 fila 18 — hook demasiado largo
ad12 = [
    'Gimnasios',
    'Dark Choco Almond Crunch Bar',
    'Imagen estatica',
    'Social proof',
    'Mas de 500 gimnasios ya venden Plesh en recepcion. El tuyo, todavia no.\n\nProducto sobre fondo blanco limpio. Numero en naranja destacado. Subtexto: "Sin azucar. Fuente de proteina. El snack que tus socios buscan."',
    'El tuyo, el siguiente? Solicita condiciones',
    URL_GYM
]

# AD 14 fila 20 — hook de dos frases complejas
ad14 = [
    'Gimnasios',
    'Snacks Plesh (general)',
    'Imagen estatica',
    'Objecion: socios con nutricion propia',
    'Tu socio mas comprometido lleva la nutricion controlada. Hasta que encuentra Plesh en recepcion.\n\nFoto de socio en recepcion cogiendo Plesh. Copy en overlay. Tono de argumento directo, no emocional.',
    'Dale lo que busca - solicita catalogo',
    URL_GYM
]

# AD 18 fila 24 — hook fragmentado en 4 piezas
ad18 = [
    'Gimnasios',
    'Pack de prueba',
    'Imagen estatica',
    'Sin riesgo de entrada',
    'Pack de prueba. Sin compromisos de volumen, sin permanencia.\n\nFondo blanco. Producto en primer plano. Copy minimalista. Sub: "Comprueba si rota en tu centro - repon solo si funciona."',
    'Pide el pack de prueba - sin compromisos',
    URL_GYM
]

updates = [
    ('Creatividades!A18:G18', [ad12]),
    ('Creatividades!A20:G20', [ad14]),
    ('Creatividades!A24:G24', [ad18]),
]

for range_name, values in updates:
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
    print(f'Actualizado: {range_name}')

print('\nRonda 3 completada - 3 hooks corregidos.')
