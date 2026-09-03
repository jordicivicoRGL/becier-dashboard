# -*- coding: utf-8 -*-
"""
Script para escribir el texto SEO "Reconstrucción Mamaria Post Mastectomía en Córdoba" de Diagonal CQ en Google Docs.
Formato: Arial 11, NORMAL_TEXT, prefijos H1:/H2:/H3: en negrita, tabla real, enlaces internos reales incrustados.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1QN41nJcgLGP_Hr4_Mhwi2g1ShkjPZwc7xO50-OPI4CY"
TAB_ID = "t.8mh44pxc14kg"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita, [links])
# ---------------------------------------------------------------------------
URL_LIPOLIFTING = "https://diagonalcq.es/cirugia-plastica/reconstruccion-mamaria/lipolifting/"
URL_CIRUGIA_PLASTICA = "https://diagonalcq.es/cirugia-plastica/"
URL_EQUIPO = "https://diagonalcq.es/sobre-nosotros/equipo-medico/"
URL_CONTACTO = "https://diagonalcq.es/contacto/"

BLOCKS_BEFORE_TABLE = [
    ("Meta title: Reconstrucción Mamaria Post Mastectomía en Córdoba | Diagonal CQ", False),
    ("Meta description: Reconstrucción mamaria post mastectomía en Córdoba con el Dr. Joan Benítez: implantes, colgajos o tejido propio. Valoración personalizada en Diagonal CQ.", False),
    ("URL slug: /cirugia-plastica/reconstruccion-mamaria/ (se mantiene la URL existente)", False),
    ("", False),
    ("H1: Reconstrucción Mamaria Post Mastectomía en Córdoba", True),
    ("La reconstrucción de la mama tras una extirpación total o parcial por cáncer forma parte del tratamiento de la enfermedad, no es una cirugía aparte ni una decisión estética. En Diagonal CQ, en Córdoba, el Dr. Joan Benítez coordina el proceso de reconstrucción con el equipo de oncología, radiología, anatomía patológica y radioterapia que atiende a cada paciente, adaptando la estrategia a su situación clínica y a sus preferencias.", False),
    ("", False),
    ("H2: ¿Qué es la reconstrucción mamaria post mastectomía?", True),
    ("La reconstrucción mamaria es un procedimiento médico y quirúrgico recomendado por el equipo que atiende a una mujer con diagnóstico de cáncer de mama. Su objetivo principal es hacer compatible el tratamiento adecuado del tumor con la conservación de la integridad corporal de la paciente.", False),
    ("", False),
    ("Según la Sociedad Española de Cirugía Plástica, Reparadora y Estética (SECPRE), la reconstrucción mamaria debe planificarse siempre de forma individualizada, en coordinación con el equipo oncológico, y con una información realista sobre lo que el procedimiento puede y no puede conseguir.", False),
    ("", False),
    ("Las secuelas del tratamiento del cáncer de mama pueden incluir la ausencia total de la mama, distorsión de su forma natural, desplazamiento o pérdida de la areola y el pezón, cambios en el volumen, asimetría con la mama contralateral, y alteraciones de la piel y los tejidos causadas por la radioterapia. Los procedimientos de reconstrucción pueden contribuir a evitar o reducir la severidad de estas secuelas.", False),
    ("", False),
    ("H2: Reconstrucción inmediata o diferida: ¿cuándo se realiza?", True),
    ("El momento idóneo para iniciar la reconstrucción se decide siempre según el contexto clínico de cada paciente.", False),
    ("", False),
    ("H3: Reconstrucción inmediata", True),
    ("El procedimiento de reconstrucción se inicia en el mismo tiempo quirúrgico que la cirugía de extirpación del tumor.", False),
    ("", False),
    ("H3: Reconstrucción diferida", True),
    ("El procedimiento de reconstrucción se inicia una vez finalizado el tratamiento oncológico del tumor, cuando este condiciona el momento o la técnica más segura.", False),
    ("", False),
    ("H2: Técnicas de reconstrucción mamaria", True),
    ("La estrategia de reconstrucción elegida depende de los criterios del equipo quirúrgico responsable, de la historia oncológica, las características físicas y las preferencias de cada paciente. Según su caso, se pueden ofrecer:", False),
    ("", False),
    ("— Reconstrucción con implantes mamarios.", False),
    ("— Reconstrucción con colgajos (torácicos o abdominales) de tejido propio de la paciente.", False),
    ("— Reconstrucción mediante microcirugía.", False),
    ("— Injerto graso (lipofilling), como técnica complementaria o principal.", False, [("Injerto graso (lipofilling)", URL_LIPOLIFTING)]),
    ("— Estrategias mixtas, combinando implantes y colgajos.", False),
    ("", False),
    ("La reconstrucción mamaria es un procedimiento complejo. Es fundamental que la paciente sea informada con detalle y participe en la decisión sobre cuál es la estrategia más adecuada para ella.", False),
    ("", False),
]

# Tabla comparativa de técnicas
TABLE_HEADERS = ["Técnica", "Origen del tejido", "Cuándo se prioriza"]
TABLE_ROWS = [
    ["Implantes mamarios", "Prótesis", "Buena cobertura cutánea, sin radioterapia extensa prevista"],
    ["Colgajos torácicos o abdominales", "Tejido propio", "Radioterapia previa o preferencia por tejido propio"],
    ["Microcirugía", "Tejido propio", "Casos que requieren mayor precisión vascular"],
    ["Injerto graso (lipofilling)", "Tejido propio", "Retoques de contorno o regeneración de piel radiada"],
    ["Estrategia mixta", "Prótesis + tejido propio", "Volumen insuficiente con tejido propio solo"],
]

BLOCKS_AFTER_TABLE = [
    ("", False),
    ("*La técnica más adecuada se determina siempre en la valoración individual con el Dr. Joan Benítez.", False),
    ("", False),
    ("H2: Reconstrucción de la areola y el pezón", True),
    ("La reconstrucción del complejo areola-pezón es, para muchas pacientes, el final de un largo proceso que a menudo ha convivido con el tratamiento de quimioterapia y radioterapia. Completar esta fase se vive frecuentemente como el cierre de una etapa.", False),
    ("", False),
    ("El procedimiento es sencillo: se realiza con anestesia local, o anestesia local y sedación asistida por un anestesista, y es ambulatorio. Con frecuencia se combina en la misma intervención con un pequeño injerto de grasa (lipofilling), con el objetivo de mejorar el contorno de la mama reconstruida y regenerar la piel afectada por la radiación.", False, [("injerto de grasa (lipofilling)", URL_LIPOLIFTING)]),
    ("", False),
    ("[CTA intermedio] ¿Te han diagnosticado cáncer de mama y quieres informarte sobre tus opciones de reconstrucción? Solicita tu valoración con el Dr. Joan Benítez en Diagonal CQ, en Córdoba. [BOTÓN: Pedir cita]", False, [("Solicita tu valoración", URL_CONTACTO)]),
    ("", False),
    ("H2: ¿Qué puede conseguir y qué no puede conseguir la reconstrucción mamaria?", True),
    ("El objetivo principal es recuperar la integridad e imagen corporal, contribuyendo a la calidad de vida de la paciente. Es importante entender que el procedimiento puede reconstruir la mama, pero no reponer el seno natural.", False),
    ("", False),
    ("La mama reconstruida presentará diferencias variables de tamaño, contorno y simetría respecto a la mama no intervenida, mantendrá las cicatrices originales y en ocasiones requerirá cicatrices adicionales —incluso en la mama sana, para mejorar la simetría—. Su consistencia y textura cutánea también pueden ser distintas. Los cambios por el envejecimiento y las variaciones de peso influirán igualmente en el resultado a largo plazo.", False),
    ("", False),
    ("H2: ¿Existen las complicaciones?", True),
    ("Como en todo procedimiento médico y quirúrgico, existe un abanico de complicaciones posibles de frecuencia variable, que el cirujano explica de forma detallada y que quedan recogidas en el documento de consentimiento informado. La aparición de una complicación no implica necesariamente una mala ejecución del procedimiento: la paciente debe distinguir entre las limitaciones propias de su caso y una complicación quirúrgica real.", False),
    ("", False),
    ("H2: ¿Cómo es el proceso en Diagonal CQ?", True),
    ("1. Valoración inicial: el Dr. Joan Benítez revisa la historia oncológica, las características físicas y las preferencias de la paciente.", False),
    ("2. Coordinación con el equipo oncológico: se confirma el momento idóneo —inmediato o diferido— según el protocolo de tratamiento del cáncer.", False),
    ("3. Planificación de la estrategia de reconstrucción: se explican las opciones técnicas disponibles y se decide conjuntamente con la paciente.", False),
    ("4. Intervención: se realiza según la técnica elegida, en coordinación con el resto de especialidades implicadas.", False),
    ("5. Reconstrucción del complejo areola-pezón (si procede): fase final, ambulatoria, con anestesia local o local y sedación.", False),
    ("6. Seguimiento: revisiones coordinadas con el equipo oncológico de la paciente.", False),
    ("", False),
    ("H2: Preguntas frecuentes sobre reconstrucción mamaria post mastectomía", True),
    ("", False),
    ("H3: ¿Cuál es el momento adecuado para la reconstrucción mamaria?", True),
    ("Depende del contexto clínico de cada paciente. Puede realizarse de forma inmediata, en el mismo tiempo quirúrgico que la extirpación del tumor, o de forma diferida, una vez finalizado el tratamiento oncológico.", False),
    ("", False),
    ("H3: ¿Hay una técnica de reconstrucción mejor que otras?", True),
    ("No. La calidad de vida tras la reconstrucción no depende de la estrategia elegida, sino de que la técnica sea compatible con la historia oncológica y las necesidades de la paciente. Todas las opciones —implantes, colgajos, microcirugía, injerto graso o combinaciones— deben valorarse de forma individual.", False),
    ("", False),
    ("H3: ¿La reconstrucción mamaria devuelve el aspecto natural del pecho?", True),
    ("No exactamente. El procedimiento reconstruye la mama, pero no repone el seno natural. Habrá diferencias de tamaño, contorno, simetría, textura y cicatrices respecto a la mama no intervenida, que se explican con detalle antes de decidir.", False),
    ("", False),
    ("H3: ¿Es necesaria la reconstrucción de la areola y el pezón?", True),
    ("No es obligatoria, pero muchas pacientes la completan como fase final. Es un procedimiento ambulatorio, con anestesia local, que a menudo se combina con un pequeño injerto de grasa.", False),
    ("", False),
    ("H3: ¿Qué complicaciones puede tener la reconstrucción mamaria?", True),
    ("Como todo procedimiento quirúrgico, tiene un abanico de complicaciones posibles que el cirujano explica de forma detallada antes de la intervención, recogidas en el consentimiento informado.", False),
    ("", False),
    ("H3: ¿La reconstrucción mamaria post mastectomía tiene financiación o facilidades de pago?", True),
    ("En Diagonal CQ podemos informarte sobre las opciones de financiación disponibles en la consulta de valoración.", False),
    ("", False),
    ("H3: ¿Se coordina la reconstrucción con mi equipo de oncología?", True),
    ("Sí. El Dr. Joan Benítez coordina el proceso con cirugía mamaria, oncología, radiología, anatomía patológica y radioterapia, para que la reconstrucción sea compatible con el tratamiento del cáncer.", False),
    ("", False),
    ("H2: Por qué elegir Diagonal CQ para tu reconstrucción mamaria en Córdoba", True),
    ("En Diagonal CQ acompañamos a cada paciente con información realista sobre lo que la reconstrucción puede conseguir, coordinación estrecha con su equipo oncológico y una decisión compartida sobre la estrategia más adecuada. Somos una clínica de referencia en Córdoba, dentro de nuestra unidad de cirugía plástica y reparadora, para pacientes que buscan recuperar su integridad corporal tras el tratamiento del cáncer de mama.", False, [("unidad de cirugía plástica y reparadora", URL_CIRUGIA_PLASTICA)]),
    ("", False),
    ("Solicita tu valoración personalizada y resuelve tus dudas sobre el proceso de reconstrucción.", False),
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
