import requests as req
from tools.calendar_tools import get_google_credentials
from google.auth.transport.requests import Request

creds = get_google_credentials()
creds.refresh(Request())

DOC_ID = '1mbkD6hmmUm944_653ptryd9MGR4dgqZZWovMTC6wiRs'
TAB_ID = 't.0'
BASE = f'https://docs.googleapis.com/v1/documents/{DOC_ID}'
hdr_get = {'Authorization': f'Bearer {creds.token}'}
hdr = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}

# Bloques: (texto, estilo_parrafo, negrita, bullet)
BLOCKS = [
    # METADATOS
    ("── METADATOS ──\n", "HEADING_2", False, False),
    ("Meta title: Liposucción Abdomen en Córdoba | Diagonal CQ\n", "NORMAL_TEXT", False, False),
    ("Meta description: Elimina la grasa localizada del abdomen y flancos con liposucción en Córdoba. Consulta personalizada con el Dr. Benítez Gomà en Diagonal CQ.\n", "NORMAL_TEXT", False, False),
    ("URL slug: /cirugia-estetica/contorno-corporal/liposuccion-abdomen/\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("── TEXTO ──\n", "HEADING_2", False, False),

    ("H1: Liposucción de Abdomen y Flancos en Córdoba\n", "HEADING_1", True, False),
    ("La liposucción de abdomen es una de las intervenciones de cirugía estética más solicitadas en Diagonal CQ. Permite eliminar de forma selectiva la grasa localizada en el abdomen y los flancos —esa grasa subcutánea resistente que no desaparece con dieta ni ejercicio— y redefinir el contorno corporal de forma duradera.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Esta página explica en qué consiste la intervención, qué pacientes son candidatos, qué resultados son realistas y cuáles son sus limitaciones, desde un enfoque médico riguroso y sin promesas exageradas.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("[añadir imagen: persona activa con abdomen trabajado o foto de consulta médica en Diagonal CQ, sin mostrar rostros identificables]\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: ¿Qué es la liposucción de abdomen y flancos?\n", "HEADING_2", True, False),
    ("Técnica quirúrgica de contorno corporal que extrae depósitos de grasa subcutánea localizada en abdomen y flancos mediante cánulas de precisión.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("La liposucción es un procedimiento quirúrgico de cirugía estética y plástica que elimina acúmulos de grasa subcutánea mediante unas cánulas muy finas introducidas a través de pequeñas incisiones en la piel. En el caso del abdomen y los flancos, el objetivo es eliminar la grasa acumulada en la zona del vientre, los costados y la cintura, logrando un contorno corporal más definido y armónico.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("No se trata de un tratamiento para perder peso, sino de una intervención quirúrgica de remodelación corporal dirigida a pacientes que ya se encuentran en un peso estable y presentan grasa localizada en zonas específicas que no responde a otras medidas.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: ¿Cómo funciona?\n", "HEADING_3", True, False),
    ("El cirujano introduce las cánulas a través de pequeñas incisiones estratégicamente colocadas. Mediante movimientos controlados, se fragmenta y aspira la grasa del tejido subcutáneo. El resultado es una reducción del volumen en las zonas tratadas y una redefinición del contorno.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Existen distintas variantes técnicas —liposucción convencional, tumescente o asistida por ultrasonidos o láser— cuya indicación depende del volumen de grasa a tratar, la elasticidad de la piel y las características individuales de cada paciente.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Zonas tratadas: abdomen y flancos\n", "HEADING_3", True, False),
    ("En la liposucción de abdomen y flancos se puede intervenir sobre:\n", "NORMAL_TEXT", False, False),
    ("Abdomen superior e inferior (por encima y por debajo del ombligo).\n", "NORMAL_TEXT", False, True),
    ("Flancos o costados (la grasa que se acumula a los lados del tronco).\n", "NORMAL_TEXT", False, True),
    ("Zona lumbar o espalda baja, si el caso lo requiere.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("La planificación exacta de las zonas a tratar se define de forma individualizada en la consulta preoperatoria con el Dr. Benítez Gomà.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("[añadir imagen: esquema anatómico o fotografía médica que muestre las zonas de tratamiento del abdomen y flancos]\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: ¿Para quién está indicada la liposucción abdominal?\n", "HEADING_2", True, False),
    ("Indicada en pacientes con peso estable y grasa localizada en abdomen o flancos que no responde al ejercicio ni a la dieta.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("La liposucción de abdomen y flancos puede estar indicada en pacientes que:\n", "NORMAL_TEXT", False, False),
    ("Se encuentran en un peso estable y cercano a su peso ideal.\n", "NORMAL_TEXT", False, True),
    ("Presentan grasa localizada en abdomen, barriga o flancos resistente al ejercicio y la dieta.\n", "NORMAL_TEXT", False, True),
    ("Tienen buena elasticidad cutánea, que permite a la piel adaptarse tras la extracción de grasa.\n", "NORMAL_TEXT", False, True),
    ("Gozan de buena salud general y no presentan contraindicaciones quirúrgicas.\n", "NORMAL_TEXT", False, True),
    ("Tienen expectativas realistas sobre los resultados de la intervención.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("No está indicada como tratamiento para perder peso ni para tratar la obesidad. La indicación final se establece siempre tras una valoración médica individualizada con el Dr. Benítez Gomà.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Beneficios realistas de la liposucción de abdomen\n", "HEADING_2", True, False),
    ("Mejora el contorno corporal eliminando grasa localizada. Los resultados son duraderos si se mantiene un peso estable.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Entre los beneficios que puede aportar una liposucción de abdomen bien indicada se incluyen:\n", "NORMAL_TEXT", False, False),
    ("Reducción del volumen en abdomen y flancos.\n", "NORMAL_TEXT", False, True),
    ("Definición de la cintura y mejora del contorno corporal.\n", "NORMAL_TEXT", False, True),
    ("Resultados duraderos: las células grasas extraídas no vuelven a aparecer en la zona tratada.\n", "NORMAL_TEXT", False, True),
    ("Cicatrices muy pequeñas y discretas, generalmente imperceptibles a largo plazo.\n", "NORMAL_TEXT", False, True),
    ("Recuperación compatible con la vida laboral habitual en 1-2 semanas.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("Los resultados dependen del volumen de grasa extraído, la elasticidad de la piel, la técnica empleada y el seguimiento postoperatorio. La valoración médica previa es imprescindible para establecer expectativas realistas en cada caso.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Riesgos y efectos secundarios ⚠️\n", "HEADING_2", True, False),
    ("Como cualquier intervención quirúrgica, la liposucción conlleva riesgos que deben valorarse individualmente antes de la operación.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Entre los efectos secundarios más habituales y generalmente transitorios se encuentran:\n", "NORMAL_TEXT", False, False),
    ("Inflamación y edema en las zonas tratadas (puede prolongarse semanas o meses).\n", "NORMAL_TEXT", False, True),
    ("Hematomas y moratones, especialmente en los primeros días.\n", "NORMAL_TEXT", False, True),
    ("Dolor o molestia postoperatoria, controlable con medicación analgésica.\n", "NORMAL_TEXT", False, True),
    ("Sensación de entumecimiento o hipersensibilidad en la piel tratada.\n", "NORMAL_TEXT", False, True),
    ("Irregularidades cutáneas transitorias o permanentes en casos concretos.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("Entre las complicaciones menos frecuentes pero posibles:\n", "NORMAL_TEXT", False, False),
    ("Seroma (acumulación de líquido bajo la piel).\n", "NORMAL_TEXT", False, True),
    ("Infección de la herida.\n", "NORMAL_TEXT", False, True),
    ("Asimetrías o irregularidades del contorno.\n", "NORMAL_TEXT", False, True),
    ("Alteraciones de la sensibilidad de carácter más prolongado.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("El riesgo global se reduce significativamente con una correcta indicación médica, una técnica quirúrgica adecuada y un seguimiento postoperatorio riguroso.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Contraindicaciones: quién NO debería realizarse esta intervención\n", "HEADING_2", True, False),
    ("Existen situaciones médicas en las que la liposucción debe evitarse o posponerse hasta una evaluación adecuada.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("La liposucción de abdomen no está indicada en:\n", "NORMAL_TEXT", False, False),
    ("Pacientes con obesidad o peso inestable.\n", "NORMAL_TEXT", False, True),
    ("Personas con enfermedades no controladas (diabetes, problemas cardiovasculares, alteraciones de la coagulación).\n", "NORMAL_TEXT", False, True),
    ("Tabaquismo activo sin control médico previo.\n", "NORMAL_TEXT", False, True),
    ("Flacidez cutánea severa sin elasticidad suficiente (puede requerir una abdominoplastia).\n", "NORMAL_TEXT", False, True),
    ("Expectativas no realistas sobre los resultados.\n", "NORMAL_TEXT", False, True),
    ("Embarazo o período de lactancia.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("La indicación final debe establecerse siempre tras una valoración médica individual.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Resultados: qué esperar y qué NO esperar\n", "HEADING_2", True, False),
    ("La liposucción mejora el contorno abdominal de forma duradera, pero los resultados son progresivos y dependen de factores individuales.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Resultados inmediatos\n", "HEADING_3", True, False),
    ("Tras la intervención se aprecia una reducción inicial del volumen en las zonas tratadas, aunque el resultado está condicionado por la inflamación postoperatoria y la faja de compresión. En los primeros días o semanas, el contorno no refleja el resultado final.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Resultados progresivos\n", "HEADING_3", True, False),
    ("Los primeros resultados apreciables suelen observarse entre las 4 y las 8 semanas. El resultado definitivo puede tardar entre 4 y 6 meses en consolidarse, cuando la piel ha terminado de adaptarse y la inflamación residual ha desaparecido por completo.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Duración\n", "HEADING_3", True, False),
    ("Los resultados son duraderos si el paciente mantiene un peso estable. Las células grasas extraídas no vuelven a aparecer en la zona tratada; sin embargo, una ganancia de peso significativa puede redistribuirse por el resto del cuerpo y afectar al resultado final.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Qué NO esperar\n", "HEADING_3", True, False),
    ("No es un sustituto de la dieta ni del ejercicio físico.\n", "NORMAL_TEXT", False, True),
    ("No trata la flacidez ni el exceso de piel (puede requerir una abdominoplastia).\n", "NORMAL_TEXT", False, True),
    ("No garantiza resultados idénticos entre pacientes: cada organismo responde de forma diferente.\n", "NORMAL_TEXT", False, True),
    ("No ofrece resultados inmediatos: la inflamación postoperatoria forma parte del proceso.\n", "NORMAL_TEXT", False, True),
    ("No elimina la celulitis.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("[añadir imagen: fotografía clínica de antes/después de liposucción de abdomen — imágenes propias de Diagonal CQ, sin identificar al paciente]\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Cómo es el proceso en Diagonal CQ: paso a paso\n", "HEADING_2", True, False),
    ("El proceso incluye consulta preoperatoria, intervención quirúrgica y seguimiento postoperatorio individualizado.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Consulta preoperatoria\n", "HEADING_3", True, False),
    ("Todo comienza con una consulta médica detallada en nuestra clínica de Córdoba. El Dr. Benítez Gomà realiza una exploración física, analiza la distribución de la grasa y la calidad de la piel, revisa el historial clínico y explica con total transparencia qué resultados son realistas en tu caso concreto.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Si se confirma la indicación, se solicitan las pruebas preoperatorias necesarias:\n", "NORMAL_TEXT", False, False),
    ("Analítica de sangre completa.\n", "NORMAL_TEXT", False, True),
    ("Electrocardiograma.\n", "NORMAL_TEXT", False, True),
    ("Valoración anestésica.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: La intervención\n", "HEADING_3", True, False),
    ("La liposucción de abdomen y flancos se realiza en quirófano bajo anestesia general o sedación profunda, según el volumen de grasa a tratar. La duración habitual es de entre 1 y 3 horas. El cirujano realiza pequeñas incisiones en zonas estratégicas para minimizar las marcas visibles, e introduce las cánulas con las que se fragmenta y aspira la grasa de forma controlada.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Postoperatorio\n", "HEADING_3", True, False),
    ("Tras la intervención se coloca una faja de compresión que deberás llevar de forma continuada durante las primeras semanas. Es normal experimentar:\n", "NORMAL_TEXT", False, False),
    ("Inflamación y hematomas los primeros días.\n", "NORMAL_TEXT", False, True),
    ("Molestia controlable con analgesia.\n", "NORMAL_TEXT", False, True),
    ("Sensación de tensión o entumecimiento en la zona tratada.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("La mayoría de los pacientes retoman su actividad laboral en 7-14 días, en función del tipo de trabajo y la evolución individual.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: Seguimiento\n", "HEADING_3", True, False),
    ("En Diagonal CQ realizamos revisiones periódicas para supervisar la evolución de la cicatrización, controlar la inflamación y asegurarnos de que la recuperación transcurre correctamente. El protocolo de seguimiento se adapta a cada paciente.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Precio de la liposucción de abdomen en Córdoba\n", "HEADING_2", True, False),
    ("El precio varía según el volumen de grasa, las zonas a tratar y las características individuales de cada caso.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("El precio de la liposucción de abdomen depende de varios factores:\n", "NORMAL_TEXT", False, False),
    ("Zonas a intervenir: solo abdomen, abdomen y flancos, o zona lumbar.\n", "NORMAL_TEXT", False, True),
    ("Volumen de grasa a extraer.\n", "NORMAL_TEXT", False, True),
    ("Tipo de anestesia y tiempo quirúrgico.\n", "NORMAL_TEXT", False, True),
    ("Necesidad de técnicas complementarias.\n", "NORMAL_TEXT", False, True),
    ("\n", "NORMAL_TEXT", False, False),
    ("En Diagonal CQ ofrecemos un presupuesto personalizado tras la primera consulta con el Dr. Benítez Gomà, sin costes adicionales no previstos. Consulta también las opciones de financiación disponibles en la clínica.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Preguntas frecuentes sobre la liposucción de abdomen\n", "HEADING_2", True, False),

    ("H3: ¿Cuánto dura la recuperación de una liposucción de abdomen?\n", "HEADING_3", True, False),
    ("La recuperación básica suele ser de 7 a 14 días. La faja de compresión se lleva entre 4 y 6 semanas. La inflamación residual puede tardar entre 3 y 6 meses en desaparecer completamente, momento en que el resultado es definitivo.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: ¿Cuánto cuesta una liposucción de abdomen en Córdoba?\n", "HEADING_3", True, False),
    ("El precio depende de cada caso clínico. En Diagonal CQ facilitamos un presupuesto personalizado y detallado tras la primera consulta, sin compromiso.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: ¿La liposucción de abdomen deja cicatrices?\n", "HEADING_3", True, False),
    ("Las incisiones son muy pequeñas —de pocos milímetros— y se colocan en zonas estratégicas. Con una correcta cicatrización y el paso del tiempo, las marcas tienden a ser prácticamente imperceptibles.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: ¿La liposucción sirve para perder peso?\n", "HEADING_3", True, False),
    ("No. La liposucción es una técnica de remodelación corporal, no de adelgazamiento. Está diseñada para eliminar depósitos de grasa localizada en pacientes cerca de su peso ideal. No sustituye la dieta ni el ejercicio.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H3: ¿Es mejor la liposucción o la abdominoplastia?\n", "HEADING_3", True, False),
    ("Depende del caso. La liposucción está indicada cuando el problema principal es la grasa localizada con buena elasticidad cutánea. La abdominoplastia está indicada cuando además existe exceso de piel o diástasis abdominal. En algunos casos se combinan ambas técnicas. La indicación correcta solo puede establecerse tras una valoración médica.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("H2: Por qué elegir Diagonal CQ para tu liposucción en Córdoba\n", "HEADING_2", True, False),
    ("En Diagonal CQ acompañamos a pacientes de Córdoba, Sevilla y otras localidades de Andalucía con un enfoque individualizado, técnico y honesto.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("El Dr. Benítez Gomà te recibirá personalmente en la consulta, resolverá todas tus dudas y te ofrecerá una valoración honesta de lo que la liposucción puede o no puede hacer en tu caso. Si la liposucción no es la técnica más indicada para ti, te lo diremos antes de la intervención.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("¿Tienes dudas? Pide tu consulta sin compromiso.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),
    ("Texto revisado por el Dr. Benítez Gomà, especialista en Cirugía Plástica, Reparadora y Estética, nº colegiado 14/14/06121.\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("── ENLAZADO INTERNO SUGERIDO ──\n", "HEADING_2", False, False),
    ("[Consulta gratuita] → /contacto/\n", "NORMAL_TEXT", False, False),
    ("[Abdominoplastia en Córdoba] → /cirugia-estetica/contorno-corporal/abdominoplastia/\n", "NORMAL_TEXT", False, False),
    ("[Cirugía de contorno corporal] → /cirugia-estetica/contorno-corporal/\n", "NORMAL_TEXT", False, False),
    ("[Liposucción de muslos y brazos] → /cirugia-estetica/contorno-corporal/liposuccion/\n", "NORMAL_TEXT", False, False),
    ("\n", "NORMAL_TEXT", False, False),

    ("── SCHEMA JSON-LD ──\n", "HEADING_2", False, False),
    ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "MedicalProcedure",\n  "name": "Liposucción de abdomen y flancos",\n  "description": "Técnica quirúrgica de contorno corporal que elimina la grasa localizada del abdomen y los flancos mediante cánulas de precisión.",\n  "procedureType": "https://health-lifesci.schema.org/SurgicalProcedure",\n  "bodyLocation": "Abdomen y flancos",\n  "followup": "Faja de compresión 4-6 semanas. Revisiones postoperatorias periódicas.",\n  "preparation": "Análisis preoperatorios, valoración anestésica y consulta previa con el cirujano.",\n  "performer": {\n    "@type": "Physician",\n    "name": "Dr. Benítez Gomà",\n    "medicalSpecialty": "PlasticSurgery"\n  },\n  "availableService": {\n    "@type": "MedicalClinic",\n    "name": "Diagonal CQ",\n    "address": {\n      "@type": "PostalAddress",\n      "addressLocality": "Córdoba",\n      "addressCountry": "ES"\n    }\n  }\n}\n</script>\n', "NORMAL_TEXT", False, False),
]

# Construir texto y rastrear rangos
full_text = ""
style_ranges = []   # (start, end, style, bold)
bullet_ranges = []  # (start, end)

cursor = 1
for text, style, bold, bullet in BLOCKS:
    start = cursor
    end = cursor + len(text)
    text_end = end - 1 if text.endswith("\n") else end

    if style != "NORMAL_TEXT" or bold:
        style_ranges.append((start, text_end, style, bold))

    if bullet:
        bullet_ranges.append((start, text_end))

    full_text += text
    cursor = end

# Paso 1: limpiar
data = req.get(BASE + '?includeTabsContent=true', headers=hdr_get).json()
for tab in data.get('tabs', []):
    if tab['tabProperties']['tabId'] == TAB_ID:
        content = tab['documentTab']['body']['content']
        end_idx = content[-1]['endIndex']
        if end_idx > 2:
            r = req.post(BASE + ':batchUpdate', headers=hdr, json={'requests': [
                {'deleteContentRange': {'range': {'startIndex': 1, 'endIndex': end_idx - 1, 'tabId': TAB_ID}}}
            ]})
            print('Limpiado:', r.status_code)

# Paso 2: insertar texto
r = req.post(BASE + ':batchUpdate', headers=hdr, json={'requests': [
    {'insertText': {'location': {'index': 1, 'tabId': TAB_ID}, 'text': full_text}}
]})
print('Texto insertado:', r.status_code)
if r.status_code != 200:
    print(r.text[:300])
    exit(1)

# Paso 3: todo el texto — NORMAL_TEXT, tamaño 11, negro
total_len = cursor - 1
format_requests = [
    # Todo texto normal
    {
        'updateParagraphStyle': {
            'range': {'startIndex': 1, 'endIndex': total_len, 'tabId': TAB_ID},
            'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
            'fields': 'namedStyleType'
        }
    },
    # Tamaño 11pt y color negro para todo
    {
        'updateTextStyle': {
            'range': {'startIndex': 1, 'endIndex': total_len, 'tabId': TAB_ID},
            'textStyle': {
                'fontSize': {'magnitude': 11, 'unit': 'PT'},
                'foregroundColor': {'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}},
                'bold': False
            },
            'fields': 'fontSize,foregroundColor,bold'
        }
    }
]
r = req.post(BASE + ':batchUpdate', headers=hdr, json={'requests': format_requests})
print('Formato base:', r.status_code)

# Aplicar negrita solo a las líneas H1/H2/H3
bold_requests = []
for start, end, style, bold in style_ranges:
    if bold:
        bold_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end, 'tabId': TAB_ID},
                'textStyle': {'bold': True},
                'fields': 'bold'
            }
        })

for i in range(0, len(bold_requests), 50):
    r = req.post(BASE + ':batchUpdate', headers=hdr, json={'requests': bold_requests[i:i+50]})
    print(f'Negritas lote {i//50+1}: {r.status_code}')

# Paso 4: bullet points — agrupar rangos consecutivos y aplicar
bullet_requests = []
for start, end in bullet_ranges:
    bullet_requests.append({
        'createParagraphBullets': {
            'range': {'startIndex': start, 'endIndex': end, 'tabId': TAB_ID},
            'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
        }
    })

for i in range(0, len(bullet_requests), 50):
    r = req.post(BASE + ':batchUpdate', headers=hdr, json={'requests': bullet_requests[i:i+50]})
    print(f'Bullets lote {i//50+1}: {r.status_code}')
    if r.status_code != 200:
        print(r.text[:200])

print('¡Hecho!')
