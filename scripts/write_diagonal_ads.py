# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1CD-CqKdVD6q7J2tTLwZ-QovrDNobomIp_jvmR63sVH8'

# Primero: borrar las 20 filas incorrectas (filas 16-35, indice 0 = fila 1)
# Las filas de datos empiezan en indice 15 (fila 16) hasta indice 34 (fila 35)
sheet_meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
img_sheet_id = None
for s in sheet_meta['sheets']:
    if s['properties']['title'] == 'IMG':
        img_sheet_id = s['properties']['sheetId']
        break

service.spreadsheets().batchUpdate(
    spreadsheetId=SHEET_ID,
    body={
        'requests': [{
            'deleteDimension': {
                'range': {
                    'sheetId': img_sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': 15,  # fila 16 (0-indexed)
                    'endIndex': 35     # fila 35 (0-indexed, no incluido)
                }
            }
        }]
    }
).execute()
print('Filas incorrectas borradas.')

# Columnas: Unidad | Tratamiento | Angulo | Hook/problema | Beneficio | CTA | Referencia | Activo | Enlace | Resultados | Comentarios | Notas
ads = [
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Esfuerzo no reconocido',
        'Perdiste el peso. Ahora, que tu cuerpo lo refleje.',
        'Elimina el exceso de piel y completa tu transformacion.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de persona de espaldas con postura segura, luz calida. Contraste entre esfuerzo pasado y resultado presente. Overlay con el hook en tipografia serif bold. Fondo neutro. Tono aspiracional.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Problema - Solucion - Piel sobrante',
        'El exceso de piel no desaparece solo.',
        'La cirugia post-perdida de peso elimina lo que el esfuerzo no puede.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen clinica neutra mostrando zona abdominal con exceso de piel marcada con flecha discreta. Fondo blanco, luz profesional. Overlay con el hook en bold. Aspecto medico, sin sensacionalismo.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Ultima etapa',
        'Ya llegaste. Solo falta el ultimo paso.',
        'Completamos tu transformacion con una planificacion quirurgica a tu medida.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de persona mirando hacia adelante, postura resolutiva. Luz de amanecer o fondo luminoso. Overlay con el hook en dos lineas, tipografia clean bold. Paleta blanca y dorada. Tono de cierre de etapa.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Demostracion - Abdomen',
        'Abdomen tras perder mucho peso: tiene solucion quirurgica.',
        'La abdominoplastia elimina el exceso de piel abdominal y redefine el contorno.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen clinica neutra de zona abdominal. Flecha o marcador de zona. Fondo blanco, luz profesional. Overlay con el hook. Aspecto medico informativo. Sin retoque exagerado.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Founder - Plan personalizado',
        'No trabajamos con una intervencion aislada. Trabajamos con un plan.',
        'Priorizamos zonas y tiempos para que cada etapa tenga sentido en tu caso.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Foto profesional del Dr. Joan Benitez en consulta o con bata medica. Cita del hook en overlay. Nombre completo y especialidad al pie. Fondo blanco/gris clinico. Tono de autoridad y confianza.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Problema - Funcional',
        'El exceso de piel genera rozaduras, irritacion y malestar.',
        'No es solo estetico. Es calidad de vida. Y tiene solucion.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen conceptual: persona activa limitada por incomodidad (no mostrar lesiones). Overlay con el hook en dos lineas. Fondo neutro. Tipografia sans-serif clara. Tono empatico y resolutivo.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Ropa',
        'Perdiste el peso. Ya es hora de comprarte esa ropa.',
        'La cirugia post-perdida de peso completa lo que el esfuerzo empezo.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de persona eligiendo ropa con actitud positiva. Tono luminoso y optimista. Overlay con el hook. Tipografia serif elegante. Fondo calido. Sin mostrar cuerpo de forma critica.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Comparativo - Post bariatrica',
        'Tras la bariatrica, el siguiente paso es completar tu transformacion.',
        'Muchos pacientes bariátricos necesitan cirugia de contorno corporal para terminar el proceso.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Infografia sencilla: linea temporal con dos etapas (perdida de peso / contorno corporal). Iconos simples. Fondo blanco, paleta medica. Overlay con el hook. Tono informativo y esperanzador.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Verano',
        'Este verano, sin esconder el resultado de tu esfuerzo.',
        'Completa tu transformacion antes de que llegue la temporada.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Persona en entorno de verano, imagen luminosa y positiva. Overlay con el hook en blanco. Tono veraniego aspiracional. Sin cuerpos perfectos irreales. Logo clinica abajo.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Tutorial - Proceso',
        'Como se planifica una cirugia post-perdida de peso.',
        '1. Consulta. 2. Evaluacion de zonas. 3. Orden y tiempos. 4. Intervencion. Sin sorpresas.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Infografia tipo timeline con 4 pasos. Iconos simples. Fondo blanco, paleta verde/azul medico. Texto breve en cada paso. Logo al pie. Aspecto de guia clara.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Social proof - Local',
        'Pacientes de toda Andalucia eligen Diagonal CQ para completar su transformacion.',
        'No somos una franquicia. Somos una clinica con historia en Cordoba.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen exterior o interior de la clinica en Cordoba. Overlay con Cordoba destacado. Resenas de Google si disponibles. Referencia de ubicacion. Tono local y de confianza.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Demostracion - Brazos',
        'La piel sobrante en brazos tiene solucion quirurgica.',
        'El lifting de brazos elimina el exceso de piel y redefine el contorno.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen clinica neutra de zona de brazo/triceps. Marcador de zona discreto. Fondo blanco, luz profesional. Overlay con el hook. Aspecto medico informativo.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Autoestima',
        'Hiciste el esfuerzo mas dificil. Mereces ver los resultados.',
        'La cirugia post-perdida de peso es la ultima parte de un proceso que ya empezaste.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de persona con expresion de satisfaccion y resolucion, postura segura. Luz calida. Overlay con el hook en tipografia serif. Tono de reconocimiento del esfuerzo. Sin cuerpos irreales.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Problema - Medicacion adelgazante',
        'La medicacion para adelgazar puede dejar exceso de piel. Hay una siguiente etapa.',
        'Si perdiste mucho peso con medicacion, la cirugia de contorno corporal puede completar el resultado.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen conceptual: persona activa y satisfecha con su perdida de peso, pero con interrogante sobre el siguiente paso. Overlay con el hook en dos lineas. Tono informativo y positivo.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Comparativo - No es vanidad',
        'No es vanidad. Es completar una transformacion real.',
        'La cirugia post-perdida de peso aborda tambien problemas funcionales, no solo esteticos.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de persona activa y en movimiento. Overlay con el hook en bold. Fondo luminoso. Tipografia clean sans-serif. Tono reivindicativo y empoderador.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Founder - Privacidad',
        'Tu cirugia es tuya. No publicamos fotos de nuestros pacientes.',
        'En Diagonal CQ la privacidad no es opcional. Es parte del trato.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen de consulta medica discreta, ambiente de confianza. Icono de privacidad o candado integrado de forma sutil. Overlay con el hook. Tono de seguridad y respeto. Logo al pie.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Problema - Cicatrices',
        'Las cicatrices te frenan? La tecnica LASH las minimiza.',
        'En Diagonal CQ trabajamos con tecnicas de incision dirigida para reducir la visibilidad de las cicatrices.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen clinica de cicatriz bien cicatrizada y discreta (no alarmante). Overlay con el hook. Fondo blanco, aspecto medico. Nota al pie con el nombre de la tecnica LASH.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Emocional - Brazos y ropa',
        'La manga corta ya no es un problema.',
        'El lifting de brazos elimina el exceso de piel y devuelve la libertad de vestir.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Persona con manga corta o sin mangas en actitud relajada y segura. Imagen de verano, tono positivo. Overlay con el hook. Tipografia bold limpia. Fondo luminoso.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Dato - Experiencia del cirujano',
        'Mas de 25 anos operando en Cordoba. Especializacion en cirugia post-perdida de peso.',
        'El Dr. Joan Benitez lleva desde 1999 tratando casos de cirugia plastica y reconstructiva.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Foto profesional del Dr. Joan Benitez. Overlay con el dato de anos de experiencia en numero grande. Nombre y especialidad al pie. Fondo blanco clinico. Tono de autoridad y trayectoria.'
    ],
    [
        'Cirugia', 'Post-perdida de peso', 'Demostracion - Muslos',
        'La piel sobrante en muslos limita tu movilidad. Tiene solucion.',
        'El lifting de muslos elimina el exceso de piel y mejora el contorno y la movilidad.',
        'Rellena el formulario para reservar tu consulta con cirujano gratis.',
        '', '', '', '', '',
        'Imagen clinica neutra de zona de muslo/interior pierna. Marcador de zona discreto. Fondo blanco, luz profesional. Overlay con el hook. Aspecto medico informativo. Sin retoque exagerado.'
    ],
]

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='IMG!A:L',
    valueInputOption='USER_ENTERED',
    body={'values': ads}
).execute()

print(f'OK: {len(ads)} propuestas correctas escritas en IMG.')
