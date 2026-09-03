# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE'
TAB = 'Copies Ads'

duster_titol = 'Dacia Duster 🏔️'

duster_k = """Vols un tot camí de veritat per les carreteres d'Andorra sense pagar preu de luxe? 🏔️

Durant els Dies Únics Dacia, del 15 al 30 de juny, el Dacia Duster t'espera a Becier amb condicions especials.

Tracció 4x4, espai i la robustesa que el Duster porta anys demostrant dia a dia. El cotxe que resisteix qualsevol trajecte, al preu just de Dacia.

A Becier t'expliquem tot sense compromís.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

duster_l = """El Duster nou ha canviat tot. Menys el que el feia imbatible. 🏔️

Del 15 al 30 de juny, els Dies Únics Dacia arriben a Becier amb condicions especials per al Dacia Duster renovat.

Disseny actualitzat, mecàniques més eficients i la mateixa capacitat tot terreny que el converteix en el cotxe de confiança per a qualsevol carretera andorrana.

Vine a veure'l o escriu-nos i t'ho expliquem tot.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

bigster_titol = 'Dacia Bigster 🚙'

bigster_k = """Vols un SUV gran i ben equipat però no estàs disposat a pagar preu de marca premium? 🚙

Durant els Dies Únics Dacia, del 15 al 30 de juny, el nou Dacia Bigster arriba per primera vegada a Becier amb condicions especials de llançament.

Espai generós, equipament complet i tot l'estil que esperes d'un gran SUV. Al preu just de Dacia.

A Becier t'ho expliquem tot sense compromís.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

bigster_l = """El Dacia Bigster demostra que no cal gastar-se una fortuna per tenir-ho tot. 🚙

Del 15 al 30 de juny, els Dies Únics Dacia t'ofereixen l'oportunitat perfecta per estrenar el model més ambiciós de Dacia a Becier.

Gran, modern i totalment equipat per a cada viatge — llarg o curt, amb família o sense. Ara amb condicions especials.

📩 Informa't sense compromís amb l'equip de Becier.
*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs."""

data = [
    {'range': f'{TAB}!J91', 'values': [[duster_titol]]},
    {'range': f'{TAB}!K91', 'values': [[duster_k]]},
    {'range': f'{TAB}!L91', 'values': [[duster_l]]},
    {'range': f'{TAB}!J92', 'values': [[bigster_titol]]},
    {'range': f'{TAB}!K92', 'values': [[bigster_k]]},
    {'range': f'{TAB}!L92', 'values': [[bigster_l]]},
]

service.spreadsheets().values().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={'valueInputOption': 'USER_ENTERED', 'data': data}
).execute()

print('OK')
