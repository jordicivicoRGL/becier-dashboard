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
ads = [
    # CAFETERIAS
    ['Cafeterias', 'Snacks Plesh (general)', 'Imagen estatica', 'Problema - Solucion',
     'Tu cliente saludable pide el cafe y se va sin comprar nada mas. Aqui esta el motivo. / Dos momentos en una sola imagen: izquierda, cliente mirando mostrador vacio; derecha, cliente con Plesh en mano. Copy del hook como headline.',
     'Solicita informacion y empieza a venderlo esta semana', URL_CAF],

    ['Cafeterias', 'Snacks Plesh (general)', 'Imagen estatica', 'Social proof',
     '+500 cafeterias ya tienen Plesh en el mostrador. La tuya, todavia no. / Imagen del producto en mostrador reconocible. Numero en grande como headline. Sub: logos de Incapto, Ametller, Areas.',
     'Unete a los +500 puntos de venta', URL_CAF],

    ['Cafeterias', 'Milk Choco Salted Caramel Almond Bites', 'Carrusel', 'Demostracion',
     'Lo que pasa cuando pones Plesh al lado de la caja registradora. / Tarjeta 1: producto en mostrador (antes). Tarjeta 2: mano cogiendo el producto. Tarjeta 3: datos de rotacion/recompra. Tarjeta 4: CTA.',
     'Pide el pack de prueba sin compromiso', URL_CAF],

    ['Cafeterias', 'Pack de prueba', 'Carrusel', 'Comparativo',
     'Tu mostrador vs el de la cafeteria de al lado que ya vende Plesh. / Tarjeta 1: mostrador generico sin diferencial. Tarjeta 2: mostrador con Plesh. Tarjeta 3: CTA con "Cual es el tuyo?"',
     'Rellena el formulario y recibe condiciones en 48h', URL_CAF],

    ['Cafeterias', 'Snacks Plesh (general)', 'Imagen estatica', 'Dato / Estadistica',
     'El cliente que cuida lo que come ya existe en tu cafeteria. Solo necesita algo que comprar. / Fondo oscuro, texto en naranja Plesh. Subtexto: "Chocolate sin azucar. Sin gluten. Fuente de proteina. Listo para tu mostrador."',
     'Diferencia tu mostrador - solicita informacion', URL_CAF],

    ['Cafeterias', 'Pack de prueba', 'Imagen estatica', 'Testimonial',
     'Empece con el pack de prueba. En tres semanas pedi reposicion. / Foto del dueno o encargado de cafeteria detras del mostrador con Plesh visible. Quote del testimonial en overlay.',
     'Solicita el pack de prueba', URL_CAF],

    ['Cafeterias', 'Snacks Plesh (general)', 'Carrusel', 'Before / After',
     'Antes: el cliente cuida la dieta y no compra nada dulce. Despues: Plesh en el mostrador. / Tarjeta 1 (ANTES): mostrador sin snack saludable, cliente de largo. Tarjeta 2 (DESPUES): mismo mostrador con Plesh, cliente comprando. Tarjeta 3: beneficios clave. Tarjeta 4: CTA.',
     'Empieza a venderlo sin riesgo', URL_CAF],

    ['Cafeterias', 'Dark Choco Sea Salt Almond Bites', 'Imagen estatica', 'Emocional',
     'Cada cliente que sale sin comprar nada dulce es dinero que no vuelve. / Imagen atmosferica de cafeteria. Copy en overlay. Fondo oscuro. Sin mostrar el producto - el copy carga todo el peso.',
     'Solicita condiciones sin compromiso', URL_CAF],

    ['Cafeterias', 'Snacks Plesh (general)', 'Imagen estatica', 'Founder',
     'Cree Plesh porque en ninguna cafeteria encontraba chocolate sin azucar. Ya hay +500 que lo tienen. / Foto del founder con el producto. Quote del hook en overlay. Fondo oscuro, naranja Plesh.',
     'Se el siguiente punto de venta - rellena el formulario', URL_CAF],

    ['Cafeterias', 'Pack de prueba', 'Imagen estatica', 'Tutorial',
     '3 pasos para tener Plesh en tu mostrador esta semana. / Diseno tipo infografia. 1: rellenas el formulario (30 seg). 2: recibes condiciones y catalogo en 48h. 3: colocas y empiezas a vender. Fondo negro, naranja Plesh para los numeros.',
     'Empieza ahora - rellena el formulario', URL_CAF],

    # GIMNASIOS
    ['Gimnasios', 'Snacks Plesh (general)', 'Imagen estatica', 'Problema - Solucion',
     'Tus socios salen del vestuario con hambre y no tienen nada que comprar en tu centro. / Imagen: socio saliendo del vestuario, recepcion sin snack saludable. Copy del hook como headline en overlay.',
     'Solicita informacion y ponlo en recepcion esta semana', URL_GYM],

    ['Gimnasios', 'Dark Choco Almond Crunch Bar', 'Imagen estatica', 'Social proof',
     '+500 centros deportivos en Espana ya generan ingresos en recepcion con Plesh. / Producto sobre fondo blanco limpio. Numero en naranja destacado. Subtexto: "Sin azucar. Fuente de proteina. El snack que tus socios buscan."',
     'Unete a los +500 puntos de venta', URL_GYM],

    ['Gimnasios', 'Snacks Plesh (general)', 'Carrusel', 'Demostracion',
     'Asi queda Plesh en la recepcion de un gimnasio. Y asi rota. / Tarjeta 1: foto producto en recepcion (lifestyle). Tarjeta 2: mano de socio cogiendo el producto post-entreno. Tarjeta 3: texto diferencial (sin azucar, proteina, rotacion alta). Tarjeta 4: CTA.',
     'Pide el pack de prueba sin compromiso', URL_GYM],

    ['Gimnasios', 'Snacks Plesh (general)', 'Carrusel', 'Comparativo',
     'El gimnasio de enfrente ya tiene Plesh en recepcion. El tuyo, tambien? / Tarjeta 1: recepcion sin producto. Tarjeta 2: recepcion con Plesh. Tarjeta 3: CTA. Sin texto redundante - la imagen lo dice todo.',
     'Recibe condiciones en 48h', URL_GYM],

    ['Gimnasios', 'Dark Choco Almond Crunch Bar', 'Imagen estatica', 'Dato / Estadistica',
     'El snack post-entreno es la compra mas impulsiva que puede hacer un socio en tu centro. Lo tienes? / Fondo blanco, producto en primer plano. Texto directo. Lenguaje de negocio, no de fitness.',
     'Aprovechalo - solicita informacion', URL_GYM],

    ['Gimnasios', 'Pack de prueba', 'Imagen estatica', 'Testimonial',
     'Lo puse en recepcion sin expectativas. Ahora lo repongo cada dos semanas. / Foto del manager de gimnasio en la recepcion. Producto visible al fondo. Quote del testimonial en overlay.',
     'Solicita el pack de prueba', URL_GYM],

    ['Gimnasios', 'Snacks Plesh (general)', 'Carrusel', 'Before / After',
     'Antes: recepcion sin ingresos propios. Despues: Plesh genera ventas solo. / Tarjeta 1 (ANTES): recepcion vacia, solo check-ins. Tarjeta 2 (DESPUES): mismo espacio con Plesh, socios comprando. Tarjeta 3: "Sin gestion extra. Sin riesgo." Tarjeta 4: CTA.',
     'Empieza sin riesgo con el pack de prueba', URL_GYM],

    ['Gimnasios', 'Snacks Plesh (general)', 'Imagen estatica', 'Emocional',
     'Tu socio cuida lo que come. Si no encuentra nada en tu centro, lo compra en otro sitio. / Foto de socio saliendo del gym con bolsa de deporte. Fondo difuminado. Copy en overlay. Sin producto visible - el dolor del negocio es el protagonista.',
     'Dale donde gastar - solicita condiciones', URL_GYM],

    ['Gimnasios', 'Pack de prueba', 'Imagen estatica', 'Founder',
     'Cree Plesh para el cliente que entrena y cuida lo que come. El tuyo ya existe. Lo tienes en tu centro? / Foto del founder en entorno fitness. Hook en overlay. Cierra con producto en recepcion real.',
     'Empieza con el pack de prueba', URL_GYM],

    ['Gimnasios', 'Snacks Plesh (general)', 'Carrusel', 'Tutorial',
     'Cuanto espacio necesita Plesh en recepcion? Menos del que crees. / Tarjeta 1: pregunta + foto de espacio real en recepcion. Tarjeta 2: "1 expositor pequeno. Sin almacen. Sin formacion." Tarjeta 3: proceso: formulario - catalogo - primer pedido - a vender. Tarjeta 4: CTA.',
     'Rellena el formulario - te contactamos en 48h', URL_GYM],
]

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='Creatividades!A:G',
    valueInputOption='USER_ENTERED',
    body={'values': ads}
).execute()

print(f"OK - {len(ads)} filas escritas en el Sheet.")
