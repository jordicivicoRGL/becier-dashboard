# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k'
SHEET_TAB = 'VID'

desenlaces = [
    # Fila 60 - Privacidad/seguridad (afirmación)
    'Durante una reforma, muchas viviendas quedan expuestas: alarmas desconectadas, personal externo sin vetar entrando y saliendo, información sensible de la casa circulando entre subcontratas. En Dcore trabajamos con equipo propio, no subcontratamos sin control, y mantenemos activos los protocolos de seguridad de tu vivienda durante toda la obra.',
    # Fila 61 - Privacidad/seguridad (pregunta)
    'La mayoría de reformas dejan la vivienda expuesta: sistemas de seguridad desactivados, personal externo sin vetar e información sensible circulando entre subcontratas. En Dcore trabajamos con equipo propio de confianza y mantenemos tu seguridad activa durante toda la obra.',
    # Fila 62 - Reforma que desentona (normativa, afirmación)
    'Muchas de estas urbanizaciones tienen normativas estrictas de la junta de compensación sobre fachadas, alturas y materiales. Una reforma que no las respeta puede acabar en sanciones o en tener que rehacer parte de la obra. En Dcore conocemos la normativa de cada zona premium de Madrid y diseñamos tu reforma para que la cumpla desde el primer plano.',
    # Fila 63 - Reforma que desentona (normativa, pregunta)
    'La normativa de estas urbanizaciones sobre fachadas, alturas y materiales es estricta y cambia de una zona a otra. En Dcore la conocemos y diseñamos tu reforma para que la cumpla desde el primer momento, evitando sanciones o tener que rehacer obra.',
    # Fila 64 - Reforma que desentona (valor de reventa)
    'En zonas de este nivel, el valor de una vivienda está ligado al estándar del entorno. Una reforma por debajo de ese nivel puede devaluar tu casa frente al resto de la zona. En Dcore diseñamos cada reforma para que esté a la altura del entorno y proteja el valor de tu inversión a futuro.',
    # Fila 65 - Cero tiempo (afirmación)
    'Un equipo de expertos —arquitecto, interiorista y jefe de obra— toma cada decisión de tu reforma con el mismo rigor que aplicaríamos a la nuestra, con control de calidad en cada fase. Así puedes delegar tu reforma por completo, sin tener que estar pendiente ni asumir el riesgo de un error.',
    # Fila 66 - Cero tiempo (pregunta combinada)
    'Cuando delegas tu reforma en un equipo de expertos, cada decisión se toma con el mismo criterio que aplicaríamos a nuestra propia casa, sin que tengas que estar encima del proyecto. Así ganas tiempo sin renunciar al mejor resultado.',
    # Fila 67 - Cero tiempo (pregunta control)
    'En Dcore delegas la gestión completa de tu reforma en un equipo de expertos, pero mantienes el control a través de un único interlocutor y seguimiento constante del proyecto. Así ganas tiempo sin renunciar a saber en todo momento cómo va tu reforma.',
    # Fila 68 - Estar a la altura (afirmación)
    'En zonas de este nivel, el resultado de tu reforma se compara con el de las viviendas de tu entorno. En Dcore diseñamos cada proyecto para que esté al nivel de las mejores viviendas de tu zona, con materiales y acabados de alta gama en cada detalle.',
    # Fila 69 - Estar a la altura (pregunta)
    'En Dcore somos especialistas en reformas de vivienda de alto standing en Madrid. Diseñamos cada proyecto para que esté al nivel de las mejores viviendas de tu zona, con materiales y acabados de alta gama en cada detalle.',
    # Fila 70 - Quieren algo único (pregunta 1)
    'Cada reforma que hacemos en Dcore se diseña desde cero para la vivienda y las necesidades de cada cliente, sin repetir materiales ni diseños de catálogo. Así tu casa no se parece a ninguna otra reforma de tu zona.',
    # Fila 71 - Quieren algo único (pregunta 2)
    'En Dcore no trabajamos con catálogos ni diseños repetidos: cada proyecto se piensa desde cero para la vivienda y la forma de vivir de cada cliente. Así, aunque vivas en una zona donde todo parece igual de exclusivo, tu casa es la única con ese diseño.',
    # Fila 72 - Constructoras generalistas
    'Llevamos más de 20 años y 800 proyectos reformando viviendas de alto standing en Madrid. Conocemos los materiales, acabados y estándares que exige este tipo de vivienda, algo que una constructora generalista no puede ofrecer.',
]

rows = [[d] for d in desenlaces]

service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{SHEET_TAB}'!G60:G72",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritos {len(rows)} Desenlaces en '{SHEET_TAB}'!G60:G72.")
