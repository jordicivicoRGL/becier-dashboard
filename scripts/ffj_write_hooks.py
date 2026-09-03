# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'

# (fila, hook)
hooks = [
    (4,  '¿Sabes realmente qué estás dándole de comer a tu perro cada día?'),
    (5,  '¿Tu perro hace caca blanda o con mucosidad y no sabes por qué?'),
    (6,  '¿Tu perro se rasca constantemente y no encuentras la causa?'),
    (7,  '¿Tu perro pierde pelo de forma excesiva y no es época de muda?'),
    (8,  '¿Tu perro sube y baja de peso aunque no cambies su alimentación?'),
    (9,  '¿Tu perro cojea o le cuesta levantarse por las mañanas?'),
    (10, '¿El pelo de tu perro no brilla aunque lo cuides mucho?'),
    (11, '¿Tu perro está apagado, sin ganas de jugar, sin energía?'),
    (12, '¿Cuántos años de vida sana le quedan a tu perro con lo que come hoy?'),
    (13, '¿Sabes leer realmente lo que pone en la etiqueta del pienso de tu perro?'),
    (14, '¿Estás seguro de que el pienso que le das es lo mejor que puedes darle?'),
    (15, '¿Sabes qué diferencia hay entre comida natural para perros y pienso?'),
    (20, '¿Cuánto tiempo pierdes cada semana preparando la comida de tu perro?'),
    (21, '¿Tu perro se rasca sin parar, se lame las patas o tiene la piel irritada?'),
    (22, '¿A tu perro le han diagnosticado intolerancia alimentaria y no sabes qué darle?'),
    (23, '¿Tu perro tiene dermatitis y ya has probado de todo sin resultados?'),
    (24, '¿Tu perro tiene otitis de forma recurrente y no encuentras la causa?'),
    (25, '¿Las patas de tu perro tienen manchas naranjas de tanto lamerse?'),
    (26, '¿Tu perro tiene mal aliento crónico aunque le cuides la boca?'),
    (27, '¿Tu perro hace caca blanda de forma habitual y no sabes por qué?'),
    (28, '¿Tu perro tiene mucho sarro para la edad que tiene?'),
    (29, '¿Tu perro tiene caspa y piel seca que no mejora con nada?'),
    (30, '¿Tu perro tiene gases constantemente y el olor es insoportable?'),
    (31, '¿Tu perro tiene legañas todos los días aunque estés muy pendiente?'),
    (32, '¿Tu perro no quiere comer y tienes que insistirle en cada comida?'),
    (33, '¿Tu perro busca comida en la basura aunque acabe de comer?'),
    (34, '¿Sabes que el pienso premium que le das puede seguir siendo ultraprocesado?'),
    (35, '¿Sabes la diferencia entre un alimento "natural" y uno realmente natural?'),
    (36, '¿Confías en el pienso solo porque tu veterinario te lo recomendó?'),
    (37, '¿Crees que la comida casera para perros no es nutricionalmente completa?'),
    (38, '¿Piensas que el pienso premium cubre todas las necesidades de tu perro?'),
    (39, '¿Sabías que los perros viven menos años de los que deberían?'),
    (40, '¿Sabías que el cáncer, la diabetes y la ERC en perros están aumentando?'),
    (41, '¿Qué harías si pudieras tener 3 años más con tu perro en perfecto estado?'),
    (42, '¿Cuánto tiempo llevas dándole algo a tu perro sin saber exactamente qué contiene?'),
    (43, '¿Llevas años pensando que el pienso era la mejor opción para tu perro?'),
    (44, '¿Tu perro lleva tiempo dándote señales que no sabías cómo interpretar?'),
    (45, '¿Sabes la diferencia real de nutrientes entre el pienso premium y la comida natural?'),
    (46, '¿Cuánto crees que cuesta dar de comer bien a tu perro cada día?'),
    (47, '¿Probaste a hacerle comida casera pero no tenías claro si la dieta era completa?'),
    (48, '¿Tienes un perro con alergias crónicas y ya no sabes qué más probar?'),
    (49, '¿Notarías la diferencia si tu perro mayor volviera a tener energía de cachorro?'),
    (50, '¿Crees que la comida natural para perros es demasiado cara?'),
    (51, '¿Sabes exactamente qué come tu perro según su raza, peso y edad?'),
    (52, '¿En cuántas preguntas podrías saber exactamente qué necesita tu perro?'),
    (53, '¿Sabes qué ingredientes reales tiene lo que le das de comer a tu perro?'),
    (54, '¿Cómo llega la comida natural congelada a tu casa y cómo la gestionas?'),
    (55, '¿Cuánto tiempo más vas a esperar para cambiar lo que come tu perro?'),
]

data = [
    {'range': f'VID!F{fila}', 'values': [[hook]]}
    for fila, hook in hooks
]

result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
).execute()

print(f"Celdas actualizadas: {result.get('totalUpdatedCells', 0)}")
