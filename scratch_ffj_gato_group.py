# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open('credentials/token_backup_20260814.json', encoding='utf-8') as f:
    token_data = json.load(f)
with open('credentials/client_secret.json', encoding='utf-8') as f:
    secret_data = json.load(f)

web_or_installed = secret_data.get('web') or secret_data.get('installed')
credentials = Credentials(
    token=token_data.get('token'),
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=web_or_installed['client_id'],
    client_secret=web_or_installed['client_secret'],
    scopes=token_data.get('scopes'),
)
credentials.refresh(Request())
service = build('sheets', 'v4', credentials=credentials)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'
TAB = 'VIDEOS'

header_result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f'{TAB}!3:3').execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)

PAIN_NUTRICION = 'Me preocupa que algo natural no cubra todo lo que mi gato necesita.'
PAIN_PRECIO = 'Me pregunto si vale la pena pagar más por algo natural.'

new_ads = [
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona (founder)', Problema=PAIN_NUTRICION,
         Hook='¿Quieres darle algo natural pero te preocupa que le falte algo importante?',
         Desenlace='Ese miedo es razonable si el producto solo promete "ser natural" sin más. Food for Joe combina ingredientes reales con una formulación veterinaria completa, para que no tengas que elegir entre natural y completo.',
         Cierre='Descubre cómo formulamos cada receta.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_PRECIO,
         Hook="¿Te cuesta justificar pagar más por algo que 'parece' lo mismo?",
         Desenlace='Por fuera puede parecer solo comida para gatos, pero por dentro hay una receta cocinada con ingredientes reales y formulada siguiendo el estándar FEDIAF, no una mezcla industrial genérica. Ahí está la diferencia que no se ve a simple vista.',
         Cierre='Descubre qué hay realmente detrás del precio.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_PRECIO,
         Hook='¿Piensas que la comida natural es un lujo que no puedes permitirte?',
         Desenlace='No tiene por qué serlo: puedes probar tu primera caja a un precio reducido gracias al código de bienvenida, y decidir después si el cambio compensa para tu gato.',
         Cierre='Prueba tu primera caja con el código WELCOME5.'),
]

for ad in new_ads:
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f'{TAB}!A:A',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [row]}
    ).execute()

# Ahora leemos todo el bloque de Gato (empieza en fila 28) y lo agrupamos por Problema
result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f'{TAB}!A28:N200').execute()
vals = result.get('values', [])
# normalizamos longitud de fila
vals = [row + [''] * (n_cols - len(row)) for row in vals]

order = []
groups = OrderedDict()
for row in vals:
    problema = row[col['Problema']]
    if problema not in groups:
        groups[problema] = []
        order.append(problema)
    groups[problema].append(row)

grouped_rows = []
for p in order:
    grouped_rows.extend(groups[p])

n_rows = len(grouped_rows)
end_row = 28 + n_rows - 1

service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f'{TAB}!A28:N{end_row}',
    valueInputOption='USER_ENTERED',
    body={'values': grouped_rows}
).execute()

print('Filas totales agrupadas:', n_rows, '-> rango A28:N%d' % end_row)
for p in order:
    print(len(groups[p]), '|', p)
