# -*- coding: utf-8 -*-
"""
Script para escribir el texto SEO "Liposucción en Córdoba" de Diagonal CQ en Google Docs.
Formato: Arial 11, NORMAL_TEXT, prefijos H1:/H2:/H3: en negrita, tabla real.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1QN41nJcgLGP_Hr4_Mhwi2g1ShkjPZwc7xO50-OPI4CY"
TAB_ID = "t.bi6874uednx7"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita)
# ---------------------------------------------------------------------------
BLOCKS_BEFORE_TABLE = [
    ("Meta title: Liposucción en Córdoba | Diagonal CQ", False),
    ("Meta description: Liposucción en Córdoba con el Dr. Joan Benítez: elimina grasa localizada y remodela tu silueta con técnica láser. Valoración personalizada en Diagonal CQ.", False),
    ("URL slug: /cirugia-estetica/liposuccion/ (se mantiene la URL existente)", False),
    ("", False),
    ("H1: Liposucción en Córdoba", True),
    ("La liposucción es la intervención de cirugía plástica de referencia para eliminar de forma definitiva la grasa localizada que no responde a la dieta ni al ejercicio. En Diagonal CQ, en Córdoba, la realizamos bajo la dirección del Dr. Joan Benítez, con la posibilidad de asistencia por láser cuando el caso lo permite, y siempre desde una valoración honesta de lo que esta cirugía puede y no puede conseguir.", False),
    ("", False),
    ("Es importante aclararlo desde el principio: la liposucción no es una técnica para perder peso ni forma parte del tratamiento de la obesidad. Su objetivo es mejorar la armonía del contorno corporal eliminando acúmulos de grasa localizados y resistentes, no sustituir hábitos de vida saludables.", False),
    ("", False),
    ("H2: ¿Qué es la liposucción y para qué sirve?", True),
    ("La liposucción es una intervención quirúrgica que elimina de forma definitiva los acúmulos localizados de tejido adiposo mediante aspiración. A diferencia de los tratamientos no invasivos de reducción de grasa, sus resultados sobre la grasa eliminada son permanentes, siempre que el paciente mantenga un peso y unos hábitos de vida estables tras la intervención.", False),
    ("", False),
    ("Según la Sociedad Española de Cirugía Plástica, Reparadora y Estética (SECPRE), la liposucción debe entenderse como una técnica de remodelación corporal y no como un tratamiento de adelgazamiento, y debe realizarse siempre por un cirujano plástico cualificado y en un entorno hospitalario seguro. Es, junto con el aumento de pecho, uno de los procedimientos de cirugía estética más solicitados a nivel mundial, según datos recogidos habitualmente por sociedades internacionales de cirugía plástica.", False),
    ("", False),
    ("Con esta técnica se consigue una mejora en la armonía del contorno corporal mediante la modelación de la silueta, pero no resuelve un problema global de sobrepeso u obesidad derivado de hábitos de vida inadecuados. Por eso, en Diagonal CQ recomendamos que el paciente mantenga un peso lo más cercano posible a su peso habitual antes de la intervención.", False),
    ("", False),
    ("H2: Zonas del cuerpo que se pueden tratar con liposucción", True),
    ("La liposucción es eficaz para tratar la grasa localizada en múltiples zonas del cuerpo. Las más habituales son:", False),
    ("", False),
    ("— Abdomen y flancos (cintura).", False),
    ("— Caderas y región lumbar.", False),
    ("— Piernas, rodillas y cara interna de los muslos.", False),
    ("— Brazos.", False),
    ("— Región cervical anterior y papada.", False),
    ("", False),
    ("La combinación de zonas a tratar y la técnica más adecuada para cada una se define siempre en la consulta de valoración, en función de la distribución individual de la grasa y de la calidad de la piel del paciente.", False),
    ("", False),
    ("H2: Técnicas de liposucción disponibles en Diagonal CQ", True),
    ("", False),
    ("H3: Liposucción tradicional", True),
    ("Consiste en la aspiración por vacío de la grasa mediante cánulas de entre 2 y 5 mm de diámetro, introducidas a través de pequeñas incisiones de 3 a 4 mm cercanas a la zona a tratar. Es la técnica más consolidada, con décadas de uso clínico, y sigue siendo la opción de referencia cuando se requiere eliminar volúmenes de grasa mayores.", False),
    ("", False),
    ("H3: Liposucción asistida (vibración, ultrasonidos o láser)", True),
    ("El cirujano puede complementar la técnica tradicional con sistemas de vibración mecánica, ultrasonidos o energía láser para facilitar la disgregación de la grasa antes de su aspiración. En Diagonal CQ asistimos los procedimientos de liposucción con láser, una técnica que permite un procedimiento menos invasivo, mejor eliminación de la grasa en zonas difíciles o ya tratadas previamente, y una mejor adaptación de la piel tras la intervención gracias al efecto de calentamiento controlado sobre la dermis.", False),
    ("", False),
    ("Si tu caso presenta flacidez cutánea asociada o buscas una recuperación más discreta, puedes consultar en detalle nuestra página de liposucción asistida por láser, donde explicamos esta técnica en profundidad.", False),
    ("", False),
]

# Tabla comparativa de técnicas
TABLE_HEADERS = ["Técnica", "Mecanismo", "Indicación principal", "Incisiones", "Recuperación orientativa*"]
TABLE_ROWS = [
    ["Liposucción tradicional", "Aspiración mecánica con cánulas", "Volúmenes de grasa moderados o grandes", "3-4 mm", "2-3 semanas"],
    ["Liposucción asistida por láser", "Aspiración + energía láser", "Zonas con flacidez o de precisión, retoques", "3-4 mm", "Ligeramente inferior a la tradicional"],
]

BLOCKS_AFTER_TABLE = [
    ("", False),
    ("*La duración indicada es orientativa y puede variar según cada caso clínico.", False),
    ("", False),
    ("H2: Beneficios reales de la liposucción", True),
    ("Cuando se realiza con una indicación adecuada, la liposucción ofrece beneficios contrastados en la remodelación corporal:", False),
    ("", False),
    ("— Eliminación definitiva de la grasa localizada tratada, siempre que se mantenga un peso estable.", False),
    ("— Mejora de la proporción y la armonía del contorno corporal.", False),
    ("— Resultado más nítido en zonas donde la dieta y el ejercicio no consiguen resultados, por la resistencia genética de ciertos depósitos de grasa.", False),
    ("— Puede combinarse con otras intervenciones, como la abdominoplastia o la mastopexia, dentro de un mismo plan de remodelación corporal.", False),
    ("— Mejora de la autopercepción de la imagen corporal, siempre con expectativas realistas previamente valoradas en consulta.", False),
    ("", False),
    ("Los resultados dependen de la técnica empleada, la zona tratada, la elasticidad de la piel y la respuesta individual de cada paciente. La valoración médica previa es imprescindible para definir expectativas ajustadas a cada caso.", False),
    ("", False),
    ("H2: ¿Soy candidato o candidata a una liposucción?", True),
    ("La cantidad de grasa que puede extraerse y el resultado final dependen de varios factores individuales que el Dr. Joan Benítez valora en la consulta previa:", False),
    ("", False),
    ("— Constitución y distribución de la grasa en el cuerpo.", False),
    ("— Calidad y elasticidad de la piel de la zona a tratar.", False),
    ("— Edad y estado de salud general.", False),
    ("", False),
    ("La evaluación de la elasticidad cutánea de la zona a intervenir es esencial. Cuando la piel tiene buena elasticidad, se retrae de forma satisfactoria tras eliminar la grasa localizada, adaptándose al nuevo contorno. Cuando la piel es menos elástica, la cantidad de grasa que se puede aspirar es menor, para evitar que quede relajada formando irregularidades o pliegues no deseados.", False),
    ("", False),
    ("H3: Contraindicaciones", True),
    ("La liposucción puede no estar indicada o debe posponerse en pacientes con:", False),
    ("", False),
    ("— Enfermedades sistémicas no controladas (diabetes descompensada, problemas cardiorrespiratorios graves).", False),
    ("— Trastornos de la coagulación.", False),
    ("— Tabaquismo activo, que compromete significativamente la cicatrización.", False),
    ("— Embarazo.", False),
    ("— Expectativas no realistas, especialmente confundir esta cirugía con un tratamiento de pérdida de peso.", False),
    ("", False),
    ("La indicación definitiva se establece siempre tras el estudio preoperatorio y la valoración individual del Dr. Joan Benítez.", False),
    ("", False),
    ("H2: Riesgos y posibles complicaciones", True),
    ("Como toda intervención quirúrgica, la liposucción conlleva riesgos generales que deben conocerse antes de tomar la decisión:", False),
    ("", False),
    ("— Infección postoperatoria de las incisiones.", False),
    ("— Hematoma o seroma (acumulación de líquido en la zona tratada).", False),
    ("— Irregularidades o asimetrías en el contorno de la zona tratada.", False),
    ("— Alteración temporal de la sensibilidad en la zona intervenida.", False),
    ("— Complicaciones propias de la anestesia utilizada.", False),
    ("", False),
    ("El estudio preoperatorio y la valoración individual del paciente tienen precisamente el objetivo de minimizar estos riesgos, descartando previamente cualquier problema de salud que los aumente.", False),
    ("", False),
    ("H2: ¿Cómo es el proceso de la liposucción en Diagonal CQ?", True),
    ("1. Consulta y valoración inicial: el Dr. Joan Benítez evalúa las zonas a tratar, la elasticidad de la piel, tu estado de salud y tus expectativas, y determina si eres candidato y qué técnica es la más adecuada.", False),
    ("2. Estudio preoperatorio: se realizan las pruebas necesarias para descartar problemas de salud que contraindiquen o condicionen la cirugía.", False),
    ("3. Planificación quirúrgica: se definen las zonas exactas a tratar y la técnica —tradicional, asistida por láser o combinada— más adecuada para tu caso.", False),
    ("4. Intervención: se realiza en un hospital, con una duración de entre 30 y 90 minutos según la cantidad de grasa a eliminar y las zonas a tratar. El tipo de anestesia habitual es anestesia local y sedación asistida por un anestesista; la raquianestesia o la anestesia general se reservan para casos más complejos o cuando se asocia a otra intervención. Se realizan 3 o 4 pequeñas incisiones de 3-4 mm por las que se introducen las cánulas de aspiración.", False),
    ("5. Postoperatorio inmediato: se coloca un vendaje compresivo que evita edemas y cardenales, aporta comodidad y ayuda a la piel a adaptarse al nuevo contorno.", False),
    ("6. Seguimiento: revisiones programadas para valorar la evolución y, si el caso lo requiere, apoyo con radiofrecuencia (Velashape III) en el postoperatorio tardío para mejorar la adaptación de la piel.", False),
    ("", False),
    ("[CTA intermedio] ¿Quieres saber si eres candidato a una liposucción? Solicita tu valoración en Diagonal CQ, en Córdoba, sin compromiso. [BOTÓN: Pedir cita]", False),
    ("", False),
    ("H2: Recuperación y cuidados tras la liposucción", True),
    ("", False),
    ("H3: Primera semana", True),
    ("La zona tratada es ligeramente dolorosa al tacto, aunque no se producen dolores intensos ni espontáneos. Se recomienda no realizar actividades laborales físicamente exigentes durante estos primeros días y mantener el vendaje o la prenda compresiva según la pauta indicada.", False),
    ("", False),
    ("H3: Segunda a cuarta semana", True),
    ("En casos seleccionados se recomiendan prendas compresivas entre 2 y 4 semanas, junto con fisioterapia de apoyo. La actividad deportiva habitual puede reiniciarse a partir de la tercera semana, momento en el que también se empiezan a apreciar los primeros cambios producidos por la intervención, a medida que el edema postoperatorio disminuye.", False),
    ("", False),
    ("H3: A partir del primer mes", True),
    ("La piel continúa adaptándose progresivamente al nuevo contorno. El resultado se considera definitivo a los 6 meses de la intervención. En casos con menor elasticidad cutánea, en Diagonal CQ asistimos el postoperatorio tardío con radiofrecuencia (Velashape III) para mejorar la fase de recuperación y adaptación de la piel.", False),
    ("", False),
    ("Señales que requieren consulta médica:", False),
    ("", False),
    ("— Fiebre superior a 38 °C.", False),
    ("— Dolor intenso que no cede con la analgesia habitual.", False),
    ("— Enrojecimiento o calor excesivo en la zona intervenida.", False),
    ("", False),
    ("H2: Liposucción y cirugías complementarias", True),
    ("La liposucción trata la grasa localizada, pero no corrige el exceso de piel ni la flacidez de la pared abdominal. Por eso, en determinados casos —especialmente tras embarazos o pérdidas de peso importantes— se combina con otras intervenciones dentro de un mismo plan de remodelación corporal:", False),
    ("", False),
    ("— Abdominoplastia: retira el exceso de piel y refuerza la musculatura abdominal cuando la liposucción sola no es suficiente.", False),
    ("— Mastopexia (elevación de pecho): puede combinarse cuando el plan de remodelación incluye también el contorno del pecho.", False),
    ("", False),
    ("La decisión de combinar procedimientos se toma siempre de forma individualizada, valorando el beneficio y la seguridad de cada caso concreto.", False),
    ("", False),
    ("H2: Preguntas frecuentes sobre la liposucción en Córdoba", True),
    ("", False),
    ("H3: ¿La liposucción sirve para perder peso?", True),
    ("No. El objetivo de la liposucción no es la pérdida de peso ni forma parte del tratamiento de la obesidad. Es recomendable mantener un peso lo más cercano posible al habitual antes de la intervención; la técnica sirve para mejorar la armonía del contorno corporal, no para adelgazar.", False),
    ("", False),
    ("H3: ¿Cuánta grasa puede extraerse en una liposucción?", True),
    ("Depende de la constitución, distribución de la grasa, elasticidad de la piel, edad y estado de salud. Cuanta mejor sea la elasticidad cutánea, mayor es la cantidad de grasa que puede eliminarse con un buen resultado estético, valorado siempre de forma individual en consulta.", False),
    ("", False),
    ("H3: ¿Cómo es la intervención de liposucción?", True),
    ("Se realiza en un hospital, con una duración de entre 30 y 90 minutos según la zona y la cantidad de grasa a tratar, habitualmente con anestesia local y sedación. Se practican 3 o 4 pequeñas incisiones por las que se introducen las cánulas de aspiración.", False),
    ("", False),
    ("H3: ¿Cómo es el postoperatorio de la liposucción?", True),
    ("Se coloca un vendaje compresivo que evita edemas y cardenales. La zona es ligeramente dolorosa al tacto durante la primera semana, sin dolor intenso ni espontáneo. En casos seleccionados se recomiendan prendas compresivas de 2 a 4 semanas.", False),
    ("", False),
    ("H3: ¿Cuándo se ven los resultados de la liposucción?", True),
    ("Los primeros cambios se aprecian a partir de las 3 semanas, cuando el edema postoperatorio empieza a disminuir. El resultado se considera definitivo a los 6 meses tras la intervención.", False),
    ("", False),
    ("H3: ¿Qué diferencia hay entre la liposucción tradicional y la liposucción láser?", True),
    ("La liposucción tradicional aspira la grasa de forma mecánica con cánulas. La liposucción asistida por láser combina esa aspiración con energía láser, lo que permite un procedimiento menos invasivo y una mejor adaptación de la piel, especialmente en zonas difíciles o ya tratadas previamente.", False),
    ("", False),
    ("H3: ¿La liposucción en Córdoba tiene financiación o facilidades de pago?", True),
    ("En Diagonal CQ podemos informarte sobre las opciones de financiación disponibles en la consulta de valoración, adaptadas a las zonas a tratar y a la técnica elegida.", False),
    ("", False),
    ("H2: Por qué elegir Diagonal CQ para tu liposucción en Córdoba", True),
    ("En Diagonal CQ no planteamos la liposucción como una solución de adelgazamiento, sino como una cirugía de remodelación corporal con criterios médicos rigurosos. El Dr. Joan Benítez valora cada caso de forma individual, incluyendo la elasticidad de la piel, para decidir con honestidad qué técnica y qué cantidad de grasa a eliminar ofrecen el mejor resultado posible.", False),
    ("", False),
    ("Si estás valorando una liposucción en Córdoba y quieres una opinión médica clara sobre tu caso, solicita una valoración personalizada sin compromiso.", False),
    ("", False),
    ("[CTA final] Solicita tu valoración personalizada en Córdoba [BOTÓN: Pedir cita]", False),
    ("", False),
    ("Doctor responsable: Dr. Joan Ramon Benítez Gomà", False),
    ("Especialidad médica: Cirugía Plástica, Reparadora y Estética", False),
    ("Número de colegiado: 146121", False),
    ("Registro sanitario del centro: NICA 54005", False),
    ("", False),
    ("Revisado y supervisado por el Dr. Joan Ramon Benítez Gomà, especialista en Cirugía Plástica, Reparadora y Estética, nº colegiado 146121. Última revisión: julio de 2026.", False),
    ("Sugerencia: enlazar la autoría a /equipo-medico/ para reforzar E-E-A-T.", False),
    ("", False),
    ("El contenido de esta página tiene carácter informativo y no sustituye la consulta médica personalizada. Ante cualquier duda sobre tu caso, consulta con un especialista cualificado.", False),
    ("", False),
    ("Sugerencias de enlazado interno: Liposucción asistida por láser → /cirugia-estetica/liposuccion/liposuccion-laser/ | Mastopexia → /cirugia-estetica/mastopexia-elevacion-de-pecho/ | Mamoplastia de aumento → /cirugia-estetica/aumento-pecho-natural/ | Abdominoplastia → /cirugia-estetica/abdominoplastia/ | Equipo médico → /equipo-medico/", False),
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def utf16_len(text):
    return sum(2 if ord(c) > 0xFFFF else 1 for c in text)

def loc(idx):
    return {"index": idx, "tabId": TAB_ID}

def rng(start, end):
    return {"startIndex": start, "endIndex": end, "tabId": TAB_ID}

def preprocess_blocks(blocks):
    result = []
    skip_next_blank = False
    for text, is_bold in blocks:
        if skip_next_blank and text == "":
            skip_next_blank = False
            continue
        skip_next_blank = is_bold and text != ""
        result.append((text, is_bold))
    return result

def build_text_requests(blocks, start_index):
    inserts = []
    bold_ranges = []
    bullet_ranges = []
    blue_ranges = []
    idx = start_index
    for text, is_bold in preprocess_blocks(blocks):
        is_bullet = text.startswith("— ")
        is_blue = text.startswith("[añadir imagen") or text.startswith("[AÑADIR IMAGEN")
        if is_bullet:
            text = text[2:]
        full = text + "\n"
        n = utf16_len(full)
        inserts.append({"insertText": {"location": loc(idx), "text": full}})
        if is_bold and text:
            bold_ranges.append((idx, idx + n))
        if is_bullet and text:
            bullet_ranges.append((idx, idx + n))
        if is_blue and text:
            blue_ranges.append((idx, idx + n))
        idx += n
    return inserts, bold_ranges, bullet_ranges, blue_ranges, idx

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
creds = get_google_credentials()
service = build("docs", "v1", credentials=creds)

print("Leyendo documento...")
doc = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
end_index = 1
for tab in doc.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            end_index = max(1, body_content[-1].get("endIndex", 2) - 1)
        break

if end_index > 1:
    print(f"Limpiando contenido existente (índice 1 a {end_index})...")
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [{"deleteContentRange": {"range": rng(1, end_index)}}]},
    ).execute()
    print("Contenido anterior eliminado.")

print("Insertando contenido principal...")
ins_before, bold_before, bullet_before, blue_before, idx_after_before = build_text_requests(BLOCKS_BEFORE_TABLE, 1)
bullet_reqs_before = [
    {"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
    for s, e in bullet_before
]
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": ins_before + bullet_reqs_before},
).execute()
print(f"  Bloque 1 insertado. Indice actual: {idx_after_before}")

table_position = idx_after_before
num_rows = len(TABLE_ROWS) + 1
num_cols = len(TABLE_HEADERS)
print(f"Insertando tabla ({num_rows} filas x {num_cols} columnas)...")
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"insertTable": {
        "rows": num_rows, "columns": num_cols, "location": loc(table_position),
    }}]},
).execute()

print("Leyendo posiciones de celdas...")
doc2 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
target_table = None
for tab in doc2.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        for element in tab.get("documentTab", {}).get("body", {}).get("content", []):
            if "table" in element and abs(element.get("startIndex", 0) - table_position) <= 5:
                target_table = element["table"]
                break
        break

if target_table is None:
    print("ERROR: no se encontro la tabla.")
    sys.exit(1)

all_rows_data = [TABLE_HEADERS] + TABLE_ROWS
cell_fills = []
for r_idx, (row_el, row_data) in enumerate(zip(target_table.get("tableRows", []), all_rows_data)):
    for cell_el, cell_text in zip(row_el.get("tableCells", []), row_data):
        cell_content = cell_el.get("content", [])
        if cell_content:
            insert_idx = cell_content[0].get("startIndex", 0)
            cell_fills.append((insert_idx, cell_text, r_idx == 0))

# Rellenar de mayor a menor indice para que los indices leidos sigan siendo validos
cell_fills.sort(key=lambda x: x[0], reverse=True)
cell_requests = []
for insert_idx, cell_text, is_header in cell_fills:
    cell_requests.append({"insertText": {"location": loc(insert_idx), "text": cell_text}})
    if is_header:
        cell_requests.append({"updateTextStyle": {
            "range": rng(insert_idx, insert_idx + utf16_len(cell_text)),
            "textStyle": {"bold": True}, "fields": "bold",
        }})

service.documents().batchUpdate(documentId=DOC_ID, body={"requests": cell_requests}).execute()
print("  Tabla rellenada.")

doc3 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
new_end = 1
for tab in doc3.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            new_end = max(1, body_content[-1].get("endIndex", 2) - 1)
        break

print("Insertando contenido despues de la tabla...")
ins_after, bold_after, bullet_after, blue_after, final_idx = build_text_requests(BLOCKS_AFTER_TABLE, new_end)
bullet_reqs_after = [
    {"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
    for s, e in bullet_after
]
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": ins_after + bullet_reqs_after},
).execute()
print(f"  Bloque 2 insertado. Indice final: {final_idx}")

print("Aplicando Arial 11...")
doc4 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
total_end = 1
for tab in doc4.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            total_end = max(1, body_content[-1].get("endIndex", 2) - 1)
        break
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"updateTextStyle": {
        "range": rng(1, total_end),
        "textStyle": {
            "weightedFontFamily": {"fontFamily": "Arial"},
            "fontSize": {"magnitude": 11, "unit": "PT"},
        },
        "fields": "weightedFontFamily,fontSize",
    }}]},
).execute()
print(f"  Arial 11 aplicado (1 a {total_end}).")

print("Aplicando negrita a headings...")
all_bold = bold_before + bold_after
bold_reqs = [
    {"updateTextStyle": {"range": rng(s, e), "textStyle": {"bold": True}, "fields": "bold"}}
    for s, e in all_bold
]
if bold_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": bold_reqs}).execute()
print(f"  {len(bold_reqs)} headings en negrita.")

print("Aplicando azul a lineas de imagen...")
all_blue = blue_before + blue_after
blue_reqs = [
    {"updateTextStyle": {
        "range": rng(s, e),
        "textStyle": {"foregroundColor": {"color": {"rgbColor": {
            "red": 0.063, "green": 0.392, "blue": 0.784
        }}}},
        "fields": "foregroundColor",
    }}
    for s, e in all_blue
]
if blue_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": blue_reqs}).execute()
print(f"  {len(blue_reqs)} lineas de imagen en azul.")

print("\nDocumento completado con exito.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
