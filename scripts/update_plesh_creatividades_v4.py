# -*- coding: utf-8 -*-
# Ronda 2 de mejoras — solo actualiza los ADs con problemas detectados
# AD 3, AD 4, AD 5 (cafeterias) y AD 14, AD 18 (gimnasios)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'
URL_CAF = 'https://plesh-cafeterias.vercel.app'
URL_GYM = 'https://plesh-gimnasio.vercel.app'

# AD 3 fila 9 — hook vago -> hook con impacto directo
ad3 = [
    'Cafeterias',
    'Milk Choco Salted Caramel Almond Bites',
    'Carrusel',
    'Demostracion',
    'El mostrador cambia. La caja registradora, tambien.\n\nT1: mostrador sin snack saludable. T2: mano cogiendo Plesh al lado de la caja. T3: texto "El cliente saludable recompra. Siempre." T4: CTA + pack de prueba.',
    'Compruebalo - pide el pack de prueba',
    URL_CAF
]

# AD 4 fila 10 — T3 mezclaba pregunta y CTA -> 4 tarjetas limpias
ad4 = [
    'Cafeterias',
    'Pack de prueba',
    'Carrusel',
    'Comparativo',
    'La cafeteria de al lado ya vende Plesh. La tuya tambien?\n\nT1: mostrador estandar sin diferencial. T2: mismo mostrador con Plesh visible y cliente comprando. T3: pregunta visual - "Cual es el tuyo?" T4: CTA limpio.',
    'Rellena el formulario - condiciones en 48h',
    URL_CAF
]

# AD 5 fila 11 — angulo falso (Dato sin dato) + solapa con AD 1 -> angulo Margen (unico que faltaba)
ad5 = [
    'Cafeterias',
    'Snacks Plesh (general)',
    'Imagen estatica',
    'Margen',
    'Cada unidad de Plesh que vendes tiene el margen de un cafe. Sin preparacion, sin tiempo.\n\nFondo oscuro. Headline en naranja Plesh. Sub: "Te contactamos en 48h con precios y condiciones de distribucion."',
    'Cuanto puedes ganar - solicita condiciones',
    URL_CAF
]

# AD 14 fila 20 — hook generico -> objecion real: socios con su propia nutricion
ad14 = [
    'Gimnasios',
    'Snacks Plesh (general)',
    'Imagen estatica',
    'Objecion: socios con nutricion propia',
    'Tus socios mas comprometidos son los que mas cuidan lo que comen. Y los que mas te compran si les das algo que encaje.\n\nFoto de socio en recepcion cogiendo Plesh. Copy en overlay. Tono de argumento, no de emocion.',
    'Dale lo que busca - solicita catalogo',
    URL_GYM
]

# AD 18 fila 24 — solapa con AD 11 -> angulo Sin riesgo de entrada (unico que faltaba en gym)
ad18 = [
    'Gimnasios',
    'Pack de prueba',
    'Imagen estatica',
    'Sin riesgo de entrada',
    'Pack de prueba. Sin compromisos de volumen. Sin permanencia. Solo comprueba si rota en tu centro.\n\nFondo blanco. Producto en primer plano. Copy minimalista. Sub: "Empieza sin compromiso - repon solo si funciona."',
    'Pide el pack de prueba - sin compromisos',
    URL_GYM
]

# Actualizar celdas especificas por fila
updates = [
    ('Creatividades!A9:G9', [ad3]),
    ('Creatividades!A10:G10', [ad4]),
    ('Creatividades!A11:G11', [ad5]),
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

print('\nRonda 2 completada - 5 ADs mejorados.')
