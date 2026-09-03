# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)
SHEET_ID = '1CD-CqKdVD6q7J2tTLwZ-QovrDNobomIp_jvmR63sVH8'

# Columnas: Unidad | Tratamiento | Ángulo | Hook/problema | Beneficio | CTA | Ref | Activo | Enlace | Resultados | Comentarios | Notas
rows = [
    # --- CAMBIO NATURAL ---
    ['Cirugía', 'Post-pérdida de peso', 'Cambio natural',
     'Perdiste el peso tras el embarazo. Tu cuerpo merece el siguiente paso.',
     'Elimina el exceso de piel y recupera tu silueta con cirugía planificada.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de mujer en entorno cotidiano, tono cálido y natural. No clínico. Overlay con el hook en serif. Paleta crema. Tono de reconocimiento, no de insatisfacción.'],

    ['Cirugía', 'Post-pérdida de peso', 'Cambio natural',
     'Una nueva etapa merece un cuerpo que la represente.',
     'Completa tu transformación con cirugía post-pérdida de peso en Córdoba.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de persona en entorno luminoso de inicio de etapa (exterior, luz de mañana). Overlay con el hook en tipografía serif elegante. Tono aspiracional y positivo.'],

    ['Cirugía', 'Post-pérdida de peso', 'Cambio natural',
     'El autocuidado no termina con la dieta.',
     'La cirugía post-pérdida de peso es el paso natural para completar el proceso.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de persona en rutina de autocuidado cotidiano, tono cálido. Overlay con el hook. Tipografía clean sans-serif. Fondo neutro. Mensaje de continuidad, no de urgencia.'],

    # --- ESTÉTICO ---
    ['Cirugía', 'Post-pérdida de peso', 'Estético',
     'Luce cualquier ropa sin pensar en lo que esconde.',
     'La cirugía post-pérdida de peso elimina el exceso de piel y devuelve la confianza al vestir.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Persona eligiendo ropa con actitud segura y desenfadada. Armario abierto al fondo. Overlay con el hook en bold. Paleta cálida. Tono de libertad, no de problema.'],

    ['Cirugía', 'Post-pérdida de peso', 'Estético',
     'Define tu silueta después de la pérdida de peso.',
     'Elimina el exceso de piel y consigue el contorno corporal que el esfuerzo no pudo terminar.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de persona con postura segura, contorno corporal bien definido visualmente. Fondo neutro o minimalista. Overlay con el hook. Tipografía bold. Tono de resultado visible.'],

    ['Cirugía', 'Post-pérdida de peso', 'Estético',
     'Deja de depender de fajas y ropa de compresión.',
     'La cirugía post-pérdida de peso te da el contorno que las fajas solo simulan.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen conceptual: faja o ropa de compresión en primer plano tachada de forma sutil. Contraste con persona en ropa normal y cómoda. Overlay con el hook. Tono directo y resolutivo.'],

    ['Cirugía', 'Post-pérdida de peso', 'Estético',
     'Adiós a la ropa que escondes y la que evitas.',
     'Con la cirugía post-pérdida de peso, viste lo que quieras sin pensar en ello.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Armario con ropa de colores y patrones variados, imagen luminosa. Persona eligiendo con actitud positiva. Overlay con el hook en bold. Fondo cálido. Tono de libertad.'],

    # --- RESULTADO ---
    ['Cirugía', 'Post-pérdida de peso', 'Resultado',
     'Tu báscula dice una cosa. Tu ropa, otra. La cirugía lo alinea.',
     'Completa el resultado con cirugía post-pérdida de peso planificada a tu medida.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Diseño tipográfico en tres líneas con ritmo visual. Fondo blanco o negro. Sin imagen de cuerpo. Impacto por el texto. Tipografía bold contrastada.'],

    ['Cirugía', 'Post-pérdida de peso', 'Resultado',
     'La bariátrica te cambió la vida. Esto completa el resultado.',
     'La cirugía post-pérdida de peso es el paso final para muchos pacientes bariátricos.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Infografía sencilla: línea de proceso con dos etapas (cirugía bariátrica → contorno corporal). Iconos simples. Fondo blanco. Tono informativo y esperanzador.'],

    ['Cirugía', 'Post-pérdida de peso', 'Resultado',
     'Todo el esfuerzo. Por fin, el resultado completo.',
     'La cirugía post-pérdida de peso cierra lo que la dieta y el ejercicio empezaron.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de persona con postura abierta y expresión de satisfacción. Luz natural, tono cálido. Overlay con el hook en serif bold. Fondo neutro. Tono de logro sin exageración.'],

    # --- PROBLEMA ---
    ['Cirugía', 'Post-pérdida de peso', 'Problema',
     '¿Evitas fotos aunque hayas perdido todo el peso?',
     'El exceso de piel después de adelgazar tiene solución quirúrgica.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Persona mirando el móvil con expresión ambivalente ante una foto. Imagen cotidiana, tono empático. Overlay con el hook en bold. Fondo neutro. Sin dramatismo.'],

    ['Cirugía', 'Post-pérdida de peso', 'Problema',
     'El exceso de piel limita tus movimientos. No tiene por qué.',
     'La cirugía post-pérdida de peso mejora también la movilidad y la calidad de vida.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Persona activa que se mueve con incomodidad (sin mostrar lesiones). Imagen conceptual. Overlay con el hook en dos líneas. Fondo neutro. Tipografía sans-serif. Tono funcional y resolutivo.'],

    ['Cirugía', 'Post-pérdida de peso', 'Problema',
     'No te reconoces en el espejo aunque hayas perdido mucho peso.',
     'La cirugía post-pérdida de peso alinea tu imagen exterior con tu transformación interior.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Persona frente al espejo con expresión reflexiva pero no negativa. Luz suave. Overlay con el hook. Tipografía serif. Tono de empatía y reconocimiento, no de insatisfacción.'],

    # --- PROCESO ---
    ['Cirugía', 'Post-pérdida de peso', 'Proceso',
     'Tú solo pon la fecha. Nosotros planificamos el resto.',
     'En Diagonal CQ nos encargamos de todo: orden de intervenciones, tiempos y seguimiento.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de agenda o calendario con una fecha marcada. Tono organizado y tranquilizador. Overlay con el hook. Tipografía clean. Fondo clínico neutro. Logo al pie.'],

    ['Cirugía', 'Post-pérdida de peso', 'Proceso',
     'Tu cirugía post-pérdida de peso no tiene letra pequeña.',
     'Presupuesto claro, plan definido y sin sorpresas desde la primera consulta.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de documento o presupuesto limpio sobre mesa de consulta. Tono de transparencia y confianza. Overlay con el hook en bold. Fondo blanco clínico. Logo al pie.'],

    ['Cirugía', 'Post-pérdida de peso', 'Proceso',
     'Tu recuperación también está planificada.',
     'Te acompañamos en cada etapa: antes, durante y después de la intervención.',
     'Rellena el formulario para reservar tu consulta con cirujano gratis.',
     '', '', '', '', '',
     'Imagen de consulta de seguimiento, médico y paciente en conversación tranquila. Tono de acompañamiento. Overlay con el hook. Fondo clínico cálido. Tipografía serif. Logo al pie.'],
]

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='IMG!A:L',
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f'OK: {len(rows)} propuestas nuevas escritas.')
