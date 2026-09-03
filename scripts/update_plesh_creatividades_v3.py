# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

SHEET_ID = '1n-1zIwRaw0dGwMM5cB5sAadnlcoj8hYZHj4uX-f1Mkw'

URL_CAF = 'https://plesh-cafeterias.vercel.app'
URL_GYM = 'https://plesh-gimnasio.vercel.app'

ads = [
    # CAFETERIAS
    [
        'Cafeterias',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Problema - Solucion',
        'Tu cliente cuida lo que come. En tu mostrador no hay nada que comprarle.\n\nDos momentos en una imagen: izquierda, mostrador sin diferencial con cliente pasando de largo; derecha, mismo mostrador con Plesh y cliente comprando. Copy del hook en overlay. Fondo oscuro.',
        'Solicita informacion - empieza a venderlo esta semana',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Social proof',
        'Ya son mas de 500 los mostradores que tienen Plesh. El tuyo, todavia no.\n\nNumero en grande como headline. Logos de Incapto, Ametller Origen, Areas, Vueling como prueba social. Fondo oscuro, acento naranja Plesh.',
        'Unete - recibe condiciones sin compromiso',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Milk Choco Salted Caramel Almond Bites',
        'Carrusel',
        'Demostracion',
        'Lo que pasa cuando aparece el snack sin azucar en el mostrador.\n\nT1: mostrador vacio (antes). T2: mano cogiendo Plesh. T3: texto "El cliente saludable recompra". T4: CTA + pack de prueba.',
        'Compruebalo - pide el pack de prueba',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Pack de prueba',
        'Carrusel',
        'Comparativo',
        'La cafeteria de al lado ya vende Plesh. La tuya tambien?\n\nT1: mostrador estandar sin diferencial. T2: mismo mostrador con Plesh visible y cliente comprando. T3: "Cual es el tuyo?" + CTA.',
        'Rellena el formulario - condiciones en 48h',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Dato / Estadistica',
        'Cuantos clientes cuidan lo que comen pero no encuentran nada en tu mostrador.\n\nFondo oscuro. Texto en naranja Plesh. Subtexto: "Chocolate sin azucar anadido. Fuente de proteina y fibra prebiotica."',
        'Dales algo que comprar - solicita catalogo',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Pack de prueba',
        'Imagen estatica',
        'Testimonial',
        'Pack de prueba el lunes. Reposicion pedida el viernes.\n\nFoto de encargado de cafeteria detras del mostrador con Plesh visible. Quote del testimonial en overlay. Ambiente de cafeteria real.',
        'Solicita tu pack de prueba',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Snacks Plesh (general)',
        'Carrusel',
        'Before / After',
        'Sin Plesh: tu cliente saludable se va sin postre. Con Plesh: no.\n\nT1 (SIN): mostrador, cliente pasa de largo. T2 (CON): mismo mostrador con Plesh, cliente compra. T3: beneficios clave (margen, rotacion, diferenciacion). T4: CTA.',
        'Empieza a venderlo sin riesgo',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Dark Choco Sea Salt Almond Bites',
        'Imagen estatica',
        'Emocional',
        'Cada cliente que sale sin comprar nada dulce es dinero que no vuelve.\n\nImagen atmosferica de cafeteria. Solo texto en overlay, sin mostrar producto. Fondo oscuro. El copy carga todo el peso.',
        'Ponlo en tu mostrador - solicita condiciones',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Founder',
        'Lo cree porque no existia en ningun mostrador. Ya lo venden mas de 500 cafeterias.\n\nFoto del founder con el producto. Quote del hook en overlay. Fondo negro, acento naranja Plesh.',
        'Se el siguiente - rellena el formulario',
        URL_CAF
    ],
    [
        'Cafeterias',
        'Pack de prueba',
        'Imagen estatica',
        'Tutorial',
        '3 pasos para tener Plesh en tu mostrador esta semana.\n\nInfografia: 1. Rellenas el formulario (30 seg). 2. Recibes condiciones y catalogo en 48h. 3. Colocas y empiezas a vender. Fondo negro, numeros en naranja Plesh.',
        'Empieza ahora - rellena el formulario',
        URL_CAF
    ],

    # GIMNASIOS
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Ingresos pasivos',
        'Tu recepcion tiene coste fijo. Plesh la convierte en punto de venta.\n\nImagen limpia de recepcion de gimnasio. Overlay con copy. Tono de negocio, no de fitness. Sin producto en primer plano.',
        'Activa tu recepcion - solicita informacion',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Dark Choco Almond Crunch Bar',
        'Imagen estatica',
        'Social proof',
        'Mas de 500 centros deportivos en Espana ya generan ingresos en recepcion con Plesh.\n\nProducto sobre fondo blanco limpio. Numero en naranja destacado. Subtexto: "Sin azucar. Fuente de proteina. El snack que tus socios buscan."',
        'El tuyo, el siguiente? Solicita condiciones',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Carrusel',
        'Objecion: espacio',
        'No tienes espacio para una tienda? Plesh ocupa menos que una caja de guantes.\n\nT1: pregunta + foto de recepcion real con espacio minimo. T2: expositor Plesh en ese espacio. T3: "Sin almacen. Sin formacion. Sin gestion extra." T4: CTA.',
        'Compruebalo - pide el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Coherencia de marca',
        'Tus socios cuidan lo que comen. El snack de tu recepcion, tambien?\n\nFoto comparativa: snack convencional vs Plesh. Tono de coherencia de imagen de centro. Fondo blanco, producto en primer plano.',
        'Dale coherencia a tu centro - solicita catalogo',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Dark Choco Almond Crunch Bar',
        'Imagen estatica',
        'Momento post-entreno',
        'El momento mas facil de vender algo en un gimnasio: la salida del vestuario.\n\nFoto de salida de vestuario con Plesh en el frame. Copy directo. Fondo blanco. Lenguaje de negocio.',
        'Aprovechalo - solicita informacion',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Imagen estatica',
        'Testimonial',
        'Pense que mis socios ya tenian su nutricion controlada. Me equivoque.\n\nFoto de manager de gimnasio en recepcion. Producto visible al fondo. Quote del testimonial en overlay. Tono natural.',
        'Solicita el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Carrusel',
        'Before / After',
        'Antes: recepcion sin ingresos propios. Despues: Plesh se vende solo.\n\nT1 (ANTES): recepcion vacia, solo check-ins y tarjetas. T2 (DESPUES): mismo espacio con Plesh, socios comprando. T3: "Sin gestion extra. Sin riesgo." T4: CTA.',
        'Empieza sin riesgo - pide el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Imagen estatica',
        'Venta perdida',
        'Cada vez que un socio compra el snack fuera, tu pierdes esa venta.\n\nFoto de socio saliendo del gym. Copy en overlay. Sin producto visible. El dolor del propietario es el protagonista. Fondo oscuro.',
        'Coge esa venta - solicita condiciones',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Pack de prueba',
        'Imagen estatica',
        'Founder',
        'Lo disene pensando en el socio que entrena y cuida lo que come. El tuyo lo busca.\n\nFoto del founder en entorno fitness. Hook en overlay. Cierra con producto colocado en recepcion real de gimnasio.',
        'Ponlo en recepcion - empieza con el pack de prueba',
        URL_GYM
    ],
    [
        'Gimnasios',
        'Snacks Plesh (general)',
        'Carrusel',
        'Tutorial',
        'Cuanto espacio necesita Plesh en tu recepcion? Menos del que crees.\n\nT1: pregunta + foto de espacio real en recepcion de gimnasio. T2: "1 expositor pequeno. Sin almacen. Sin formacion." T3: proceso - formulario / catalogo / primer pedido / a vender. T4: CTA.',
        'Rellena el formulario - te contactamos en 48h',
        URL_GYM
    ],
]

service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A7:G26',
    valueInputOption='RAW',
    body={'values': ads}
).execute()

print('OK - 20 ADs actualizados con valueInputOption RAW.')
