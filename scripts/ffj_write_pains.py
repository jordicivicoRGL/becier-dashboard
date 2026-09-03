# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'

new_rows = [
    # TOFU - Sintomas fisicos
    ['TOFU', 'Sintomas fisicos', 'Veterinario', '', 'Otitis recurrente sin causa aparente'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Pata manchada de naranja/marron por lamido cronico'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Mal aliento cronico que no mejora con nada'],
    ['TOFU', 'Sintomas fisicos', 'Veterinario', '', 'Dermatitis atopica diagnosticada'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Heces blandas o con mucosidad de forma habitual'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Placa dental excesiva para su edad'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Caspa y piel seca sin solucion'],
    ['TOFU', 'Sintomas fisicos', 'Veterinario', '', 'Intolerancia alimentaria diagnosticada'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Flatulencias frecuentes y olor insoportable'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Ojos con muchas leganias de forma cronica'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'Come muy rapido, ansiedad con la comida'],
    ['TOFU', 'Sintomas fisicos', 'Persona', '', 'El perro no quiere comer / rechaza el pienso'],
    ['TOFU', 'Sintomas fisicos', 'Veterinario', '', 'Musculos poco desarrollados para su raza/edad'],
    # TOFU - Sintomas emocionales/conducta
    ['TOFU', 'Sintomas emocionales/conducta', 'Persona', '', 'Ansiedad elevada sin causa aparente'],
    ['TOFU', 'Sintomas emocionales/conducta', 'Persona', '', 'El perro busca comida en basura y suelo constantemente'],
    ['TOFU', 'Sintomas emocionales/conducta', 'Persona', '', 'Cambios de humor inexplicables, caracter irritable'],
    # TOFU - Desconocimiento
    ['TOFU', 'Desconocimiento', 'Veterinario', '', 'El pienso premium puede seguir siendo ultra-procesado'],
    ['TOFU', 'Desconocimiento', 'Veterinario', '', 'Diferencia entre natural en etiqueta y comida realmente natural'],
    ['TOFU', 'Desconocimiento', 'Persona', '', 'No saber leer el etiquetado de los ingredientes del pienso'],
    ['TOFU', 'Desconocimiento', 'Veterinario', '', 'Lo que es realmente una harina de carne'],
    ['TOFU', 'Desconocimiento', 'Persona', '', 'Los conservantes artificiales que lleva el pienso sin saberlo'],
    # TOFU - Mitos/creencias
    ['TOFU', 'Mitos/creencias', 'Persona', '', 'Mi veterinario me recomienda ese pienso, asi que es bueno'],
    ['TOFU', 'Mitos/creencias', 'Persona', '', 'La comida casera no es equilibrada para perros'],
    ['TOFU', 'Mitos/creencias', 'Veterinario', '', 'El pienso de alta gama cubre todas las necesidades'],
    # TOFU - Longevidad
    ['TOFU', 'Longevidad', 'Persona', '', 'Los perros viven menos de lo que deberian segun estudios recientes'],
    ['TOFU', 'Longevidad', 'Veterinario', '', 'Enfermedades cronicas (cancer, ERC, diabetes) aumentan en perros jovenes'],
    ['TOFU', 'Longevidad', 'Persona', '', 'Querer mas anyos de vida con calidad junto a su perro'],
    # MOFU - Culpa/responsabilidad
    ['MOFU', 'Culpa/responsabilidad', 'Persona', '', 'Sentirse mal tras enterarse de lo que lleva el pienso que da a su perro'],
    ['MOFU', 'Culpa/responsabilidad', 'Testimonio UGC', '', 'El veterinario le dijo que cambiara la dieta y no sabe como'],
    ['MOFU', 'Culpa/responsabilidad', 'Persona', '', 'Llevar anyos dandole pienso pensando que hacia lo correcto'],
    ['MOFU', 'Culpa/responsabilidad', 'Persona', '', 'Haber ignorado los sintomas del perro por mucho tiempo'],
    # MOFU - Comparativa
    ['MOFU', 'Comparativa', 'Veterinario', '', 'Pienso premium vs comida natural cocinada: diferencia real de nutrientes'],
    ['MOFU', 'Comparativa', 'Persona', '', 'Cuanto cuesta realmente alimentar bien a un perro al dia'],
    ['MOFU', 'Comparativa', 'Testimonio UGC', '', 'Ya probe comida casera pero no sabia si la dieta era completa'],
    ['MOFU', 'Comparativa', 'Veterinario', '', 'Por que el pienso seco no puede replicar la biodisponibilidad de la comida cocinada'],
    # MOFU - Prueba social
    ['MOFU', 'Prueba social', 'Testimonio UGC', '', 'Esceptico que cambio y vio resultados en 3 semanas'],
    ['MOFU', 'Prueba social', 'Testimonio UGC', '', 'Perro con alergias cronicas que mejoro al cambiar la alimentacion'],
    ['MOFU', 'Prueba social', 'Testimonio UGC', '', 'Duenyo que noto el cambio de energia en su perro senior'],
    ['MOFU', 'Prueba social', 'Testimonio UGC', '', 'Veterinario que empezo a recomendar comida natural tras ver resultados'],
    # MOFU - Miedo/friccion
    ['MOFU', 'Miedo/friccion', 'Persona', '', 'Miedo a que la transicion sea dificil o provoque diarrea'],
    ['MOFU', 'Miedo/friccion', 'Persona', '', 'Mi perro es muy selectivo, no se si lo comera'],
    ['MOFU', 'Miedo/friccion', 'Persona', '', 'No saber cuanto darle ni si la racion es correcta'],
    ['MOFU', 'Miedo/friccion', 'Persona', '', 'El precio parece caro al principio sin ver el valor completo'],
    ['MOFU', 'Miedo/friccion', 'Veterinario', '', 'Como hacer la transicion sin estresar al perro ni al duenyo'],
    ['MOFU', 'Miedo/friccion', 'Persona', '', 'Ya intente el cambio una vez y fue un desastre (mal asesorado)'],
    # BOFU - Miedo/friccion especifico
    ['BOFU', 'Miedo/friccion', 'Persona', '', 'Duda sobre la conservacion: como gestionar la comida congelada'],
    ['BOFU', 'Miedo/friccion', 'Persona', '', 'Incertidumbre sobre la logistica de entrega (cadena de frio)'],
    ['BOFU', 'Miedo/friccion', 'Persona', '', 'Que pasa si no le gusta? Puedo devolver el pedido?'],
    # BOFU - Producto
    ['BOFU', 'Producto', 'Veterinario', '', 'Como esta formulado el plan segun raza, peso y condicion'],
    ['BOFU', 'Producto', 'Persona', '', 'El quiz y como funciona la personalizacion de la dieta'],
    ['BOFU', 'Producto', 'Persona', '', 'Que ingredientes reales lleva cada receta de FFJ'],
    ['BOFU', 'Producto', 'Persona', '', 'Como llega el pedido y como se gestiona el congelado en casa'],
    # BOFU - Urgencia/resultado
    ['BOFU', 'Urgencia/resultado', 'Testimonio UGC', '', 'Cuanto tardan en verse los primeros cambios visibles'],
    ['BOFU', 'Urgencia/resultado', 'Persona', '', 'Lo que pierde cada semana que sigue con el pienso actual'],
    ['BOFU', 'Urgencia/resultado', 'Veterinario', '', 'Por que empezar antes marca la diferencia a largo plazo'],
]

result = service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='VID!A:E',
    valueInputOption='USER_ENTERED',
    body={'values': new_rows}
).execute()

updated = result.get('updates', {}).get('updatedRows', 0)
print(f'Filas escritas: {updated}')
print(f'Rango actualizado: {result.get("updates", {}).get("updatedRange", "")}')
