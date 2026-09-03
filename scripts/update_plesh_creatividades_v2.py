# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'

URL_CAF = 'https://plesh-cafeterias.vercel.app'
URL_GYM = 'https://plesh-gimnasio.vercel.app'

# Columnas: A=Target, B=Producto, C=Formato, D=Tipo, E=Hook/Idea principal, F=CTA, G=Landing
# Las filas 7-26 son las nuestras (20 ADs). Las sobreescribimos con la versión mejorada.
# Mejoras aplicadas:
# - Acentos y caracteres españoles correctos
# - Hooks recortados a máx 1-2 frases (regla de 3 segundos)
# - CTAs diferenciados entre cafeterías y gimnasios
# - Gimnasios con ángulos propios (no espejo de cafeterías)
# - Fix del #ERROR! en fila 18 (el + al inicio se interpreta como fórmula)

ads = [
    # ── CAFETERÍAS ───────────────────────────────────────────────────────────
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Problema → Solución',
        'Tu cliente cuida lo que come. En tu mostrador no hay nada que comprarle.\n\nDos momentos en una imagen: izquierda, mostrador sin diferencial con cliente pasando de largo; derecha, mismo mostrador con Plesh y cliente comprando. Copy del hook en overlay. Fondo oscuro.',
        'Solicita información — empieza a venderlo esta semana',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Social proof',
        '+500 mostradores. ¿El tuyo es el 501?\n\nNúmero en grande como headline. Logos de Incapto, Ametller Origen, Areas, Vueling como prueba social. Fondo oscuro, acento naranja Plesh.',
        'Únete — recibe condiciones sin compromiso',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Milk Choco Salted Caramel Almond Bites',
        'Carrusel',
        'Demostración',
        'Lo que pasa cuando aparece el snack sin azúcar en el mostrador.\n\nT1: mostrador vacío (antes). T2: mano cogiendo Plesh. T3: texto "El cliente saludable recompra". T4: CTA + pack de prueba.',
        'Compruébalo — pide el pack de prueba',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Pack de prueba',
        'Carrusel',
        'Comparativo',
        'La cafetería de al lado ya vende Plesh. ¿La tuya también?\n\nT1: mostrador estándar sin diferencial. T2: mismo mostrador con Plesh visible y cliente comprando. T3: "¿Cuál es el tuyo?" + CTA.',
        'Rellena el formulario — condiciones en 48h',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Dato / Estadística',
        'Cuántos clientes cuidan lo que comen pero no encuentran nada en tu mostrador.\n\nFondo oscuro. Texto en naranja Plesh. Subtexto: "Chocolate sin azúcar añadido. Fuente de proteína y fibra prebiótica."',
        'Dales algo que comprar — solicita catálogo',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Pack de prueba',
        'Imagen estática',
        'Testimonial',
        'Pack de prueba el lunes. Reposición pedida el viernes.\n\nFoto de encargado de cafetería detrás del mostrador con Plesh visible. Quote del testimonial en overlay. Ambiente de cafetería real.',
        'Solicita tu pack de prueba',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Carrusel',
        'Before / After',
        'Sin Plesh: tu cliente saludable se va sin postre. Con Plesh: no.\n\nT1 (SIN): mostrador, cliente pasa de largo. T2 (CON): mismo mostrador con Plesh, cliente compra. T3: beneficios clave (margen, rotación, diferenciación). T4: CTA.',
        'Empieza a venderlo sin riesgo',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Dark Choco Sea Salt Almond Bites',
        'Imagen estática',
        'Emocional',
        'Cada cliente que sale sin comprar nada dulce es dinero que no vuelve.\n\nImagen atmosférica de cafetería. Solo texto en overlay, sin mostrar producto. Fondo oscuro. El copy carga todo el peso.',
        'Ponlo en tu mostrador — solicita condiciones',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Founder',
        'Lo creé porque no existía en ningún mostrador. Ya lo venden más de 500 cafeterías.\n\nFoto del founder con el producto. Quote del hook en overlay. Fondo negro, acento naranja Plesh.',
        'Sé el siguiente — rellena el formulario',
        URL_CAF
    ],
    [
        'Cafeterías',
        'Pack de prueba',
        'Imagen estática',
        'Tutorial',
        '3 pasos para tener Plesh en tu mostrador esta semana.\n\nInfografía: 1. Rellenas el formulario (30 seg). 2. Recibes condiciones y catálogo en 48h. 3. Colocas y empiezas a vender. Fondo negro, números en naranja Plesh.',
        'Empieza ahora — rellena el formulario',
        URL_CAF
    ],

    # ── GIMNASIOS (ángulos propios, no espejo de cafeterías) ─────────────────
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Ingresos pasivos',
        'Tu recepción tiene coste fijo. Plesh la convierte en punto de venta.\n\nImagen limpia de recepción de gimnasio. Overlay con copy. Tono de negocio, no de fitness. Sin producto en primer plano.',
        'Activa tu recepción — solicita información',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Dark Choco Almond Crunch Bar',
        'Imagen estática',
        'Social proof',
        'Más de 500 centros deportivos en España ya generan ingresos en recepción con Plesh.\n\nProducto sobre fondo blanco limpio. Número en naranja destacado. Subtexto: "Sin azúcar. Fuente de proteína. El snack que tus socios buscan."',
        '¿Es el tuyo el siguiente? Solicita condiciones',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Carrusel',
        'Objeción: espacio',
        '¿No tienes espacio para una tienda? Plesh ocupa menos que una caja de guantes.\n\nT1: pregunta + foto de recepción real con espacio mínimo. T2: expositor Plesh en ese espacio. T3: "Sin almacén. Sin formación. Sin gestión extra." T4: CTA.',
        'Compruébalo — pide el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Coherencia de marca',
        'Tus socios cuidan lo que comen. El snack de tu recepción, ¿también?\n\nFoto comparativa: snack convencional vs Plesh. Tono de coherencia de imagen de centro. Fondo blanco, producto en primer plano.',
        'Dale coherencia a tu centro — solicita catálogo',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Dark Choco Almond Crunch Bar',
        'Imagen estática',
        'Momento post-entreno',
        'El momento más fácil de vender algo en un gimnasio: la salida del vestuario.\n\nFoto de salida de vestuario con Plesh en el frame. Copy directo. Fondo blanco. Lenguaje de negocio.',
        'Aprovéchalo — solicita información',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Imagen estática',
        'Testimonial',
        'Pensé que mis socios ya tenían su nutrición controlada. Me equivoqué.\n\nFoto de manager de gimnasio en recepción. Producto visible al fondo. Quote del testimonial en overlay. Tono natural.',
        'Solicita el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Carrusel',
        'Before / After',
        'Antes: recepción sin ingresos propios. Después: Plesh se vende solo.\n\nT1 (ANTES): recepción vacía, solo check-ins y tarjetas. T2 (DESPUÉS): mismo espacio con Plesh, socios comprando. T3: "Sin gestión extra. Sin riesgo." T4: CTA.',
        'Empieza sin riesgo — pide el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estática',
        'Venta perdida',
        'Cada vez que un socio compra el snack fuera, tú pierdes esa venta.\n\nFoto de socio saliendo del gym. Copy en overlay. Sin producto visible — el dolor del propietario es el protagonista. Fondo oscuro.',
        'Coge esa venta — solicita condiciones',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Imagen estática',
        'Founder',
        'Lo diseñé pensando en el socio que entrena y cuida lo que come. El tuyo lo busca.\n\nFoto del founder en entorno fitness. Hook en overlay. Cierra con producto colocado en recepción real de gimnasio.',
        'Ponlo en recepción — empieza con el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Carrusel',
        'Tutorial',
        '¿Cuánto espacio necesita Plesh en tu recepción? Menos del que crees.\n\nT1: pregunta + foto de espacio real en recepción de gimnasio. T2: "1 expositor pequeño. Sin almacén. Sin formación." T3: proceso — formulario / catálogo / primer pedido / a vender. T4: CTA.',
        'Rellena el formulario — te contactamos en 48h',
        URL_GYM
    ],
]

# Sobreescribir exactamente las filas 7-26 (los 20 ADs originales)
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A7:G26',
    valueInputOption='USER_ENTERED',
    body={'values': ads}
).execute()

print(f'OK — {len(ads)} ADs actualizados en filas 7-26.')
