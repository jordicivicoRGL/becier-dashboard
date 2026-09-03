# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'
VID_GID  = 2067151146  # sheetId de la pestaña VID

# ── 1. HOOKS MEJORADOS ──────────────────────────────────────────────────────
improved_hooks = [
    (4,  '¿Sabrías distinguir un ingrediente real de un subproducto en la etiqueta del pienso?'),
    (6,  '¿Has probado ya tres champús antiparasitarios y tu perro sigue rascándose igual?'),
    (8,  '¿Tu perro está en su peso ideal o lleva meses sin conseguirlo aunque lo controles?'),
    (13, '¿Sabes lo que significa "harina de origen animal" en el pienso que le das a tu perro?'),
    (27, '¿Tu perro tiene digestión irregular y el veterinario te dice que está sano?'),
    (34, '¿Sabías que el pienso de alta gama pasa por los mismos procesos que la comida basura?'),
    (36, '¿Sabe tu veterinario que el pienso que recomienda lleva conservantes artificiales?'),
    (37, 'Te dijeron que la comida casera para perros no era completa. ¿Qué pasa si eso es falso?'),
    (38, 'El pienso de 80€/kg también está ultraprocesado. ¿Lo sabías?'),
    (39, '¿Sabías que la esperanza de vida media de los perros ha bajado en los últimos 30 años?'),
    (42, '¿Cuántos años llevas dándole pienso a tu perro sin saber lo que lleva realmente?'),
    (45, '¿Cuántos nutrientes pierde el pienso en el proceso de fabricación?'),
    (51, '¿Tu perro de 8kg come exactamente lo mismo que uno de 30kg? Aquí hay un problema.'),
    (54, '¿Te frena el no saber cómo gestionar la comida congelada en casa?'),
    (55, 'Cada semana con el pienso actual tiene un coste que no ves en el veterinario. ¿Lo sabías?'),
]

values_data = [
    {'range': f'VID!F{row}', 'values': [[hook]]}
    for row, hook in improved_hooks
]

service.spreadsheets().values().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={'valueInputOption': 'USER_ENTERED', 'data': values_data}
).execute()
print(f'Hooks actualizados: {len(improved_hooks)}')

# ── 2. COLOR — TOP 6 en amarillo dorado, resto en blanco ───────────────────
GOLD  = {'red': 1.0,  'green': 0.851, 'blue': 0.4}   # #FFD966
WHITE = {'red': 1.0,  'green': 1.0,   'blue': 1.0}

top6_rows = {9, 11, 12, 41, 50, 52}

# Filas con hook (todas las que tienen contenido en col F)
all_hook_rows = [r for r, _ in improved_hooks] + [
    5, 7, 10, 14, 15, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33,
    35, 40, 43, 44, 46, 47, 48, 49, 53, 9, 11, 12, 41, 50, 52
]

format_requests = []
for row in set(all_hook_rows):
    color = GOLD if row in top6_rows else WHITE
    format_requests.append({
        'repeatCell': {
            'range': {
                'sheetId': VID_GID,
                'startRowIndex': row - 1,
                'endRowIndex': row,
                'startColumnIndex': 5,  # col F
                'endColumnIndex': 6
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    })

service.spreadsheets().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={'requests': format_requests}
).execute()
print(f'Celdas formateadas: {len(format_requests)} (6 en dorado, resto en blanco)')
