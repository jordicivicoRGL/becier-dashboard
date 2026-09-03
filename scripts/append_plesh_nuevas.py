# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'
URL_CAF = 'https://plesh-cafeterias.vercel.app'
URL_GYM = 'https://plesh-gimnasio.vercel.app'

# Columnas: Target, Producto, Formato, Tipo, Hook / Idea principal, CTA, Landing
nuevos_ads = [
    # CAFETERÍAS
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Lifestyle',
        '¿Cuántos clientes te piden algo dulce sin azúcar y te quedas sin respuesta?',
        'Ten la respuesta. Solicita información',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Milk Choco Salted Caramel Almond Bites',
        'Imagen estática',
        'Producto',
        'El snack que piden sin que nadie se lo ofrezca.',
        'Ponlo en tu mostrador',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Diseño',
        'Tu mostrador te diferencia. O te hace igual que todas las demás.',
        'Diferéncialo. Solicita condiciones',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Lifestyle',
        'Con el café van a pedir algo. La pregunta es si lo tienes.',
        'Tenlo. Solicita catálogo',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Pack de prueba',
        'Imagen estática',
        'Infografia',
        'Lo que ingresa de media un punto de venta Plesh al mes.',
        'Calcula el tuyo. Solicita condiciones',
        URL_CAF
    ],

    # GIMNASIOS
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Lifestyle',
        'Tu socio acaba de entrenar. Tiene hambre. ¿Qué le ofreces?',
        'Dale algo. Solicita catálogo',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Diseño',
        'Recepción abierta 10 horas al día. Sin vender nada.',
        'Cámbialo. Solicita información',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Producto',
        'El snack de tu recepción dice mucho de tu centro.',
        'Mejóralo. Solicita información',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Diseño',
        'El gimnasio de al lado ya tiene Plesh.',
        '¿Y el tuyo? Solicita condiciones',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Lifestyle',
        'Sin Plesh, tus socios compran el snack en otro sitio...',
        'Quédate con esa venta. Solicita condiciones',
        URL_GYM
    ],
]

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A:G',
    valueInputOption='USER_ENTERED',
    body={'values': nuevos_ads}
).execute()

print(f'OK — {len(nuevos_ads)} nuevos ADs añadidos.')
