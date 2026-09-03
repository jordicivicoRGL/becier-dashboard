# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'

# Correcciones: (rango, valor_correcto)
# Solo columna E (Problema) para las filas que escribi sin acentos
corrections = [
    ('VID!E25', 'Pata manchada de naranja/marrón por lamido crónico'),
    ('VID!E26', 'Mal aliento crónico que no mejora con nada'),
    ('VID!E27', 'Dermatitis atópica diagnosticada'),
    ('VID!E30', 'Caspa y piel seca sin solución'),
    ('VID!E33', 'Ojos con muchas legañas de forma crónica'),
    ('VID!E38', 'Mi veterinario me recomienda ese pienso, así que es bueno'),
    ('VID!E41', 'Los perros viven menos de lo que deberían según estudios recientes'),
    ('VID!E42', 'Enfermedades crónicas (cáncer, ERC, diabetes) aumentan en perros jóvenes'),
    ('VID!E43', 'Querer más años de vida con calidad junto a su perro'),
    ('VID!E45', 'Llevar años dándole pienso pensando que hacía lo correcto'),
    ('VID!E46', 'Haber ignorado los síntomas del perro por mucho tiempo'),
    ('VID!E48', 'Cuánto cuesta realmente alimentar bien a un perro al día'),
    ('VID!E49', 'Ya probé comida casera pero no sabía si la dieta era completa'),
    ('VID!E50', 'Perro con alergias crónicas que mejoró al cambiar la alimentación'),
    ('VID!E51', 'Dueño que notó el cambio de energía en su perro senior'),
    ('VID!E53', 'Cómo está formulado el plan según raza, peso y condición'),
    ('VID!E54', 'El quiz y cómo funciona la personalización de la dieta'),
    ('VID!E55', 'Qué ingredientes reales lleva cada receta de FFJ'),
    ('VID!E56', 'Cómo llega el pedido y cómo se gestiona el congelado en casa'),
]

data = [{'range': r, 'values': [[v]]} for r, v in corrections]

result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
).execute()

print(f"Celdas actualizadas: {result.get('totalUpdatedCells', 0)}")
