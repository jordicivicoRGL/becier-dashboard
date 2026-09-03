# -*- coding: utf-8 -*-
"""
Script para escribir el texto SEO "Cirugía Estética en Córdoba" (página pilar) de Diagonal CQ en Google Docs.
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
TAB_ID = "t.9etpecxr67er"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita)
# ---------------------------------------------------------------------------
BLOCKS_BEFORE_TABLE = [
    ("Meta title: Cirugía Estética en Córdoba | Diagonal CQ", False),
    ("Meta description: Cirugía estética en Córdoba con el Dr. Joan Benítez: rostro, pecho y contorno corporal. Valoración personalizada y seguimiento cercano. Pide tu cita.", False),
    ("URL slug: /cirugia-estetica-cordoba/", False),
    ("", False),
    ("H1: Cirugía Estética en Córdoba", True),
    ("En Diagonal CQ ofrecemos cirugía estética en Córdoba con un enfoque personalizado: un único equipo que te acompaña desde la primera valoración hasta el seguimiento posterior. Si estás pensando en un cambio en tu rostro, tu pecho o tu silueta, en esta página encontrarás qué tratamientos realizamos, cómo trabajamos y qué debes saber antes de dar el paso.", False),
    ("", False),
    ("H2: ¿Qué es la cirugía estética y en qué se diferencia de la cirugía plástica?", True),
    ("La cirugía estética es la rama de la medicina quirúrgica que tiene como objetivo mejorar la apariencia física de una persona sana, por decisión personal y no por una necesidad médica. Se diferencia de la cirugía plástica reparadora, que corrige alteraciones causadas por accidentes, enfermedades o malformaciones congénitas.", False),
    ("", False),
    ("En la práctica, ambas disciplinas están estrechamente relacionadas: un mismo especialista puede realizar tanto intervenciones estéticas como reconstructivas, ya que comparten técnicas y formación. Según la Sociedad Española de Cirugía Plástica, Reparadora y Estética (SECPRE), la cirugía estética debe realizarse siempre bajo criterios de seguridad clínica y con una valoración previa exhaustiva del paciente, independientemente de que la motivación sea estética.", False),
    ("", False),
    ("En Diagonal CQ, cada intervención parte de esta misma premisa: la decisión es personal, pero el abordaje es siempre médico y riguroso.", False),
    ("", False),
    ("H2: Tratamientos de cirugía estética en Diagonal CQ", True),
    ("Agrupamos nuestros tratamientos de cirugía estética en tres áreas según la zona del cuerpo a tratar.", False),
    ("", False),
    ("H3: Cirugía estética facial", True),
    ("— Blefaroplastia: corrige el exceso de piel y grasa en los párpados superiores e inferiores, suavizando la mirada cansada.", False),
    ("— Otoplastia: corrige la posición o el tamaño de las orejas, habitualmente orejas prominentes o \"en soplillo\".", False),
    ("", False),
    ("H3: Cirugía de pecho", True),
    ("— Aumento de pecho: incrementa el volumen mamario mediante implantes, adaptados a la anatomía de cada paciente.", False),
    ("— Reducción de pecho: reduce el volumen y peso mamario, mejorando molestias posturales asociadas a mamas muy voluminosas.", False),
    ("— Elevación de pecho (mastopexia): corrige la caída o pérdida de firmeza mamaria sin necesidad de modificar el volumen.", False),
    ("— Cirugía secundaria de mama: revisa o corrige intervenciones mamarias previas realizadas en otro centro o en Diagonal CQ.", False),
    ("", False),
    ("H3: Contorno corporal", True),
    ("— Liposucción: técnica de eliminación de grasa localizada mediante cánulas de aspiración, base de las variantes específicas por zona que ofrecemos en Diagonal CQ.", False),
    ("— Liposucción de abdomen y flancos: elimina el exceso de grasa localizada en la zona media del cuerpo.", False),
    ("— Liposucción de piernas y glúteos: remodela el contorno de la parte inferior del cuerpo.", False),
    ("— Liposucción en brazos: reduce la grasa localizada en la zona del tríceps.", False),
    ("— Liposucción asistida por láser: técnica que combina la aspiración de grasa con energía láser para favorecer la retracción de la piel.", False),
    ("— Abdominoplastia: retira el exceso de piel y grasa del abdomen y refuerza la musculatura abdominal, indicada especialmente tras embarazos o pérdidas de peso importantes.", False),
    ("", False),
]

# Tabla comparativa de categorías
TABLE_HEADERS = ["Categoría", "Tratamientos incluidos", "Objetivo principal", "Recuperación orientativa*"]
TABLE_ROWS = [
    ["Cirugía facial", "Blefaroplastia, Otoplastia", "Rejuvenecer o corregir rasgos faciales", "1-2 semanas"],
    ["Cirugía de pecho", "Aumento, reducción, mastopexia, cirugía secundaria", "Modificar volumen o firmeza mamaria", "2-4 semanas"],
    ["Contorno corporal", "Liposucción, liposucción de abdomen/piernas/brazos, liposucción láser, abdominoplastia", "Remodelar la silueta corporal", "2-6 semanas según técnica"],
]

BLOCKS_AFTER_TABLE = [
    ("", False),
    ("*La duración indicada es orientativa y puede variar según cada caso clínico.", False),
    ("", False),
    ("H2: ¿Cómo abordamos la cirugía estética en Diagonal CQ?", True),
    ("Nuestro proceso se estructura en cinco fases, comunes a todos los tratamientos de cirugía estética que realizamos:", False),
    ("", False),
    ("1. Primera consulta y valoración: analizamos tu caso, tus expectativas y tu historial de salud con el Dr. Joan Benítez.", False),
    ("2. Plan quirúrgico personalizado: diseñamos la técnica más adecuada según tu anatomía y objetivo.", False),
    ("3. Preparación preoperatoria: pruebas médicas necesarias y recomendaciones previas a la intervención.", False),
    ("4. Intervención: se realiza en las condiciones de seguridad y anestesia adecuadas a cada procedimiento.", False),
    ("5. Seguimiento postoperatorio: revisiones programadas para acompañar tu recuperación.", False),
    ("", False),
    ("Si quieres saber qué tratamiento se adapta mejor a tu caso, solicita tu valoración con el Dr. Joan Benítez y te explicaremos las opciones más adecuadas para ti.", False),
    ("", False),
    ("H2: ¿Es la cirugía estética adecuada para mí?", True),
    ("No toda persona es candidata a cualquier tratamiento de cirugía estética. Antes de decidir, es importante tener en cuenta:", False),
    ("", False),
    ("— Tu estado de salud general y si tienes patologías no controladas que puedan aumentar el riesgo quirúrgico.", False),
    ("— Si eres fumador, ya que el tabaco puede afectar a la cicatrización y a los resultados.", False),
    ("— Que tus expectativas sean realistas: la cirugía estética mejora la apariencia, pero no sustituye hábitos de vida saludables ni resuelve problemas de autoestima no relacionados con el aspecto físico.", False),
    ("", False),
    ("Estos factores se valoran siempre en la consulta previa, donde el Dr. Joan Benítez determinará si eres candidato y qué técnica se ajusta mejor a tu situación.", False),
    ("", False),
    ("H2: Preguntas frecuentes sobre cirugía estética en Córdoba", True),
    ("", False),
    ("H3: ¿Qué diferencia hay entre cirugía estética y cirugía plástica?", True),
    ("La cirugía estética modifica una parte del cuerpo sano por decisión personal, mientras que la cirugía plástica reparadora corrige alteraciones derivadas de accidentes, enfermedades o malformaciones. Muchos cirujanos, como el Dr. Joan Benítez, están formados en ambas ramas.", False),
    ("", False),
    ("H3: ¿Cuánto tiempo de recuperación necesita una cirugía estética?", True),
    ("Depende del tratamiento: intervenciones faciales como la blefaroplastia suelen requerir 1-2 semanas, mientras que procedimientos de contorno corporal como la abdominoplastia pueden necesitar entre 4 y 6 semanas. El plazo exacto se valora de forma individual.", False),
    ("", False),
    ("H3: ¿La cirugía estética en Córdoba tiene financiación o facilidades de pago?", True),
    ("En Diagonal CQ podemos informarte sobre las opciones de financiación disponibles en la consulta de valoración, adaptadas a cada tratamiento y caso.", False),
    ("", False),
    ("H3: ¿Qué riesgos generales tiene una cirugía estética?", True),
    ("Como toda intervención quirúrgica, conlleva riesgos generales (infección, cicatrización anómala, reacción a la anestesia) que se explican de forma detallada antes de la intervención. El equipo médico valora cada caso para minimizarlos.", False),
    ("", False),
    ("H3: ¿Cómo elijo el tratamiento de cirugía estética adecuado para mí?", True),
    ("No existe una respuesta única: depende de la zona a tratar, tu anatomía y tus objetivos. La consulta de valoración con el Dr. Joan Benítez es el paso necesario para determinar qué opción se ajusta mejor a tu caso.", False),
    ("", False),
    ("H3: ¿Es dolorosa la recuperación tras una cirugía estética?", True),
    ("El nivel de molestia varía según el tratamiento y se controla con la medicación pautada tras la intervención. En la consulta se informa de qué esperar en cada caso concreto.", False),
    ("", False),
    ("H2: Por qué elegir Diagonal CQ para tu cirugía estética en Córdoba", True),
    ("En Diagonal CQ no ofrecemos un catálogo cerrado de intervenciones: cada plan quirúrgico se diseña con el Dr. Joan Benítez a partir de tu caso concreto, con seguimiento cercano antes y después de la intervención. Somos una clínica de referencia en Córdoba para quienes buscan un abordaje médico riguroso, sin promesas vacías y con información clara en cada fase del proceso.", False),
    ("", False),
    ("Solicita tu valoración inicial y da el primer paso hacia el tratamiento de cirugía estética que mejor se adapte a ti.", False),
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
    ("Sugerencias de enlazado interno: Blefaroplastia → /cirugia-estetica-facial/blefaroplastia/ | Aumento de pecho → /cirugia-de-pecho/aumento-de-pecho/ | Liposucción → /cirugia-estetica/liposuccion/ | Liposucción de abdomen y flancos → /contorno-corporal/liposuccion-abdomen-flancos/ | Equipo médico → /equipo-medico/ | Contacto / valoración → /contacto/", False),
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
    """Elimina líneas en blanco justo después de headings (is_bold=True)."""
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
    """Returns (insert_requests, bold_ranges, bullet_ranges, blue_ranges, final_index)."""
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

# Procesar de mayor a menor indice: cada insertText desplaza los indices
# posteriores dentro del mismo batchUpdate, asi que rellenamos empezando
# por la ultima celda para que los indices ya leidos sigan siendo validos.
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
