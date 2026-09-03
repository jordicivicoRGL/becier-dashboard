# -*- coding: utf-8 -*-
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open('credentials/token_backup_20260814.json', encoding='utf-8') as f:
    token_data = json.load(f)
with open('credentials/client_secret.json', encoding='utf-8') as f:
    secret_data = json.load(f)

web_or_installed = secret_data.get('web') or secret_data.get('installed')

credentials = Credentials(
    token=token_data.get('token'),
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=web_or_installed['client_id'],
    client_secret=web_or_installed['client_secret'],
    scopes=token_data.get('scopes'),
)
credentials.refresh(Request())
service = build('sheets', 'v4', credentials=credentials)

SHEET_ID = '184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4'
TAB = 'VIDEOS'

header_result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f'{TAB}!3:3'
).execute()
headers = header_result.get('values', [[]])[0]
col = {h: i for i, h in enumerate(headers)}
n_cols = len(headers)

ads = [
    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Persona',
         Problema='Mi gato tiene el pelo apagado y se le nota reseca la piel.',
         Hook='¿Tu gato tiene el pelo sin brillo y se rasca más de lo normal?',
         Desenlace='El pienso seco aporta poca grasa buena y casi nada de humedad; sin esos nutrientes la piel se reseca y el pelo pierde brillo. Food for Joe se cocina con más de un 70% de humedad natural y ácidos grasos que nutren la piel desde dentro.',
         Cierre='Descubre en 1 minuto el plan de tu gato con el quiz de Food for Joe.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Veterinario',
         Hook='El pelo y la piel son el primer síntoma visible de una mala alimentación.',
         Desenlace='Veterinario a cámara explicando que la falta de grasas de calidad y humedad en la dieta se refleja directamente en el pelo; los ácidos grasos de FFJ trabajan desde dentro.',
         Cierre='Pregúntale a nuestro equipo veterinario qué receta le conviene.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Before/After', Tipo='Persona',
         Hook='Este es el pelo de mi gato a las 3 semanas de cambiar su comida.',
         Desenlace='Contraste visual del pelo apagado antes y brillante después; el dueño explica el cambio de pienso a receta natural.',
         Cierre='Empieza el cambio hoy con el plan personalizado.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Llevaba meses probando champús para gatos y el problema no era el pelo, era el pienso.',
         Desenlace='Cliente cuenta que tras cambiar de alimentación notó el pelo más suave y menos caída en pocas semanas.',
         Cierre='Lee más experiencias reales en Trustpilot y prueba tu plan.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona (founder)',
         Hook='Cuando vimos el pelo de nuestro gato en la mesa cada día, decidimos cambiar su comida.',
         Desenlace='El founder cuenta el origen personal del producto y por qué formularon FFJ con veterinarios para cuidar piel y pelo desde la nutrición.',
         Cierre='Así nació Food for Joe. Descubre el plan de tu gato.'),

    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Persona',
         Problema='Quiero darle algo natural pero no tengo tiempo de cocinarle nada.',
         Hook='No tienes tiempo de cocinarle a tu gato, pero tampoco quieres darle cualquier cosa.',
         Desenlace='FFJ ya viene cocinado y congelado; solo hay que descongelar y servir, con la misma calidad que cocinar en casa sin el tiempo que exige.',
         Cierre='Recibe raciones listas cada mes, sin cocinar nada.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Demostración', Tipo='Persona',
         Hook='Así es descongelar la comida de mi gato, de la nevera al plato.',
         Desenlace='Se muestra el proceso real: sacar del congelador, descongelar en la nevera, servir; énfasis en la simplicidad del día a día.',
         Cierre='Pruébalo tú también, sin complicarte la vida.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Tutorial', Tipo='Persona',
         Hook='Así es la rutina real de dar de comer natural a mi gato en menos de 1 minuto.',
         Desenlace='Paso a paso: descongelar, servir la ración ya personalizada; sin cocinar ni pesar nada porque el plan ya viene calculado.',
         Cierre='Consigue el tuyo con el quiz personalizado.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Comparativo', Tipo='Persona',
         Hook='Cocinar para tu gato cada día vs. abrir la nevera y servir.',
         Desenlace='Comparación entre cocinar casero (tiempo, dudas nutricionales) y FFJ (formulado por veterinarios, listo para servir).',
         Cierre='La comida casera, sin cocinar cada día.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona (founder)',
         Hook='Queríamos darle a nuestro gato algo casero, pero ninguno de los dos cocina.',
         Desenlace='El founder explica que creó FFJ para dueños que quieren calidad real sin tiempo para cocinar, con recetas formuladas por veterinarios.',
         Cierre='Así nació el plan que hace el trabajo por ti.'),

    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Problema='Mi gato es muy especial con la comida, no sé si se la va a comer.',
         Hook='Mi gato dejaba el plato a medias con todo... hasta que probó esto.',
         Desenlace='Cliente cuenta que su gato selectivo aceptó la receta desde el primer día por el aroma y la textura natural.',
         Cierre='Descubre si a tu gato también le va a encantar.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Demostración', Tipo='Persona',
         Hook='Grabé la primera vez que le di esta comida a mi gato, que nunca come nada nuevo.',
         Desenlace='Vídeo real del gato oliendo y comiendo, reacción genuina, sin cortes forzados.',
         Cierre='Pide tu plan y compruébalo con tu propio gato.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Veterinario',
         Hook='Los gatos rechazan la comida nueva por el olfato, no por capricho.',
         Desenlace='Veterinario explica que los gatos son especialmente sensibles al olor y la textura, y que las recetas cocinadas y frescas suelen tener mejor aceptación que el pienso seco.',
         Cierre='Habla con nuestro equipo si tu gato es especialmente selectivo.'),
    dict(Target='Gato', Funnel='BOF', Ángulo='Social proof', Tipo='Persona',
         Hook="Miles de gatos 'imposibles' ya comen esto cada día.",
         Desenlace='Mención de la valoración real en Trustpilot y de dueños que llegaron a FFJ tras varios intentos fallidos con otras marcas.',
         Cierre='Súmate a los que ya encontraron lo que su gato sí come.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Before/After', Tipo='Persona',
         Hook='De dejar el plato a medias a pedir más: así cambió mi gato.',
         Desenlace='Contraste entre la rutina anterior (rechazo, comida sin tocar) y la actual (plato vacío, interés real por la comida).',
         Cierre='Encuentra la receta que tu gato sí quiere comer.'),

    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Veterinario',
         Problema='No sé cuánto pienso está comiendo realmente ni si es la cantidad correcta.',
         Hook='¿Sabes realmente cuánto come tu gato al día?',
         Desenlace='El pienso a libre disposición dificulta controlar el peso; FFJ calcula la ración exacta según peso, edad y actividad.',
         Cierre='Calcula la ración exacta de tu gato con el quiz.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Persona',
         Hook='Con el pienso a libre disposición es casi imposible saber cuánto come tu gato.',
         Desenlace='Sin raciones medidas es fácil que el gato coma de más; FFJ viene con la ración diaria ya calculada.',
         Cierre='Deja de calcular a ojo. Empieza con la ración exacta.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Mi gato bajó de peso sin que yo tuviera que restringirle nada.',
         Desenlace='Cliente cuenta que al pasar a raciones personalizadas su gato llegó a su peso ideal de forma natural, sin pasar hambre.',
         Cierre='Descubre el plan pensado para el peso de tu gato.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Tutorial', Tipo='Persona',
         Hook='Así se sirve la ración exacta que necesita mi gato, cada día.',
         Desenlace='Se muestra el proceso de servir la porción indicada según el plan personalizado, sin pesar ni calcular nada.',
         Cierre='Recibe raciones ya calculadas para tu gato.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Comparativo', Tipo='Veterinario',
         Hook='Pienso a libre disposición vs. ración calculada: la diferencia está en el peso.',
         Desenlace='Comparación de ambos métodos y su impacto en el control de peso a largo plazo, con recomendación veterinaria de raciones controladas.',
         Cierre='Consulta la ración ideal para tu gato con nuestro equipo.'),

    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Veterinario',
         Problema='Me preocupa que algo natural no cubra todo lo que mi gato necesita.',
         Hook='Natural no significa incompleto: así se formula una dieta felina completa.',
         Desenlace='El veterinario explica el estándar FEDIAF y cómo las recetas de FFJ se formulan para cubrir todos los requerimientos nutricionales del gato, no solo por "ser natural".',
         Cierre='Consulta la ficha nutricional completa de cada receta.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona',
         Hook='No basta con que sea natural, tiene que ser completo. Por eso lo hicimos así.',
         Desenlace='El founder explica que el equipo de veterinarios y nutricionistas formula cada receta siguiendo FEDIAF, no solo con ingredientes "sanos" al azar.',
         Cierre='Descubre cómo formulamos cada receta.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Demostración', Tipo='Persona',
         Hook='Esto es lo que hay detrás de cada ración de mi gato.',
         Desenlace='Se muestra la ficha técnica/etiqueta del producto en pantalla, señalando el sello FEDIAF y el desglose nutricional.',
         Cierre='Revisa tú mismo la composición antes de decidir.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Comparativo', Tipo='Veterinario',
         Hook="Pienso 'natural' de supermercado vs. receta formulada por veterinarios: no es lo mismo.",
         Desenlace='Diferencia entre el marketing de "natural" sin respaldo nutricional y una receta certificada con estándares FEDIAF.',
         Cierre='Elige una receta con respaldo veterinario real.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Antes de cambiarle la comida, le pregunté a mi veterinario si era seguro.',
         Desenlace='Cliente cuenta que consultó con su veterinario antes de cambiar y confirmó que la receta cumplía con los estándares nutricionales necesarios.',
         Cierre='Cambia con la tranquilidad de una receta certificada.'),

    dict(Target='Gato', Funnel='TOF', Ángulo='Tutorial', Tipo='Veterinario',
         Problema='Me preocupa el proceso de cambiarle la comida, no sé cómo hacerlo bien.',
         Hook='Así se cambia la comida de un gato sin que la rechace.',
         Desenlace='El veterinario explica la transición gradual (mezclar cantidades crecientes durante varios días) para evitar rechazo y problemas digestivos.',
         Cierre='Te acompañamos en cada paso de la transición.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Persona',
         Hook='Cambiarle la comida a mi gato me daba miedo, así que investigué cómo hacerlo bien.',
         Desenlace='El dueño relata el proceso real de transición siguiendo la guía de FFJ, sin sustos ni rechazo.',
         Cierre='Recibe la guía de transición con tu primer pedido.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Mi gato es de los que rechaza todo lo nuevo, y aun así hicimos la transición sin problema.',
         Desenlace='Testimonio real de un gato "difícil" que se adaptó bien siguiendo el proceso gradual recomendado.',
         Cierre='Empieza la transición con confianza.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Demostración', Tipo='Persona',
         Hook='Día 1 vs. día 7 de cambiar la comida de mi gato.',
         Desenlace='Progresión real de la mezcla de alimento antiguo y nuevo durante la semana de transición.',
         Cierre='Sigue el mismo proceso con tu gato.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona',
         Hook='Sabemos que los gatos odian el cambio, por eso diseñamos la transición pensando en ellos.',
         Desenlace='El founder explica que el equipo pensó específicamente en la neofobia felina al diseñar el proceso de cambio y el acompañamiento al cliente.',
         Cierre='Descubre cómo te acompañamos en el cambio.'),

    dict(Target='Gato', Funnel='TOF', Ángulo='Emocional', Tipo='Persona',
         Problema='Siento que el pienso de toda la vida es solo comida industrial.',
         Hook='Le doy de comer lo mismo desde hace años sin pensarlo, y eso me pesa.',
         Desenlace='El dueño reflexiona sobre dar por sentado el pienso de siempre sin cuestionar qué contiene realmente, y cómo decidió cambiarlo.',
         Cierre='Dale algo que sepas exactamente qué es.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Veterinario',
         Hook='El pienso seco convencional puede tener menos de un 12% de humedad natural.',
         Desenlace='Diferencia entre un pienso ultraprocesado con harinas y subproductos genéricos, y una receta cocinada con más de un 70% de humedad e ingredientes identificables.',
         Cierre='Revisa qué lleva realmente lo que le das a tu gato.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Comparativo', Tipo='Persona',
         Hook="Ingredientes que reconoces vs. 'harinas y subproductos animales'.",
         Desenlace='Comparar la lista de ingredientes de un pienso genérico frente a la de Food for Joe, mostrando en pantalla ambas etiquetas.',
         Cierre='Lee la etiqueta antes de decidir.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona',
         Hook='Empezamos esto porque no sabíamos qué llevaba realmente el pienso de nuestro gato.',
         Desenlace='El founder cuenta el origen de la marca: la falta de transparencia en el etiquetado de los piensos convencionales y la decisión de cocinar con ingredientes reales.',
         Cierre='Conoce el origen de cada ingrediente que usamos.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Dejé de sentirme culpable en cuanto vi lo que llevaba de verdad su comida.',
         Desenlace='El cliente relata cómo el cambio a una receta con ingredientes reconocibles le dio tranquilidad frente a la culpa de dar "algo industrial".',
         Cierre='Dale la tranquilidad de una comida transparente.'),

    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Veterinario',
         Problema='Las heces de mi gato no tienen buena pinta y el olor es muy fuerte.',
         Hook='Las heces de tu gato dicen mucho más de lo que crees sobre su comida.',
         Desenlace='Heces blandas o de olor fuerte suelen indicar mala digestibilidad del pienso; una dieta más digestible mejora visiblemente ese síntoma.',
         Cierre='Consulta si el cambio de dieta puede ayudar a tu gato.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='En dos semanas noté la diferencia... en el arenero.',
         Desenlace='El cliente cuenta, con naturalidad, cómo mejoraron las heces y el olor tras el cambio de alimentación.',
         Cierre='Comprueba tú mismo el cambio en pocas semanas.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Persona',
         Hook='Más del 70% de humedad natural vs. menos del 12% del pienso seco: la digestión nota la diferencia.',
         Desenlace='Una dieta con más humedad y menos ingredientes de relleno es más fácil de digerir, lo que se refleja en heces mejor formadas.',
         Cierre='Dale una digestión más fácil desde la primera semana.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Before/After', Tipo='Persona',
         Hook='Esto es lo que cambió en el arenero de mi gato tras cambiarle la comida.',
         Desenlace='Relato honesto del contraste entre antes y después, centrado en consistencia y olor, sin imágenes explícitas.',
         Cierre='Empieza el cambio y notarás la diferencia tú también.'),
    dict(Target='Gato', Funnel='TOF', Ángulo='Founder', Tipo='Persona',
         Hook='Cuando varios clientes nos escribieron sobre lo mismo, supimos que íbamos por buen camino.',
         Desenlace='El founder comenta que la mejora digestiva es uno de los comentarios más repetidos por clientes, y lo conecta con la formulación de las recetas.',
         Cierre='Descubre por qué tantos gatos digieren mejor con FFJ.'),

    dict(Target='Gato', Funnel='TOF', Ángulo='Dato/Estadística', Tipo='Veterinario',
         Problema='Sé que mi gato bebe poca agua pero no sé si es un riesgo real.',
         Hook='Los gatos apenas beben agua por instinto, y eso puede pasar factura a los riñones.',
         Desenlace='Los gatos, como cazadores de presas, obtienen la mayor parte del agua de su alimento; con pienso seco esa fuente casi desaparece.',
         Cierre='Pregunta a nuestro equipo cómo mejorar la hidratación de tu gato.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Problema→Solución', Tipo='Persona',
         Hook='Mi gato casi no toca el bebedero, así que empecé a preocuparme por su hidratación.',
         Desenlace='Cambiar a una comida con más humedad natural ayuda a cubrir esa falta de ingesta de agua directa.',
         Cierre='Dale hidratación real desde el plato, no solo desde el bebedero.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Comparativo', Tipo='Veterinario',
         Hook='8-12% de humedad en el pienso seco frente a más del 70% en una receta cocinada.',
         Desenlace='Comparación directa de humedad entre ambos tipos de alimento y su impacto en la hidratación general del gato.',
         Cierre='Elige una fuente extra de hidratación en cada comida.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Testimonial', Tipo='Testimonio',
         Hook='Mi gato nunca fue de beber mucha agua, pero desde que come esto ya no me preocupa tanto.',
         Desenlace='El cliente relata la tranquilidad de saber que su gato recibe hidratación a través de la comida, no solo del bebedero.',
         Cierre='Dale una fuente extra de agua en cada plato.'),
    dict(Target='Gato', Funnel='MOF', Ángulo='Demostración', Tipo='Persona',
         Hook='Así de húmeda es la comida real de un gato, comparada con el pienso de toda la vida.',
         Desenlace='Se muestra en pantalla la textura jugosa de la receta cocinada frente al pienso seco, remarcando visualmente la diferencia de humedad.',
         Cierre='Compruébalo tú mismo con el plan de tu gato.'),
]

assert len(ads) == 45, len(ads)

rows = []
for ad in ads:
    row = [''] * n_cols
    for field, value in ad.items():
        if field in col:
            row[col[field]] = value
    rows.append(row)

result = service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f'{TAB}!A:A',
    valueInputOption='USER_ENTERED',
    insertDataOption='INSERT_ROWS',
    body={'values': rows}
).execute()

print('Updated range:', result.get('updates', {}).get('updatedRange'))
print('Rows written:', len(rows))
