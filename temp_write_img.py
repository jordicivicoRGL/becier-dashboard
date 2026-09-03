# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1RHtUA5Jzu330SmL0OogU2rN7UIJ_qe3e1Wr_DO_9vs4'
TAB = 'IMG'

# Columnas D-H: Foto, Ángulo, Problema, Headline, Subline
ads = [
    {
        'Foto': 'Pack',
        'Angulo': 'Doble mecanismo',
        'Problema': 'Ojeras y bolsas sin solución real',
        'Headline': 'Dos productos. Dos momentos. Una mirada completamente distinta.',
        'Subline': '• Roll-on por la mañana: drenaje inmediato\n• Contorno por la noche: reparación en profundidad\n• Resultado visible en 28 días\n• Garantía 30 días sin riesgo',
    },
    {
        'Foto': 'Persona',
        'Angulo': 'Comparativo',
        'Problema': 'Lleva años usando corrector sin tratar las ojeras',
        'Headline': 'Llevas años tapando. Esto trata.',
        'Subline': '• El corrector cubre las ojeras unas horas\n• El contorno actúa sobre la melanina y la densidad\n• 99% reduce sombra de ojeras en 28 días\n• Garantía 30 días',
    },
    {
        'Foto': 'Producto',
        'Angulo': 'Dato/Estadística',
        'Problema': 'No cree en las promesas de los cosméticos',
        'Headline': '98% reduce bolsas. 99% reduce ojeras. 28 días.',
        'Subline': '• Estudio independiente con 68 voluntarias\n• 75% notó efecto lifting en 15 minutos\n• Clínicamente probado · Testado dermatológicamente\n• 30 días de garantía sin preguntas',
    },
    {
        'Foto': 'Pack',
        'Angulo': 'Ahorro',
        'Problema': 'Quiere los dos productos pero le parece caro comprarlos por separado',
        'Headline': 'Los dos juntos: 79,99€. Por separado: 89,98€.',
        'Subline': '• Roll-on antibolsas + Contorno antiojeras\n• Diseñados para trabajar en secuencia\n• Envío gratuito 24-48h\n• Garantía 30 días',
    },
    {
        'Foto': 'Persona',
        'Angulo': 'Problema → Solución',
        'Problema': 'Cree que sus ojeras son de familia y no tienen solución',
        'Headline': 'No son de familia. Son de los productos que no llegan hasta el origen.',
        'Subline': '• Los postbióticos marinos actúan sobre melanina y densidad\n• El reishi reduce la inflamación que genera bolsas\n• 99% reduce ojeras en 28 días\n• Pruébalo sin riesgo',
    },
    {
        'Foto': 'Pack',
        'Angulo': 'Ingredientes',
        'Problema': 'Quiere entender qué lleva el producto antes de comprarlo',
        'Headline': 'Reishi. Postbióticos marinos. Aceite de aguacate. Así se tratan bolsas y ojeras.',
        'Subline': '• Reishi: antiinflamatorio, activa el drenaje linfático\n• Postbióticos marinos: redensifican y reducen melanina\n• Aceite de aguacate: calma y nutre la zona del ojo\n• 99% ingredientes naturales · Cruelty-free',
    },
    {
        'Foto': 'Persona',
        'Angulo': 'Problema → Solución',
        'Problema': 'A partir de los 35 nota que su mirada cambia y lo que usaba ya no funciona',
        'Headline': 'La piel del contorno tiene 0,5mm. La del resto de la cara, 2mm. No puede aguantar lo mismo.',
        'Subline': '• Formulado específicamente para la zona del ojo\n• Activos que penetran donde las cremas normales no llegan\n• Desde la primera aplicación notas la diferencia\n• 30 días de garantía total',
    },
    {
        'Foto': 'Pack',
        'Angulo': 'Social proof',
        'Problema': 'No conoce la marca y no sabe si fiarse',
        'Headline': 'Beauty Shortlist Award 2026. Vogue. Elle. Marie Claire. +128.000 clientas.',
        'Subline': '• El premio internacional independiente de cosmética natural\n• Testado dermatológicamente\n• Clínicamente probado con 68 voluntarias\n• Garantía 30 días sin preguntas',
    },
    {
        'Foto': 'Lifestyle',
        'Angulo': 'Regalo',
        'Problema': 'Busca un regalo de belleza útil y diferente',
        'Headline': 'El regalo de belleza que realmente se usa.',
        'Subline': '• Rutina completa de contorno de ojos en 2 pasos\n• Resultados visibles desde la primera semana\n• Packaging cuidado · Envío gratis 24-48h\n• Garantía 30 días — sin riesgo para quien lo regala',
    },
    {
        'Foto': 'Persona',
        'Angulo': 'Problema → Solución',
        'Problema': 'Se levanta con la zona del ojo hinchada sin haber dormido mal',
        'Headline': 'Te levantas descansada. Tu contorno de ojos, no.',
        'Subline': '• El aplicador metálico frío drena en 15 segundos\n• El contorno repara durante la noche mientras duermes\n• 98% reduce bolsas · 99% reduce ojeras\n• Pruébalo 30 días sin riesgo',
    },
]

# Escribir en D24:H33 (fila 24 = primera libre tras el contenido existente)
values = [
    [ad['Foto'], ad['Angulo'], ad['Problema'], ad['Headline'], ad['Subline']]
    for ad in ads
]

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"'{TAB}'!D24:H33",
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

print(f"Celdas actualizadas: {result.get('updatedCells')}")
print(f"Rango: {result.get('updatedRange')}")
