# -*- coding: utf-8 -*-
import json
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

PAIN_SOBREPESO = 'No sé cuánto pienso está comiendo realmente ni si es la cantidad correcta.'
PAIN_NUTRICION = 'Me preocupa que algo natural no cubra todo lo que mi gato necesita.'
PAIN_PRECIO = 'Me pregunto si vale la pena pagar más por algo natural.'

ads = [
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_SOBREPESO,
         Hook='¿Le sirves la comida a ojo sin saber si es la ración correcta?',
         Desenlace='Servir a ojo hace fácil pasarse sin darte cuenta, sobre todo con el pienso a libre disposición. Food for Joe calcula la ración exacta según el peso, la edad y la actividad de tu gato, así que sabes justo cuánto necesita cada día.',
         Cierre='Calcula la ración exacta de tu gato con el quiz.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Veterinario', Problema=PAIN_SOBREPESO,
         Hook='¿Tu gato tiene sobrepeso y no sabes si es por las raciones?',
         Desenlace='El sobrepeso felino está muy ligado a raciones sin control, algo habitual cuando el pienso está siempre disponible. Con una ración calculada a su peso real, es más fácil que mantenga un peso saludable sin pasar hambre.',
         Cierre='Descubre la ración pensada para el peso de tu gato.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_SOBREPESO,
         Hook='¿Dejas el comedero siempre lleno sin controlar cuánto come?',
         Desenlace='Con el comedero siempre lleno es casi imposible saber cuánto come tu gato realmente. Food for Joe llega en raciones ya medidas, pensadas para su peso y actividad, sin que tengas que calcular nada.',
         Cierre='Recibe raciones ya calculadas para tu gato.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Testimonio', Problema=PAIN_SOBREPESO,
         Hook='¿Te preocupa que tu gato esté comiendo de más sin que te des cuenta?',
         Desenlace='Sin una ración de referencia, es fácil que un gato coma más de lo que necesita día tras día. Con el plan personalizado de Food for Joe sabes exactamente cuánto darle, ajustado a su peso y edad.',
         Cierre='Empieza con la ración exacta de tu gato hoy mismo.'),

    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Veterinario', Problema=PAIN_NUTRICION,
         Hook='¿Te preocupa que un alimento natural no sea nutricionalmente completo?',
         Desenlace='Natural no es sinónimo de completo si no está bien formulado. Cada receta de Food for Joe la diseñan veterinarios y nutricionistas siguiendo el estándar FEDIAF, para cubrir todo lo que tu gato necesita, no solo lo que suena bien.',
         Cierre='Consulta la ficha nutricional completa de cada receta.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_NUTRICION,
         Hook="¿Dudas si lo 'natural' cumple con lo que tu gato necesita cada día?",
         Desenlace="Muchos productos usan la palabra 'natural' sin ningún respaldo nutricional detrás. Las recetas de Food for Joe cumplen el estándar FEDIAF, así que sabes que cubren sus necesidades reales, no solo la etiqueta.",
         Cierre='Revisa el respaldo nutricional antes de decidir.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona (founder)', Problema=PAIN_NUTRICION,
         Hook='¿Quieres darle algo natural pero te preocupa que le falte algo importante?',
         Desenlace='Ese miedo es razonable si el producto solo promete "ser natural" sin más. Food for Joe combina ingredientes reales con una formulación veterinaria completa, para que no tengas que elegir entre natural y completo.',
         Cierre='Descubre cómo formulamos cada receta.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Testimonio', Problema=PAIN_NUTRICION,
         Hook='¿No sabes si una dieta natural cubre todas las necesidades de tu gato?',
         Desenlace='Es una duda habitual, porque no toda comida "natural" está pensada para cubrir todos los requerimientos de un gato. Las recetas de Food for Joe sí, porque se formulan siguiendo el estándar FEDIAF desde el primer ingrediente.',
         Cierre='Comprueba tú mismo la composición completa.'),

    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_PRECIO,
         Hook='¿Te preguntas si vale la pena pagar más por una comida natural?',
         Desenlace='Ese precio extra no es solo por la etiqueta: incluye ingredientes reales, una receta formulada por veterinarios y envío con frío controlado hasta tu casa. Es lo que cuesta hacerlo bien, no un capricho.',
         Cierre='Prueba tu primera caja con 5€ de descuento con el código WELCOME5.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Veterinario', Problema=PAIN_PRECIO,
         Hook='¿Dudas si el precio extra realmente se nota en la salud de tu gato?',
         Desenlace='La diferencia está en lo que hay dentro: ingredientes identificables frente a harinas y subproductos genéricos, y una formulación pensada para cubrir sus necesidades reales. No es solo un precio más alto, es una comida distinta.',
         Cierre='Consulta el desglose de ingredientes de cada receta.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_PRECIO,
         Hook="¿Te cuesta justificar pagar más por algo que 'parece' lo mismo?",
         Desenlace='Por fuera puede parecer solo comida para gatos, pero por dentro hay una receta cocinada con ingredientes reales y formulada siguiendo el estándar FEDIAF, no una mezcla industrial genérica. Ahí está la diferencia que no se ve a simple vista.',
         Cierre='Descubre qué hay realmente detrás del precio.'),
    dict(Target='Gato', Funnel='MOFU', Ángulo='Problema→Solución', Tipo='Persona', Problema=PAIN_PRECIO,
         Hook='¿Piensas que la comida natural es un lujo que no puedes permitirte?',
         Desenlace='No tiene por qué serlo: puedes probar tu primera caja a un precio reducido gracias al código de bienvenida, y decidir después si el cambio compensa para tu gato.',
         Cierre='Prueba tu primera caja con el código WELCOME5.'),
]

assert len(ads) == 12, len(ads)

rows = []
for ad in ads:
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

result = service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f'{TAB}!A:A',
    valueInputOption='USER_ENTERED',
    insertDataOption='INSERT_ROWS',
    body={'values': rows}
).execute()

print('Updated range:', result.get('updates', {}).get('updatedRange'))
