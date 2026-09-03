# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1RHtUA5Jzu330SmL0OogU2rN7UIJ_qe3e1Wr_DO_9vs4'

# Columnas G-K = Problema, Ángulo, Hook, Desenlace, Cierre
ads = [
    {
        'Problema': 'Usa algo para el contorno pero sin rutina fija ni momento concreto',
        'Ángulo': 'Experto',
        'Hook': 'Hay un motivo por el que este pack tiene dos productos y no uno.',
        'Desenlace': 'Por las mañanas: el roll-on metálico drena físicamente el líquido acumulado y reduce la inflamación. Por las noches: el contorno penetra mientras duermes y repara la densidad de la piel. Son dos fases distintas del mismo problema. Si solo usas uno, estás viendo la mitad del resultado.',
        'Cierre': 'Pruébalo 30 días sin riesgo. Si no notas la diferencia, te devolvemos todo el dinero.',
    },
    {
        'Problema': 'He probado muchos contornos y ninguno me ha dado un resultado real',
        'Ángulo': 'Experto',
        'Hook': 'La razón por la que la mayoría de contornos no funcionan: no llegan donde está el problema.',
        'Desenlace': 'Las bolsas son líquido acumulado: el reishi del roll-on es antiinflamatorio y activa el drenaje linfático. Las ojeras son melanina y pérdida de densidad: los postbióticos marinos del contorno redensifican la dermis y reducen la pigmentación. No es magia. Es actuar exactamente donde está el origen de cada problema.',
        'Cierre': '98% reduce bolsas. 99% reduce ojeras. Estudio con 68 voluntarias, 28 días. Garantía 30 días.',
    },
    {
        'Problema': 'No sé si aplico el contorno de ojos correctamente',
        'Ángulo': 'Founder',
        'Hook': 'La mayoría aplica el contorno con los dedos. Hay un motivo por el que este lleva un roll-on metálico.',
        'Desenlace': 'El aplicador metálico frío activa el drenaje linfático con el masaje. El frío reduce la inflamación física desde el primer segundo. No es un elemento estético: es parte del mecanismo de acción. Por eso en 15 minutos ya notas el efecto. Y si lo combinas con el contorno de noche, la zona se trata desde dos frentes.',
        'Cierre': 'El pack incluye los dos. Envío gratis en 24-48h.',
    },
    {
        'Problema': 'Sigo una rutina de skincare completa pero no tengo nada específico para el contorno',
        'Ángulo': 'Founder',
        'Hook': 'Cuidas tu piel a conciencia. Pero el contorno de ojos no puede aguantar lo mismo que el resto de la cara.',
        'Desenlace': 'La piel del contorno tiene 0,5mm de grosor frente a los 2mm del resto de la cara. Los activos de las cremas normales son demasiado pesados para esa zona. Necesita concentraciones distintas, ingredientes específicos y un aplicador que no estire ni agreda. Por eso existe este pack.',
        'Cierre': 'Dos productos formulados exclusivamente para esa zona. Garantía 30 días.',
    },
    {
        'Problema': 'Creo que mis ojeras son de familia y que no hay nada que pueda hacer',
        'Ángulo': 'Experto',
        'Hook': 'Me decían que mis ojeras eran de familia. Resultó que nunca había usado el producto que actúa donde está el origen.',
        'Desenlace': 'Las ojeras genéticas existen. Pero la mayoría tienen una causa tratable: melanina superficial, mala circulación o pérdida de densidad. Los postbióticos marinos actúan sobre esas tres causas. No es que no tengas solución. Es que los productos que habías probado no llegaban hasta allí.',
        'Cierre': '30 días para comprobarlo tú misma. Si no notas diferencia, te devolvemos todo.',
    },
    {
        'Problema': 'No me creo las promesas de los cosméticos, ya me han decepcionado antes',
        'Ángulo': 'Experto',
        'Hook': '98% reduce bolsas. 99% reduce ojeras. No son promesas: son datos de un estudio independiente con 68 voluntarias.',
        'Desenlace': 'Los estudios cosméticos independientes son caros. Pocas marcas los hacen porque requieren comprometerse con el resultado antes de salir al mercado. Los hicimos porque necesitábamos saber que funcionaba antes de decírtelo. 68 voluntarias, 45-65 años, 28 días. Los resultados: medibles y replicables.',
        'Cierre': 'Pruébalo con la misma garantía que nosotras nos dimos: 30 días sin riesgo.',
    },
    {
        'Problema': 'Llevo años gastando en corrector para tapar lo que no puedo tratar',
        'Ángulo': 'Founder',
        'Hook': '¿Cuánto llevas comprando corrector para las ojeras? ¿Y cuánto tiempo llevas tratándolas?',
        'Desenlace': 'El corrector tapa. A las 4 horas, la ojera vuelve. Al día siguiente, empiezas de cero. El contorno de ojos actúa sobre la melanina y la densidad de esa piel. No es un resultado de un día: es un cambio real en la estructura de la zona. A las 4 semanas, el corrector te hace menos falta.',
        'Cierre': 'Deja de tapar. Empieza a tratar. 30 días de garantía total.',
    },
    {
        'Problema': 'Quiero los dos productos pero me parece caro comprarlos por separado',
        'Ángulo': 'Founder',
        'Hook': 'Roll-on más contorno por separado: 89,98€. Pack Essential Eyes: 79,99€. Y juntos funcionan mejor que cada uno solo.',
        'Desenlace': 'No es solo el precio. El roll-on y el contorno están diseñados para trabajar en secuencia: por la mañana activas el drenaje, por la noche reparas en profundidad. El resultado conjunto es mayor que la suma de los dos por separado. El pack no es un descuento: es la manera correcta de usar los dos.',
        'Cierre': 'Ahorra 10€ y 4 semanas de dudas. Garantía 30 días.',
    },
    {
        'Problema': 'A partir de los 35 noto que mi mirada ha cambiado y lo que usaba antes ya no funciona',
        'Ángulo': 'Experto',
        'Hook': 'A partir de los 35, el contorno de ojos necesita más que una crema hidratante. Hay un motivo biológico para eso.',
        'Desenlace': 'Con los años, la piel del contorno pierde colágeno más rápido que el resto de la cara. La microcirculación empeora. Los activos de las cremas normales ya no penetran igual. Los postbióticos marinos redensifican, el reishi reduce la inflamación acumulada y el aceite de aguacate trabaja sobre la melanina. Específicamente formulado para lo que le pasa a esa zona con el tiempo.',
        'Cierre': 'El momento de empezar es ahora. Garantía 30 días.',
    },
    {
        'Problema': 'Busco un regalo de belleza que sea útil de verdad, no algo que acabe en un cajón',
        'Ángulo': 'Founder',
        'Hook': 'Si buscas un regalo de belleza que realmente se use, este es el único que puedo recomendarte con seguridad.',
        'Desenlace': 'No es un perfume que se quede en el cajón. No es un facial que dure un día. Es una rutina de dos pasos para el contorno que da resultados visibles desde la primera semana. +128.000 clientas lo usan. Beauty Shortlist Award 2026. Y si no encanta, garantía total 30 días.',
        'Cierre': 'Envío gratis en 24-48h. Packaging cuidado. Sin riesgo.',
    },
]

# Construir valores para G90:K99 (10 filas, columnas G-K)
values = [
    [ad['Problema'], ad['Ángulo'], ad['Hook'], ad['Desenlace'], ad['Cierre']]
    for ad in ads
]

result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='G90:K99',
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

print(f"Celdas actualizadas: {result.get('updatedCells')}")
print(f"Rango actualizado: {result.get('updatedRange')}")
print("✓ 10 propuestas de vídeo escritas en G90:K99")
