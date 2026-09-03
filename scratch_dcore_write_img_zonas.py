# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
IMG_TAB = 'IMG'

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"{IMG_TAB}!1:1"
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)
print("Headers:", headers)

base = {'Campaña': 'Zonas premium Madrid', 'Formato': 'Imagen', 'Target': 'B2C',
        'Comentarios': 'Imagen de vivienda de alto standing reformada en zona premium + el texto principal y sub texto en la imagen'}

ads = [
    {**base, 'Anuncio': '32', 'Pain principal': 'Confianza y control',
     'Pain': 'Obra visible, personal sin vetar o sistemas de seguridad desactivados durante la reforma',
     'Texto principal en la imagen': 'Tu seguridad, protegida durante toda la reforma.',
     'Sub texto en la imagen': 'Equipo propio. Sin subcontratas sin control.'},

    {**base, 'Anuncio': '33', 'Pain principal': 'Confianza y control',
     'Pain': 'Obra visible, personal sin vetar o sistemas de seguridad desactivados durante la reforma',
     'Texto principal en la imagen': '¿Sabes quién entra en tu casa durante la reforma?',
     'Sub texto en la imagen': 'En Dcore, solo equipo propio de confianza.'},

    {**base, 'Anuncio': '34', 'Pain principal': 'Normativa y valor de la vivienda',
     'Pain': 'Reforma que no respeta la normativa de la urbanización',
     'Texto principal en la imagen': 'Reformas que cumplen la normativa de tu urbanización.',
     'Sub texto en la imagen': 'Evita sanciones. Evita rehacer obra.'},

    {**base, 'Anuncio': '35', 'Pain principal': 'Normativa y valor de la vivienda',
     'Pain': 'Reforma que no respeta la normativa de la urbanización',
     'Texto principal en la imagen': '¿Tu reforma cumple la normativa de tu urbanización?',
     'Sub texto en la imagen': 'En Dcore, sí. Desde el primer plano.'},

    {**base, 'Anuncio': '36', 'Pain principal': 'Normativa y valor de la vivienda',
     'Pain': 'Reforma que devalúa la vivienda frente al estándar de la zona',
     'Texto principal en la imagen': 'Una reforma a la altura, protege el valor de tu casa.',
     'Sub texto en la imagen': 'Diseño acorde al estándar de tu zona.'},

    {**base, 'Anuncio': '37', 'Pain principal': 'Confianza y control',
     'Pain': 'Delegar la reforma sin tiempo para gestionar ni margen de error',
     'Texto principal en la imagen': 'Delega tu reforma por completo, sin cometer un error.',
     'Sub texto en la imagen': 'Un equipo de expertos decide por ti.'},

    {**base, 'Anuncio': '38', 'Pain principal': 'Confianza y control',
     'Pain': 'Delegar la reforma sin tiempo para gestionar ni margen de error',
     'Texto principal en la imagen': '¿Y si un equipo de expertos decidiera por ti?',
     'Sub texto en la imagen': 'Mismo gran resultado, cero tiempo invertido.'},

    {**base, 'Anuncio': '39', 'Pain principal': 'Confianza y control',
     'Pain': 'Delegar la reforma sin tiempo para gestionar ni margen de error',
     'Texto principal en la imagen': 'Delega tu reforma sin perder el control.',
     'Sub texto en la imagen': 'Un solo interlocutor. Seguimiento constante.'},

    {**base, 'Anuncio': '40', 'Pain principal': 'Estilo de vida',
     'Pain': 'Reforma que debe estar a la altura de su entorno/círculo',
     'Texto principal en la imagen': 'Tu zona exige una reforma a la altura.',
     'Sub texto en la imagen': 'Materiales y acabados de alta gama en cada detalle.'},

    {**base, 'Anuncio': '41', 'Pain principal': 'Estilo de vida',
     'Pain': 'Reforma que debe estar a la altura de su entorno/círculo',
     'Texto principal en la imagen': '¿Tu reforma está a la altura de tu zona?',
     'Sub texto en la imagen': 'Especialistas en vivienda de alto standing en Madrid.'},

    {**base, 'Anuncio': '42', 'Pain principal': 'Estilo de vida',
     'Pain': 'Miedo a un proyecto de catálogo, quieren diseño único',
     'Texto principal en la imagen': 'Tu casa, la única con ese diseño en tu zona.',
     'Sub texto en la imagen': 'Cero catálogo. Cero repetición.'},

    {**base, 'Anuncio': '43', 'Pain principal': 'Estilo de vida',
     'Pain': 'Miedo a un proyecto de catálogo, quieren diseño único',
     'Texto principal en la imagen': '¿Y si tu casa fuera única, incluso en tu zona?',
     'Sub texto en la imagen': 'Diseño desde cero, para ti.'},

    {**base, 'Anuncio': '44', 'Pain principal': 'Calidad',
     'Pain': 'Constructoras generalistas sin trayectoria en vivienda de alto standing',
     'Texto principal en la imagen': 'No cualquier constructora está a la altura de tu casa.',
     'Sub texto en la imagen': '+20 años y 800 proyectos en vivienda de alto standing.'},
]

rows = []
for ad in ads:
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f"{IMG_TAB}!A:A",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas nuevas en IMG (Anuncio 32-44).")
