# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE'
TAB = 'Copies Ads'

scenic_titol = 'Renault Grand Scenic 🚐'

scenic_a = """Necessites un cotxe familiar o un SUV que estalviï combustible? 🤔

Aquest mes a Becier Vehicles tens dues opcions d'ocasió que ho tenen tot. El Renault Grand Scenic: 7 places, 150 CV automàtic i només 30.000 km, amb sostre solar panoràmic, pantalla amb Apple CarPlay i Android Auto, aparcament automàtic i seients posteriors regulables per facilitar l'accés. I el Dacia Duster híbrid, km 0, acabat Journey amb doble pantalla, navegació integrada, càmeres i sensors, i consums de menys de 5 l/100 km.

Fes un cop d'ull al vídeo i descobreix quin encaixa millor amb la teva família.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

scenic_b = """Imagina't estrenant un cotxe pensat per a tu i la família. 😍

El Renault Grand Scenic t'ofereix 7 places, seients posteriors que es mouen per fer-te la vida més fàcil, sostre solar panoràmic i tecnologia amb Apple CarPlay i Android Auto, tot amb només 30.000 km. Si prefereixes un SUV que no passa desapercebut, el Dacia Duster híbrid, km 0, acabat Journey, et porta doble pantalla, navegació integrada i consums de menys de 5 l/100 km per gaudir de cada trajecte sense preocupar-te pel dipòsit.

Descobreix-los al vídeo.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

scenic_c = """Un SUV híbrid amb menys de 5 l/100 km de consum? Existeix. 🚙

És el Dacia Duster, km 0, acabat Journey, amb doble pantalla, navegació integrada i motor híbrid autorecarregable de 155 CV. I si busques espai per a tota la família, el Renault Grand Scenic ofereix 7 places, 150 CV automàtic i només 30.000 km, amb sostre solar panoràmic i aparcament automàtic inclòs.

Fes un cop d'ull al vídeo i tria el teu.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

duster_titol = 'Dacia Duster 🚙'

data = [
    {'range': f'{TAB}!A107', 'values': [['Agost']]},
    {'range': f'{TAB}!B107', 'values': [['Vehicles']]},
    {'range': f'{TAB}!D107', 'values': [['Renault Grand Scenic / Dacia Duster']]},
    {'range': f'{TAB}!J107', 'values': [[scenic_titol]]},
    {'range': f'{TAB}!K107', 'values': [[scenic_a]]},
    {'range': f'{TAB}!L107', 'values': [[scenic_b]]},
    {'range': f'{TAB}!M107', 'values': [[scenic_c]]},
]

service.spreadsheets().values().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={'valueInputOption': 'USER_ENTERED', 'data': data}
).execute()

print('OK')
