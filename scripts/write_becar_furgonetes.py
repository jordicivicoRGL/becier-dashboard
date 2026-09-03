# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE'
TAB = 'Copies Ads'

CIERRE = "\n\n📩 Reserva la teva furgoneta amb AVIS.\n*Consulta la disponibilitat i les condicions amb els nostres assessors comercials."

rows = {
    93: {  # Carrusel
        'titol': 'Furgonetes en lloguer 🚐',
        'v1': "Necessites una furgoneta per a un viatge en grup, una mudança o uns dies de feina? 🚐\n\nA AVIS tens la furgoneta per a cada necessitat: espai per a persones, mobles o material, sempre a punt.\n\nLa reserves només pels dies que et calgui, sense compromisos llargs." + CIERRE,
        'v2': "Un viatge en grup, una mudança o una feina que no s'atura: cada situació té la seva furgoneta. 🚐\n\nA AVIS tens diferents opcions de furgonetes en lloguer, adaptades al que necessitis en cada moment.\n\nReserva-la pels dies exactes i oblida't de complicacions." + CIERRE,
        'v3': "Hi ha moments en què el cotxe no n'hi ha prou: un grup gran, una mudança, una feina amb molt material. 🚐\n\nPer a tot això, a AVIS tens la furgoneta que et fa falta: espai de sobres i lloguer flexible pels dies que necessitis." + CIERRE,
    },
    94: {  # Master - mudances
        'titol': 'Furgoneta per a mudances 📦',
        'v1': "T'has quedat sense espai per moure els mobles o les caixes de la mudança? 📦\n\nA AVIS tens la furgoneta que necessites, pel temps que necessites. Sense compromisos llargs ni sorpreses.\n\nReserva-la per uns dies i fes la mudança sense estrès, carregant-ho tot d'un sol cop." + CIERRE,
        'v2': "Quantes vegades has hagut de fer dos viatges perquè el cotxe no t'ha cabut tot? 📦\n\nAmb la furgoneta d'AVIS, la mudança es fa en un sol trajecte. Espai de sobres per als mobles, les caixes i tot el que calgui moure.\n\nLa reserves pels dies que et facin falta i la tornes quan acabis." + CIERRE,
        'v3': "La mudança sempre és més complicada quan no tens on carregar-ho tot. 📦\n\nA AVIS lloguem furgonetes pensades exactament per això: espai ampli, fàcils de conduir i disponibles pel temps que necessitis.\n\nDemana-la per als dies de la mudança i oblida't dels viatges de més." + CIERRE,
    },
    95: {  # Trafic - feina
        'titol': 'Furgoneta de feina 🔧',
        'v1': "La teva feina no para, però et falta una furgoneta per moure eines i material cada dia? 🔧\n\nA AVIS tens furgonetes preparades per al dia a dia professional: espai per a tot l'equip de feina i llibertat per llogar-la només quan la necessitis.\n\nSense vincular-te a llarg termini, sense complicacions." + CIERRE,
        'v2': "Quan la feina s'acumula, no tens temps per esperar un vehicle. 🔧\n\nAmb AVIS, reserves la furgoneta que et fa falta per a la teva feina i la tens llesta quan la necessites, pels dies que calgui.\n\nMaterial, eines i equip, tot a punt per sortir a treballar." + CIERRE,
        'v3': "Un dia de feina carregat no hauria de dependre de si el teu vehicle té prou espai. 🔧\n\nA AVIS lloguem furgonetes per a autònoms i professionals que necessiten moure material sense limitacions, pel temps exacte que els cal." + CIERRE,
    },
    96: {  # Spaceclass - passatgers
        'titol': 'Furgoneta Spaceclass 🏔️',
        'v1': "Sou un grup i el cotxe se us queda petit per a la propera escapada? 🏔️\n\nLa furgoneta Spaceclass d'AVIS té espai per a tothom i per a tot l'equipatge de l'aventura.\n\nReserva-la pels dies del viatge i comenceu-lo tots junts, sense haver d'agafar dos cotxes." + CIERRE,
        'v2': "Quantes vegades heu hagut de deixar algú (o alguna cosa) a casa perquè no hi cabíeu tots? 🏔️\n\nAmb la Spaceclass d'AVIS, el grup i tot el material hi caben sense problemes. Ideal per a escapades a la muntanya o sortides llargues.\n\nLa demanes pels dies que us facin falta." + CIERRE,
        'v3': "Els millors plans en grup comencen quan hi cap tothom. 🏔️\n\nA AVIS tens la furgoneta Spaceclass per a les vostres escapades: espai per a persones i equipatge, i la flexibilitat de llogar-la només pels dies que necessiteu." + CIERRE,
    },
}

data = []
for row_num, content in rows.items():
    values = [content['titol'], content['v1'], content['v2'], content['v3']]
    data.append({
        'range': f"'{TAB}'!J{row_num}:M{row_num}",
        'values': [values],
    })

body = {'valueInputOption': 'USER_ENTERED', 'data': data}
result = service.spreadsheets().values().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
print(f"Celdas actualizadas: {result.get('totalUpdatedCells')}")
