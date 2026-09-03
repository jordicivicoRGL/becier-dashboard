# -*- coding: utf-8 -*-
"""
Script para escribir el texto de la Home de Diagonal CQ en Google Docs.
Formato: Arial 11, NORMAL_TEXT, prefijos H1:/H2:/H3: en negrita.
Sin tabla (no aplica a texto de home).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1QN41nJcgLGP_Hr4_Mhwi2g1ShkjPZwc7xO50-OPI4CY"
TAB_ID = "t.p9oyu53xryl0"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita)
# ---------------------------------------------------------------------------
BLOCKS = [
    ("Meta title: Clínica de Cirugía Estética en Córdoba | Diagonal CQ", False),
    ("Meta description: Clínica de cirugía y medicina estética en Córdoba dirigida por el Dr. Joan Benítez. Resultados naturales y seguros. Pide tu valoración sin compromiso.", False),
    ("", False),

    ("H1: Clínica de Cirugía Estética en Córdoba", True),
    ("Diagonal CQ es una clínica de cirugía estética en Córdoba especializada en resultados naturales y seguros. Coordinamos diagnóstico y tratamiento en un mismo centro, con la experiencia del Dr. Joan Benítez al frente de cada intervención.", False),
    ("CTA: Pide tu valoración", False),
    ("", False),

    ("H2: Una clínica en Córdoba pensada para cada paciente", True),
    ("En Diagonal CQ ponemos formación, experiencia y tecnología actual al servicio de cada persona que nos visita. Cada caso se valora de forma individual, sin protocolos estándar ni resultados forzados: el objetivo es siempre una mejora natural y acorde a lo que cada paciente necesita.", False),
    ("", False),

    ("H2: Especialidades en Diagonal CQ", True),
    ("H3: Cirugía Estética", True),
    ("Es el núcleo de Diagonal CQ: intervenciones como mamoplastia, liposucción, abdominoplastia o blefaroplastia, realizadas con planificación quirúrgica individualizada.", False),
    ("", False),
    ("H3: Medicina Estética", True),
    ("Tratamientos no invasivos o mínimamente invasivos con láser y tecnología médica para mejorar la piel y ralentizar signos de envejecimiento, sin cirugía.", False),
    ("", False),
    ("H3: Cirugía Plástica y Reparadora", True),
    ("Reconstrucción mamaria tras cáncer de mama, tratamiento de heridas y quemaduras, y otras intervenciones reparadoras, con un enfoque funcional además de estético.", False),
    ("", False),
    ("H3: Unidad de Cirugía Post Pérdida de Peso", True),
    ("Acompañamos a quienes han perdido mucho peso, tras cirugía bariátrica, dieta o ejercicio, con un plan de cirugía reparadora personalizado para completar ese cambio.", False),
    ("", False),

    ("H2: Tratamientos más solicitados", True),
    ("Cirugía Estética: Mamoplastia de aumento, Liposucción, Blefaroplastia", False),
    ("Medicina Estética: Rejuvenecimiento facial láser, Remodelación corporal", False),
    ("Cirugía Plástica y Reparadora: Reconstrucción mamaria", False),
    ("Unidad Post Pérdida de Peso: Cirugía post pérdida de peso, Abdominoplastia", False),
    ("(cada tratamiento enlaza a su página correspondiente)", False),
    ("", False),

    ("H2: Nuestro equipo médico", True),
    ("Diagonal CQ está dirigida por el Dr. Joan Benítez, especialista en Cirugía Plástica, Reparadora y Estética con más de 25 años de experiencia. Le acompaña un equipo de especialistas en medicina estética, láser, enfermería y anestesia, todos con formación específica en su área.", False),
    ("CTA: Conoce al equipo → /equipo/", False),
    ("", False),

    ("H2: ¿Empezamos?", True),
    ("Cuéntanos qué te gustaría mejorar y te ayudamos a decidir el mejor camino, sin compromiso. Estamos en Córdoba, en Pintora María Blanchard, 1.", False),
    ("CTA final: Pide tu cita", False),
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
    inserts = []
    bold_ranges = []
    idx = start_index
    for text, is_bold in preprocess_blocks(blocks):
        full = text + "\n"
        n = utf16_len(full)
        inserts.append({"insertText": {"location": loc(idx), "text": full}})
        if is_bold and text:
            bold_ranges.append((idx, idx + n))
        idx += n
    return inserts, bold_ranges, idx

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

print("Insertando contenido...")
inserts, bold_ranges, final_idx = build_text_requests(BLOCKS, 1)
service.documents().batchUpdate(documentId=DOC_ID, body={"requests": inserts}).execute()
print(f"  Contenido insertado. Indice final: {final_idx}")

print("Aplicando Arial 11...")
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"updateTextStyle": {
        "range": rng(1, final_idx),
        "textStyle": {
            "weightedFontFamily": {"fontFamily": "Arial"},
            "fontSize": {"magnitude": 11, "unit": "PT"},
        },
        "fields": "weightedFontFamily,fontSize",
    }}]},
).execute()

print("Aplicando negrita a headings...")
bold_reqs = [
    {"updateTextStyle": {"range": rng(s, e), "textStyle": {"bold": True}, "fields": "bold"}}
    for s, e in bold_ranges
]
if bold_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": bold_reqs}).execute()
print(f"  {len(bold_reqs)} headings en negrita.")

print("\nDocumento completado con exito.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
