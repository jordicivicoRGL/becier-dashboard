# -*- coding: utf-8 -*-
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k"
TAB = "Copies"


def get_service():
    token_path = os.path.join(os.path.dirname(__file__), "credentials", "token.json")
    secret_path = os.path.join(os.path.dirname(__file__), "credentials", "client_secret.json")
    with open(token_path) as f:
        token_data = json.load(f)
    with open(secret_path) as f:
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


def texto(parrafos):
    return "\n\n".join(parrafos)


CTA_A = 'Haz clic en "Cotizar", rellena el formulario y te contactamos sin compromiso.'
CTA_B = 'Haz clic en "Cotizar", cuéntanos tu proyecto en el formulario y te llamamos.'
CTA_C = 'Haz clic en "Cotizar" y rellena el formulario: te contactamos sin compromiso.'
CTA_D = 'Haz clic en "Cotizar", completa el formulario y nos ponemos en contacto contigo.'

# ---------------- VIDEO 1: Reforma dos veces ----------------
v1_titulos = [
    "¿Vas a reformar tu chalet dos veces? 🏡",
    "¿Reformas tu chalet o lo arreglas dos veces? 🔑",
    "Todo cerrado antes de obra 🔒",
    "Bien hecha a la primera ✅",
]
v1_textos = [
    texto([
        "Muchos propietarios en Madrid reforman su chalet dos veces sin querer. 😬",
        "Se enamoran de un chalet, invierten una fortuna y acaban con espacios que "
        'no encajan, decisiones improvisadas y esa sensación de "esto no era lo '
        'que quería".',
        "En DCORE hacemos reformas integrales de chalets en Madrid, con diseño, "
        "materiales y distribución cerrados antes de tocar un solo muro.",
        CTA_A,
    ]),
    texto([
        "En DCORE diseñamos, decidimos materiales y cerramos la distribución "
        "antes de que empiece la obra, así no rehacemos nada ni improvisamos "
        "nada.",
        "Arquitecto, interiorista y jefe de obra trabajan coordinados por un "
        "project manager que lleva tu proyecto de principio a fin, sin que "
        "tengas que hacer de intermediario entre nadie.",
        "Reformas integrales de chalets en Madrid, con presupuesto fijo y un "
        "único equipo.",
        CTA_B,
    ]),
    texto([
        "Diseño, materiales y distribución: todo decidido antes de tocar un solo "
        "muro de tu chalet.",
        'Nada de "ya lo vemos sobre la marcha". En DCORE cerramos cada detalle '
        "con presupuesto fijo y un equipo propio: arquitecto, interiorista y "
        "jefe de obra.",
        "Reformas integrales de chalets en Madrid, sin depender de la "
        "improvisación de nadie.",
        CTA_C,
    ]),
    texto([
        "Reforma tu chalet una sola vez, y que sea la definitiva.",
        "En DCORE diseñamos, presupuestamos y ejecutamos con un único equipo, sin "
        "decisiones improvisadas ni sobrecostes de última hora que te obliguen a "
        "volver a empezar.",
        "Reformas integrales de chalets en Madrid capital y alrededores.",
        CTA_D,
    ]),
]

# ---------------- VIDEO 2: Verano piscina ----------------
v2_titulos = [
    "¿Reformar significa renunciar al verano? ☀️",
    "¿Y si tu chalet se reforma solo? 🏡",
    "Un equipo, cero gestiones 🔑",
    "Reforma, tú disfruta 🍹",
]
v2_textos = [
    texto([
        "Muchos propietarios posponen la reforma de su chalet por miedo a perder "
        "el verano. 🏊",
        "Mientras tú disfrutas de la piscina, en DCORE gestionamos arquitecto, "
        "interiorista y jefe de obra para que no tengas que estar pendiente de "
        "nada.",
        "Reformas integrales de chalets en Madrid, con presupuesto cerrado y "
        "materiales de máxima calidad.",
        CTA_A,
    ]),
    texto([
        "Pasas el verano junto a la piscina. ☀️ Tu chalet se transforma sin que "
        "tengas que mover un dedo.",
        "En DCORE nos encargamos de arquitectura, interiorismo y obra con un "
        "único equipo y presupuesto cerrado.",
        "Reformas integrales de chalets en Madrid, para que tú solo tengas que "
        "disfrutar.",
        CTA_B,
    ]),
    texto([
        "Arquitecto, interiorista y jefe de obra: un único equipo para toda tu "
        "reforma, sin que muevas un dedo.",
        "En DCORE gestionamos cada fase con presupuesto cerrado y materiales de "
        "alta calidad, para que sigas de vacaciones mientras avanza la obra.",
        "Reformas integrales de chalets en Madrid capital y alrededores.",
        CTA_C,
    ]),
    texto([
        "Tu chalet se reforma este verano sin que tengas que ocuparte de nada: "
        "nosotros nos encargamos de todo.",
        "Diseño, obra y materiales bajo un mismo equipo, con presupuesto cerrado.",
        "Reformas integrales de chalets en Madrid.",
        CTA_D,
    ]),
]

# ---------------- VIDEO 3: Chalet de 2M ----------------
v3_titulos = [
    "¿Tu chalet merece más que una reforma genérica? 🏛️",
    "¿Arquitectura o solo decoración? 🏆",
    "20 años de arquitectura en Madrid 🏆",
    "Un proyecto, no una obra 🔑",
]
v3_textos = [
    texto([
        "Un chalet de dos millones de euros no se reforma como un piso "
        "cualquiera.",
        "Y sin embargo, muchos estudios lo hacen: la misma cocina bonita, el "
        "mismo salón más grande, cero visión de conjunto.",
        "En DCORE hacemos reformas integrales de chalets en Madrid, estudiando "
        "cómo entra la luz, cómo se relaciona la casa con el jardín y qué "
        "materiales seguirán siendo elegantes dentro de veinte años.",
        CTA_A,
    ]),
    texto([
        "En una vivienda excepcional, la diferencia entre arquitectura y "
        "decoración se nota.",
        "Llevamos años diseñando reformas integrales de chalets en Madrid donde "
        "cada decisión importa: luz, materiales, distribución y relación con el "
        "jardín como parte de un mismo proyecto.",
        CTA_B,
    ]),
    texto([
        "20 años diseñando reformas integrales de chalets en Madrid, para "
        "viviendas que no admiten soluciones genéricas.",
        "Estudiamos luz, materiales y distribución como un proyecto único, no "
        "como una suma de habitaciones desconectadas entre sí.",
        CTA_C,
    ]),
    texto([
        "Tu chalet merece un proyecto de arquitectura, no una reforma más de una "
        "lista.",
        "En DCORE diseñamos cada vivienda en Madrid como un conjunto: luz, "
        "jardín, materiales y distribución trabajados juntos, no por separado.",
        CTA_D,
    ]),
]

rows = [
    [],
    ["", "", "Variante 1", "Variante 2", "Variante 3", "Variante 4", "Variante 5"],
    ["", "Video 1: Reforma dos veces — Títulos", *v1_titulos],
    ["", "Video 1: Reforma dos veces — Textos", *v1_textos],
    ["", "Video 2: Verano piscina — Títulos", *v2_titulos],
    ["", "Video 2: Verano piscina — Textos", *v2_textos],
    ["", "Video 3: Chalet de 2 M — Títulos", *v3_titulos],
    ["", "Video 3: Chalet de 2 M — Textos", *v3_textos],
]

service = get_service()
result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{TAB}'!A1:G8",
    valueInputOption="USER_ENTERED",
    body={"values": rows},
).execute()
print(json.dumps(result, indent=2, ensure_ascii=False))
