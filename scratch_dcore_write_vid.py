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

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"'{SHEET_TAB}'!3:3"
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)
print("Headers:", headers)

base = {'Negocio': 'B2B', 'Target': 'Chalets', 'Utilizado': False,
        'Cierre': '¡Infórmate gratis rellenando el formulario!'}

ads = [
    {**base, 'Problema': 'Imprevistos estructurales / instalaciones antiguas / humedades', 'Ángulo': 'Problema',
     'Hook': 'En chalets con años es habitual encontrar imprevistos: humedades, instalaciones antiguas o problemas estructurales. En Dcore evaluamos tu chalet antes de presupuestar para que no haya sobrecostes por sorpresas. Enseñar un ejemplo real de imprevisto detectado.'},

    {**base, 'Problema': 'Materiales y acabados de alta gama a la altura de un chalet premium', 'Ángulo': 'Autoridad',
     'Hook': 'En un chalet de alto nivel, cada acabado cuenta. Trabajamos solo con materiales y acabados de alta gama, los mismos que exigiríamos en nuestra propia reforma. Mostrar detalle de acabados premium.'},

    {**base, 'Problema': 'Necesidad de especialización en reformas de chalets de alto nivel', 'Ángulo': 'Autoridad',
     'Hook': 'Llevamos más de 20 años y 800 proyectos reformando chalets de alto nivel en Madrid. Conocemos los materiales, acabados y estándares que exige este tipo de vivienda.'},

    {**base, 'Problema': 'Equipo dedicado (arquitecto + interiorista + jefe de obra)', 'Ángulo': 'Confianza',
     'Hook': 'La mayoría de empresas subcontratan cada fase de tu chalet a terceros. En Dcore tenemos constructora propia: arquitecto, interiorista y jefe de obra dedicados en exclusiva a tu proyecto.'},

    {**base, 'Problema': 'Precio cerrado incluso en proyectos grandes', 'Ángulo': 'Autoridad',
     'Hook': 'Los proyectos grandes tienen más partidas y más riesgo de desviación. En Dcore cerramos el presupuesto de tu chalet por contrato, sin importar el tamaño. Enseñar un ejemplo de presupuesto desglosado.'},

    {**base, 'Problema': 'Seguimiento en tiempo real vía app', 'Ángulo': 'Problema',
     'Hook': 'La mayoría de empresas te dan una fecha de inicio y una de fin, y en medio, silencio. En Dcore ves el avance de tu chalet desde el móvil, con fotos actualizadas. Grabación de pantalla de la app.'},

    {**base, 'Problema': 'Chalet heredado o de segunda mano, antiguo, sin actualizar', 'Ángulo': 'Necesidad',
     'Hook': 'Las viviendas heredadas o antiguas suelen tener distribuciones que ya no encajan y sistemas obsoletos. En Dcore hacemos la reforma integral de tu chalet, de principio a fin. Mostrar antes/después.'},

    {**base, 'Problema': 'Compra reciente, reformar antes de mudarse', 'Ángulo': 'Problema',
     'Hook': 'Entre la compra y la mudanza hay una reforma completa por gestionar: diseño, licencias, obra y acabados. En Dcore nos encargamos de todo para que llegues a vivir a un chalet ya terminado.'},

    {**base, 'Problema': 'Obra de chalet más larga y compleja, riesgo de que se alargue', 'Ángulo': 'Autoridad',
     'Hook': 'Cuanto más grande el proyecto, más fácil que los plazos se disparen sin planificación técnica. Dcore lleva más de 800 proyectos entregados en el plazo pactado, con penalización por contrato si no se cumple.'},
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
    range=f"'{SHEET_TAB}'!A:A",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"Escritas {len(rows)} filas en la pestaña '{SHEET_TAB}'.")
