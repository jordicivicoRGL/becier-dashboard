# -*- coding: utf-8 -*-
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
TAB = 'Copies'

def get_service():
    with open('credentials/token.json', encoding='utf-8') as f:
        token_data = json.load(f)
    with open('credentials/client_secret.json', encoding='utf-8') as f:
        secret_data = json.load(f)
    web_or_installed = secret_data.get("web") or secret_data.get("installed")
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web_or_installed["client_id"],
        client_secret=web_or_installed["client_secret"],
        scopes=token_data.get("scopes"),
    )
    creds.refresh(Request())
    return build("sheets", "v4", credentials=creds)

service = get_service()

titulos_v1 = [
    "¿Y si tu reforma no tuviera sorpresas? 🏡",
    "Presupuesto cerrado, sin sobrecostes 🔒",
    "Cada partida, decidida antes de empezar 🔑",
    "Sin sobrecostes de última hora ✅",
]

textos_v1 = [
"""Reformar un chalet suele venir con sorpresas: partidas que aparecen a mitad de obra y presupuestos que se disparan sin que nadie las haya avisado.

En DCORE cerramos cada partida antes de tocar un solo muro: diseño, materiales y distribución decididos de antemano, con presupuesto fijo.

Reformas integrales de chalets en Madrid, sin sobrecostes ni sorpresas.

Haz clic en "Cotizar", rellena el formulario y te contactamos sin compromiso.""",
"""En DCORE cerramos el presupuesto de tu chalet por contrato, partida por partida, antes de empezar la obra.

Arquitecto, interiorista y jefe de obra trabajan coordinados por un único equipo, así no hay sorpresas ni facturas que no esperabas.

Reformas integrales de chalets en Madrid, con presupuesto fijo y un equipo propio.

Haz clic en "Cotizar", cuéntanos tu proyecto en el formulario y te llamamos.""",
"""Nada de "ya lo vemos sobre la marcha". En DCORE cerramos cada detalle de tu chalet antes de empezar: diseño, materiales y presupuesto por partidas.

Un único equipo propio —arquitecto, interiorista y jefe de obra— para que no tengas que hacer de intermediario entre nadie.

Reformas integrales de chalets en Madrid capital y alrededores.

Haz clic en "Cotizar" y rellena el formulario: te contactamos sin compromiso.""",
"""Reforma tu chalet una sola vez, con presupuesto cerrado de principio a fin.

En DCORE diseñamos, presupuestamos y ejecutamos con un único equipo, sin partidas ocultas ni sobrecostes que te obliguen a renegociar a mitad de obra.

Reformas integrales de chalets en Madrid capital y alrededores.

Haz clic en "Cotizar", completa el formulario y nos ponemos en contacto contigo.""",
]

titulos_v2 = [
    "Tu chalet, sin que estés pendiente 📲",
    "Sigue tu obra desde el móvil 🔑",
    "Un equipo, cero gestiones 🔑",
    "Nosotros gestionamos, tú sigues tu día a día ✅",
]

textos_v2 = [
"""Muchos propietarios evitan reformar su chalet por no querer estar todo el día pendientes de la obra.

En DCORE gestionamos arquitecto, interiorista y jefe de obra por ti, y puedes seguir el avance en tiempo real desde el móvil.

Reformas integrales de chalets en Madrid, con materiales de máxima calidad y presupuesto detallado por partidas y cerrado antes de empezar.

Haz clic en "Cotizar", rellena el formulario y te contactamos sin compromiso.""",
"""Sigue el avance de tu chalet desde el móvil, con fotos actualizadas de cada fase de la obra. 📲

En DCORE nos encargamos de arquitectura, interiorismo y obra con un único equipo.

Reformas integrales de chalets en Madrid, para que no tengas que estar encima de nadie.

Haz clic en "Cotizar", cuéntanos tu proyecto en el formulario y te llamamos.""",
"""Arquitecto, interiorista y jefe de obra: un único equipo para toda tu reforma, sin que tengas que coordinar a nadie.

En DCORE gestionamos cada fase con presupuesto cerrado y materiales de alta calidad, y puedes seguir el progreso en tiempo real.

Reformas integrales de chalets en Madrid capital y alrededores.

Haz clic en "Cotizar" y rellena el formulario: te contactamos sin compromiso.""",
"""Tu chalet se reforma sin que tengas que ocuparte de nada: nosotros nos encargamos de todo y te mantenemos informado en tiempo real.

Diseño, obra y materiales bajo un mismo equipo, con presupuesto cerrado.

Reformas integrales de chalets en Madrid.

Haz clic en "Cotizar", completa el formulario y nos ponemos en contacto contigo.""",
]

data = [
    {"range": f"'{TAB}'!H3:K3", "values": [titulos_v1]},
    {"range": f"'{TAB}'!H4:K4", "values": [textos_v1]},
    {"range": f"'{TAB}'!H5:K5", "values": [titulos_v2]},
    {"range": f"'{TAB}'!H6:K6", "values": [textos_v2]},
]

body = {"valueInputOption": "USER_ENTERED", "data": data}
result = service.spreadsheets().values().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
print("Actualizado:", result.get("totalUpdatedCells"), "celdas")
