# -*- coding: utf-8 -*-
"""
Script para escribir el texto SEO "Clínica de Cirugía Plástica en Córdoba" (página pilar) de Diagonal CQ en Google Docs.
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
TAB_ID = "t.p5i0lub40lb7"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita)
# ---------------------------------------------------------------------------
URL_RECONSTRUCCION = "https://diagonalcq.es/cirugia-plastica/reconstruccion-mamaria/"
URL_LIPOLIFTING = "https://diagonalcq.es/cirugia-plastica/reconstruccion-mamaria/lipolifting/"
URL_HERIDAS = "https://diagonalcq.es/cirugia-plastica/heridas-quemaduras/"
URL_CANCER_PIEL = "https://diagonalcq.es/cirugia-plastica/cancer-piel/"
URL_POST_PESO = "https://diagonalcq.es/cirugia-plastica/cirugia-post-perdida-peso/"
URL_ABDOMINOPLASTIA = "https://diagonalcq.es/cirugia-estetica/abdominoplastia/"
URL_EQUIPO = "https://diagonalcq.es/sobre-nosotros/equipo-medico/"
URL_CONTACTO = "https://diagonalcq.es/contacto/"

BLOCKS_BEFORE_TABLE = [
    ("Meta title: Clínica de Cirugía Plástica en Córdoba | Diagonal CQ", False),
    ("Meta description: Clínica de cirugía plástica y reparadora en Córdoba con el Dr. Joan Benítez: reconstrucción mamaria, cáncer de piel, quemaduras y más. Pide tu valoración.", False),
    ("URL slug: /cirugia-plastica/ (categoría real ya existente en el sitio)", False),
    ("", False),
    ("H1: Clínica de Cirugía Plástica en Córdoba", True),
    ("En Diagonal CQ somos una clínica de cirugía plástica en Córdoba especializada en cirugía reparadora: intervenciones que responden a una necesidad médica real, no a una elección estética. El Dr. Joan Benítez trabaja de forma coordinada con otros especialistas cuando el caso lo requiere, para devolver forma y función tras una enfermedad, un accidente o una pérdida de peso importante.", False),
    ("", False),
    ("H2: ¿Qué es la cirugía plástica y reparadora?", True),
    ("La cirugía plástica y reparadora es la rama de la medicina quirúrgica que corrige alteraciones causadas por enfermedades, accidentes, malformaciones congénitas o intervenciones previas, con el objetivo de restaurar la forma y la función del cuerpo. Se diferencia de la cirugía estética en que no responde a una decisión personal de mejora sobre un cuerpo sano, sino a una necesidad médica.", False),
    ("", False),
    ("Según la Sociedad Española de Cirugía Plástica, Reparadora y Estética (SECPRE), ambas disciplinas comparten formación y técnicas, pero la cirugía reparadora exige además una coordinación estrecha con otras especialidades médicas —oncología, cirugía general, dermatología— según el origen de cada caso.", False),
    ("", False),
    ("En Diagonal CQ, cada intervención de cirugía reparadora parte de una valoración médica rigurosa y, cuando es necesario, de la coordinación con el equipo que ya está tratando al paciente.", False),
    ("", False),
    ("H2: Tratamientos de cirugía plástica y reparadora en Diagonal CQ", True),
    ("Agrupamos nuestros tratamientos de cirugía reparadora en cuatro áreas.", False),
    ("", False),
    ("H3: Reconstrucción mamaria", True),
    ("— Reconstrucción mamaria post mastectomía: restaura la forma, el volumen y la simetría del pecho tras una mastectomía por cáncer de mama. Consulta el detalle completo en nuestra página de reconstrucción mamaria.", False, [("página de reconstrucción mamaria", URL_RECONSTRUCCION)]),
    ("— Injerto graso (lipofilling reconstructivo): utiliza grasa propia de la paciente para corregir irregularidades o mejorar el resultado de una reconstrucción previa.", False, [("Injerto graso (lipofilling reconstructivo)", URL_LIPOLIFTING)]),
    ("— Corrección de deformidades congénitas: aborda malformaciones mamarias presentes desde el nacimiento.", False),
    ("", False),
    ("H3: Heridas y quemaduras", True),
    ("Tratamiento quirúrgico de heridas complejas y secuelas de quemaduras, con el objetivo de restaurar la cobertura cutánea y minimizar las cicatrices resultantes. Ampliamos esta información en nuestra página de heridas y quemaduras.", False, [("página de heridas y quemaduras", URL_HERIDAS)]),
    ("", False),
    ("H3: Cáncer de piel", True),
    ("— Extirpación de cáncer de piel y reconstrucción: extirpación quirúrgica de la lesión con márgenes de seguridad y reconstrucción inmediata de la zona afectada, coordinada con el especialista en dermatología u oncología que haya realizado el diagnóstico. Más información en nuestra página de cáncer de piel.", False, [("página de cáncer de piel", URL_CANCER_PIEL)]),
    ("", False),
    ("H3: Cirugía post pérdida de peso", True),
    ("Tras pérdidas de peso importantes quedan secuelas de exceso de piel y flacidez que no se resuelven solo con dieta o ejercicio. Puedes consultar el detalle completo en nuestra página de cirugía post pérdida de peso. En Diagonal CQ abordamos estas secuelas con:", False, [("página de cirugía post pérdida de peso", URL_POST_PESO)]),
    ("— Abdominoplastia: elimina el exceso de piel y grasa del abdomen. La tratamos en detalle en nuestra página de abdominoplastia.", False, [("página de abdominoplastia", URL_ABDOMINOPLASTIA)]),
    ("— Lifting corporal (brazos, muslos, pecho, glúteos): elimina la piel sobrante en estas zonas tras una pérdida de peso masiva, mejorando el contorno corporal general.", False),
    ("", False),
]

# Tabla comparativa de categorías
TABLE_HEADERS = ["Categoría", "Tratamientos incluidos", "Origen habitual del caso"]
TABLE_ROWS = [
    ["Reconstrucción mamaria", "Post mastectomía, injerto graso, deformidades congénitas", "Cáncer de mama, malformación congénita"],
    ["Heridas y quemaduras", "Tratamiento de heridas complejas y secuelas de quemaduras", "Accidente, quemadura, herida compleja"],
    ["Cáncer de piel", "Extirpación y reconstrucción", "Diagnóstico dermatológico u oncológico"],
    ["Cirugía post pérdida de peso", "Abdominoplastia, lifting corporal (brazos, muslos, pecho, glúteos)", "Pérdida de peso masiva (dieta o cirugía bariátrica)"],
]

BLOCKS_AFTER_TABLE = [
    ("", False),
    ("H2: ¿Cómo abordamos la cirugía reparadora en Diagonal CQ?", True),
    ("Nuestro proceso se adapta al origen de cada caso, pero sigue siempre estas fases:", False),
    ("", False),
    ("1. Valoración médica inicial: el Dr. Joan Benítez analiza el origen del caso, los informes médicos previos si los hay, y el objetivo funcional y estético de la reconstrucción.", False),
    ("2. Coordinación con otros especialistas: cuando el caso lo requiere (oncología, dermatología, cirugía general), se coordina el momento y la técnica más adecuada con el equipo que ya trata al paciente.", False),
    ("3. Plan quirúrgico personalizado: se diseña la técnica según el origen de la lesión, el estado de los tejidos y los objetivos realistas del paciente.", False),
    ("4. Intervención: se realiza en las condiciones de seguridad y anestesia adecuadas a cada procedimiento.", False),
    ("5. Seguimiento postoperatorio: revisiones programadas, coordinadas también con el equipo médico de origen cuando corresponde.", False),
    ("", False),
    ("[CTA intermedio] ¿Necesitas una valoración de cirugía reparadora? Solicita tu consulta con el Dr. Joan Benítez en Diagonal CQ, en Córdoba. [BOTÓN: Pedir cita]", False),
    ("", False),
    ("H2: ¿Es la cirugía plástica y reparadora adecuada para mí?", True),
    ("A diferencia de la cirugía estética, la indicación de estos tratamientos parte casi siempre de una necesidad médica ya diagnosticada: una mastectomía, una quemadura, una lesión cutánea o una pérdida de peso masiva con secuelas de piel. Antes de la intervención se valoran:", False),
    ("— Tu estado de salud general y si tienes patologías no controladas que puedan aumentar el riesgo quirúrgico.", False),
    ("— Si eres fumador, ya que el tabaco puede afectar a la cicatrización y a los resultados.", False),
    ("— El momento adecuado, que en casos oncológicos depende de la coordinación con el tratamiento principal (por ejemplo, la radioterapia condiciona el momento de una reconstrucción mamaria).", False),
    ("— Que tus expectativas sean realistas: el objetivo de la cirugía reparadora es restaurar forma y función, no garantizar un resultado idéntico al previo a la lesión.", False),
    ("", False),
    ("H2: Preguntas frecuentes sobre cirugía plástica y reparadora en Córdoba", True),
    ("", False),
    ("H3: ¿Qué diferencia hay entre cirugía plástica reparadora y cirugía estética?", True),
    ("La cirugía reparadora corrige alteraciones causadas por enfermedades, accidentes o malformaciones congénitas, con el objetivo de restaurar forma y función. La cirugía estética modifica una parte del cuerpo sano por decisión personal. El Dr. Joan Benítez está formado en ambas ramas, que comparten técnicas quirúrgicas.", False),
    ("", False),
    ("H3: ¿La reconstrucción mamaria está cubierta por la Seguridad Social?", True),
    ("Sí. La ley española reconoce el derecho de toda paciente mastectomizada a la reconstrucción mamaria en el sistema sanitario público. En el ámbito privado, la mayoría de los seguros médicos con cobertura quirúrgica también la incluyen. Puedes consultar los detalles en nuestra página de reconstrucción mamaria.", False, [("página de reconstrucción mamaria", URL_RECONSTRUCCION)]),
    ("", False),
    ("H3: ¿Cuándo se puede operar una secuela de pérdida de peso masiva?", True),
    ("Se recomienda esperar a que el peso esté estable durante al menos 6 meses, mantener un buen estado de salud general y no fumar. La indicación definitiva se valora siempre en consulta con el Dr. Joan Benítez.", False),
    ("", False),
    ("H3: ¿La extirpación de cáncer de piel deja cicatriz?", True),
    ("Toda cirugía de extirpación deja una cicatriz, cuyo tamaño depende de la lesión y los márgenes de seguridad necesarios. En Diagonal CQ planificamos la reconstrucción inmediata para minimizar el impacto estético y funcional de la cicatriz resultante.", False),
    ("", False),
    ("H3: ¿La cirugía reparadora en Córdoba tiene financiación o facilidades de pago?", True),
    ("En Diagonal CQ podemos informarte sobre las opciones de financiación disponibles en la consulta de valoración, adaptadas a cada tratamiento y caso.", False),
    ("", False),
    ("H3: ¿Necesito un informe médico previo para pedir cita?", True),
    ("No es imprescindible para la primera consulta, pero si tu caso está relacionado con un tratamiento oncológico o una intervención previa, es recomendable traer los informes disponibles para que el Dr. Joan Benítez pueda valorar tu caso con toda la información.", False),
    ("", False),
    ("H2: Por qué elegir Diagonal CQ para tu cirugía plástica y reparadora en Córdoba", True),
    ("En Diagonal CQ abordamos la cirugía reparadora con la misma exigencia médica que cualquier otra especialidad quirúrgica: valoración individual, coordinación con otros especialistas cuando el caso lo requiere, y un seguimiento cercano antes y después de la intervención. Somos una clínica de referencia en Córdoba para pacientes que necesitan restaurar forma y función tras una enfermedad, un accidente o una pérdida de peso importante.", False),
    ("", False),
    ("Solicita tu valoración inicial y resuelve tus dudas sobre el tratamiento de cirugía reparadora que necesitas.", False),
    ("", False),
    ("[CTA final] Solicita tu valoración en Córdoba [BOTÓN: Pedir cita]", False, [("Solicita tu valoración en Córdoba", URL_CONTACTO)]),
    ("", False),
    ("Doctor responsable: Dr. Joan Ramon Benítez Gomà", False, [("Dr. Joan Ramon Benítez Gomà", URL_EQUIPO)]),
    ("Especialidad médica: Cirugía Plástica, Reparadora y Estética", False),
    ("Número de colegiado: 146121", False),
    ("Registro sanitario del centro: NICA 54005", False),
    ("", False),
    ("Revisado y supervisado por el Dr. Joan Ramon Benítez Gomà, especialista en Cirugía Plástica, Reparadora y Estética, nº colegiado 146121. Última revisión: julio de 2026.", False, [("Dr. Joan Ramon Benítez Gomà", URL_EQUIPO)]),
    ("", False),
    ("El contenido de esta página tiene carácter informativo y no sustituye la consulta médica personalizada. Ante cualquier duda sobre tu caso, consulta con un especialista cualificado.", False),
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
    for item in blocks:
        text, is_bold = item[0], item[1]
        links = item[2] if len(item) > 2 else []
        if skip_next_blank and text == "":
            skip_next_blank = False
            continue
        skip_next_blank = is_bold and text != ""
        result.append((text, is_bold, links))
    return result

def build_text_requests(blocks, start_index):
    inserts = []
    bold_ranges = []
    bullet_ranges = []
    blue_ranges = []
    link_ranges = []
    idx = start_index
    for text, is_bold, links in preprocess_blocks(blocks):
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
        for anchor, url in links:
            pos = text.find(anchor)
            if pos != -1:
                start_off = utf16_len(text[:pos])
                end_off = utf16_len(text[:pos + len(anchor)])
                link_ranges.append((idx + start_off, idx + end_off, url))
        idx += n
    return inserts, bold_ranges, bullet_ranges, blue_ranges, link_ranges, idx

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
ins_before, bold_before, bullet_before, blue_before, link_before, idx_after_before = build_text_requests(BLOCKS_BEFORE_TABLE, 1)
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
ins_after, bold_after, bullet_after, blue_after, link_after, final_idx = build_text_requests(BLOCKS_AFTER_TABLE, new_end)
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

print("Aplicando hipervinculos...")
all_links = link_before + link_after
link_reqs = [
    {"updateTextStyle": {
        "range": rng(s, e),
        "textStyle": {"link": {"url": url}},
        "fields": "link",
    }}
    for s, e, url in all_links
]
if link_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": link_reqs}).execute()
print(f"  {len(link_reqs)} hipervinculos aplicados.")

print("\nDocumento completado con exito.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
