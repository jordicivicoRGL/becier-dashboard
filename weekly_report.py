#!/usr/bin/env python3
"""
Informe semanal Becier — Meta Ads + Google Ads
Uso: python weekly_report.py
Automatización: Task Scheduler, lunes 07:00
"""

import os
import sys
import json
import re
import calendar
import base64
from email.mime.text import MIMEText
from datetime import date, timedelta

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import anthropic
from googleapiclient.discovery import build

from tools.facebook_ads_tools import get_campaigns_insights_range
from tools.ads_tools import get_campaigns_stats_range
from tools.calendar_tools import get_google_credentials

# ── Configuración ─────────────────────────────────────────────────────────────
DOC_ID   = "1aw_QxRhAOPuC0bZerRXK9tM-xsD5bO_CndXyGbFnxL0"
SHEET_ID = "1Hayb94Pr2XO1YI1-V9IQUbL5M2qNKjXSItNfDvqWdYc"
META_ACCOUNT   = "becier"
GOOGLE_ACCOUNT = "becier"
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"

# Colores para Google Docs (texto)
GREEN = {"red": 0.07, "green": 0.53, "blue": 0.26}
RED   = {"red": 0.80, "green": 0.07, "blue": 0.07}

# Colores de fondo para Google Sheets
SH_GREEN  = {"red": 0.82, "green": 0.93, "blue": 0.83}   # verde suave
SH_RED    = {"red": 0.96, "green": 0.80, "blue": 0.80}   # rojo suave
SH_HEADER = {"red": 0.20, "green": 0.20, "blue": 0.20}   # gris oscuro
SH_WEEK   = {"red": 0.83, "green": 0.91, "blue": 0.98}   # azul suave
SH_TOTAL  = {"red": 0.93, "green": 0.93, "blue": 0.93}   # gris claro
SH_PREV   = {"red": 0.93, "green": 0.93, "blue": 0.93}   # mismo gris que TOTAL (sem. anterior)
SH_WHITE  = {"red": 1.00, "green": 1.00, "blue": 1.00}

# Colores para tabla en Google Docs
DOC_HEADER_BG    = {"red": 0.13, "green": 0.13, "blue": 0.13}
DOC_PREV_ROW_BG  = {"red": 0.94, "green": 0.94, "blue": 0.94}
DOC_TOTAL_ROW_BG = {"red": 0.82, "green": 0.82, "blue": 0.82}
DOC_GRAY_TEXT    = {"red": 0.50, "green": 0.50, "blue": 0.50}


# ── Fechas ────────────────────────────────────────────────────────────────────
def calculate_dates() -> dict:
    today = date.today()
    dow = today.weekday()

    last_sunday  = today - timedelta(days=dow + 1)
    last_monday  = last_sunday - timedelta(days=6)
    prev_sunday  = last_monday - timedelta(days=1)
    prev_monday  = prev_sunday - timedelta(days=6)

    month_start = today.replace(day=1)
    month_end   = last_sunday

    prev_month_last  = month_start - timedelta(days=1)
    prev_month_start = prev_month_last.replace(day=1)
    day_delta        = (month_end - month_start).days
    prev_month_end_c = prev_month_start + timedelta(days=day_delta)
    _, pm_days = calendar.monthrange(prev_month_start.year, prev_month_start.month)
    prev_month_end = prev_month_end_c if prev_month_end_c.day <= pm_days else prev_month_last

    return {
        "week":       (last_monday,       last_sunday),
        "prev_week":  (prev_monday,       prev_sunday),
        "month":      (month_start,       month_end),
        "prev_month": (prev_month_start,  prev_month_end),
    }


# ── Clasificación ─────────────────────────────────────────────────────────────
def classify_meta_campaign(name: str) -> str:
    n = name.upper()
    if "LEAD" in n:
        return "Lead Ad"
    if "ALCANCE" in n:
        return "Alcance"
    if "LE" in n:
        return "Landing"
    return "Otro"


def get_meta_conversion(campaign_type: str, actions: dict) -> int:
    if campaign_type == "Lead Ad":
        return actions.get("lead", 0)
    if campaign_type == "Landing":
        return (actions.get("offsite_conversion.fb_pixel_lead", 0)
                or actions.get("lead", 0)
                or actions.get("complete_registration", 0))
    return 0


def classify_google_campaign(name: str) -> str:
    n = name.upper()
    if "VEHICLES" in n:
        return "VEHICLES"
    if "GRUP-BECIER" in n or "GRUP BECIER" in n:
        return "GRUP-BECIER"
    if "BECSER" in n:
        return "BECSER"
    if "BECAR" in n:
        return "BECAR"
    return "Otro"


# ── Aggregación Google ────────────────────────────────────────────────────────
def aggregate_google(campaigns: list) -> dict:
    groups: dict = {}
    for c in campaigns:
        line = classify_google_campaign(c["name"])
        if line not in groups:
            groups[line] = {"spend": 0.0, "impressions": 0, "clicks": 0,
                            "conversions": 0.0, "campaigns": 0}
        g = groups[line]
        g["spend"]       += c["cost_eur"]
        g["impressions"] += c["impressions"]
        g["clicks"]      += c["clicks"]
        g["conversions"] += c["conversions"]
        g["campaigns"]   += 1

    for g in groups.values():
        g["ctr"]  = round(g["clicks"] / g["impressions"] * 100, 2) if g["impressions"] else 0.0
        g["cpc"]  = round(g["spend"] / g["clicks"], 2)             if g["clicks"]      else 0.0
        g["cpm"]  = round(g["spend"] / g["impressions"] * 1000, 2) if g["impressions"] else 0.0
        g["cpa"]  = round(g["spend"] / g["conversions"], 2)        if g["conversions"] else 0.0
        g["spend"] = round(g["spend"], 2)

    return groups


# ── Helpers de formato ────────────────────────────────────────────────────────
def fmt_eur(val: float) -> str:
    return f"{val:.2f}€"

def fmt_pct(val: float) -> str:
    return f"{val:.2f}%"

def fmt_num(val: float) -> str:
    v = int(val)
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v/1_000:.1f}K"
    return str(v)

def pct_change(current: float, previous: float) -> str:
    if not previous:
        return "N/D"
    change = (current - previous) / previous * 100
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.1f}%"

def shorten(name: str, maxlen: int = 32) -> str:
    return name if len(name) <= maxlen else name[:maxlen - 1] + "…"


def _doc_row_bg_req(table_start: int, row_idx: int, n_cols: int, bg: dict) -> dict:
    return {
        "updateTableCellStyle": {
            "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": bg}}},
            "fields": "backgroundColor",
            "tableRange": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start},
                    "rowIndex": row_idx,
                    "columnIndex": 0,
                },
                "rowSpan": 1,
                "columnSpan": n_cols,
            },
        }
    }


# ── Tabla Meta — formato fila actual + fila anterior por campaña ──────────────
META_CAM_HEADERS = ["Campaña", "Tipo", "Período", "Gasto", "CPM", "CTR", "CPC", "Conv.", "CPL"]
# col idx: 0=Campaña 1=Tipo 2=Período 3=Gasto 4=CPM 5=CTR 6=CPC 7=Conv 8=CPL
# Columnas a colorear en la fila "Sem. actual" y si lower_is_better
META_METRIC_COLS = {
    3: False,   # Gasto: más = neutral, no color
    4: True,    # CPM: lower is better
    5: False,   # CTR: higher is better
    6: True,    # CPC: lower is better
    7: False,   # Conv.: higher is better
    8: True,    # CPL: lower is better
}


def _cell_color(current: float, previous: float, lower_is_better: bool):
    """Devuelve 'green', 'red' o None según si la métrica mejoró."""
    if not previous or current == previous:
        return None
    improved = (current < previous) if lower_is_better else (current > previous)
    return "green" if improved else "red"


def meta_campaign_paired_rows(week_cams: list, prev_cams: list):
    """
    Devuelve (flat_rows, cell_colors) donde:
    - flat_rows: lista de filas (actual + anterior por campaña + fila total)
    - cell_colors: dict {row_idx: {col_idx: 'green'|'red'}} para fila actual
    """
    prev_by_name = {c["campaign_name"]: c for c in prev_cams}
    flat_rows   = []
    cell_colors = {}   # {row_index_in_flat: {col_idx: color}}

    for c in sorted(week_cams, key=lambda x: x["spend_eur"], reverse=True):
        prev      = prev_by_name.get(c["campaign_name"], {})
        t         = classify_meta_campaign(c["campaign_name"])
        conv      = get_meta_conversion(t, c["actions"])
        prev_conv = get_meta_conversion(t, prev.get("actions", {})) if prev else 0
        cpl       = round(c["spend_eur"] / conv, 2) if conv else 0
        prev_cpl  = round(prev.get("spend_eur", 0) / prev_conv, 2) if prev_conv else 0

        # Fila semana actual
        cur_row = [
            shorten(c["campaign_name"]),
            t,
            fmt_eur(c["spend_eur"]),
            fmt_eur(c["cpm"]),
            fmt_pct(c["ctr_pct"]),
            fmt_eur(c["cpc"]),
            str(conv),
            fmt_eur(cpl) if cpl else "—",
        ]
        # Fila semana anterior
        prev_row = [
            "",
            "",
            fmt_eur(prev.get("spend_eur", 0)),
            fmt_eur(prev.get("cpm", 0)),
            fmt_pct(prev.get("ctr_pct", 0)),
            fmt_eur(prev.get("cpc", 0)),
            str(prev_conv),
            fmt_eur(prev_cpl) if prev_cpl else "—",
        ]

        # Colores para la fila actual (comparando con anterior)
        raw_vals = {
            3: (c["cpm"],     prev.get("cpm", 0),     True),
            4: (c["ctr_pct"], prev.get("ctr_pct", 0), False),
            5: (c["cpc"],     prev.get("cpc", 0),     True),
            6: (float(conv),  float(prev_conv),        False),
            7: (cpl,          prev_cpl,                True),
        }
        row_colors = {}
        for col, (cur_v, prev_v, lib) in raw_vals.items():
            c_color = _cell_color(cur_v, prev_v, lib)
            if c_color:
                row_colors[col] = c_color

        cur_row_idx = len(flat_rows)   # índice en flat_rows (base 0, +1 para cabecera)
        cell_colors[cur_row_idx] = row_colors
        flat_rows.append(cur_row)
        flat_rows.append(prev_row)

    # Fila total al final
    total_spend  = sum(c["spend_eur"] for c in week_cams)
    total_conv   = sum(get_meta_conversion(classify_meta_campaign(c["campaign_name"]), c["actions"]) for c in week_cams)
    total_cpl    = round(total_spend / total_conv, 2) if total_conv else 0
    flat_rows.append(["TOTAL", "—",
                      fmt_eur(total_spend), "—", "—", "—",
                      str(total_conv), fmt_eur(total_cpl) if total_cpl else "—"])

    return flat_rows, cell_colors


# ── Filas Google por línea ────────────────────────────────────────────────────
GOOGLE_LINES   = ["VEHICLES", "BECAR", "GRUP-BECIER", "BECSER", "Otro"]
GOOGLE_HEADERS = [
    "Línea", "Gasto", "vs%",
    "CPM", "vs%", "CTR", "vs%",
    "CPC", "vs%", "Conv.", "CPA", "vs%"
]
GOOGLE_COLOR_COLS  = [2, 4, 6, 8, 11]
GOOGLE_INVERT_COLS = [4, 8, 11]  # CPM, CPC, CPA: bajar es bueno


def google_line_rows(current: dict, previous: dict) -> list:
    rows = []
    for line in GOOGLE_LINES:
        if line not in current:
            continue
        g  = current[line]
        pg = previous.get(line, {})
        rows.append([
            line,
            fmt_eur(g["spend"]),
            pct_change(g["spend"],       pg.get("spend", 0)),
            fmt_eur(g["cpm"]),
            pct_change(g["cpm"],         pg.get("cpm", 0)),
            fmt_pct(g["ctr"]),
            pct_change(g["ctr"],         pg.get("ctr", 0)),
            fmt_eur(g["cpc"]),
            pct_change(g["cpc"],         pg.get("cpc", 0)),
            str(int(g["conversions"])),
            fmt_eur(g["cpa"]) if g["cpa"] else "—",
            pct_change(g["cpa"],         pg.get("cpa", 0)),
        ])

    spend  = sum(g["spend"]       for g in current.values())
    pspend = sum(g["spend"]       for g in previous.values())
    conv   = sum(g["conversions"] for g in current.values())
    rows.append([
        "TOTAL",
        fmt_eur(spend), pct_change(spend, pspend),
        "—", "—", "—", "—", "—", "—",
        str(int(conv)), "—", "—"
    ])
    return rows


# ── Análisis con Claude ───────────────────────────────────────────────────────
ANALYSIS_SYSTEM_PROMPT = """Eres un experto en paid media analizando el rendimiento semanal de Becier, empresa española de vehículos y servicios de movilidad (coches de ocasión, rent a car, seguros).

TONO Y LENGUAJE:
- Profesional y medido. Sin términos alarmistas ("colapsa", "desploma", "catástrofe").
- Para métricas sin datos usa: "sin conversiones registradas esta semana", "aún sin resultados", "pendiente de registros".
- Para métricas que empeoran: "ha bajado", "requiere atención", "por debajo de la semana anterior".

EVALUACIÓN DE MÉTRICAS:
- CPM: bajar = bueno (alcance más barato). Subir = requiere atención.
- CTR: subir = bueno (más relevancia). Bajar = requiere atención.
- CPC: bajar = bueno. Subir = requiere atención.
- CPL/CPA: bajar = bueno. Subir = requiere atención.
- Conversiones: subir = bueno. Sin datos = "sin conversiones registradas esta semana".

FRAMEWORK:
- Para cada métrica: valor actual, variación vs semana anterior, si mejora o requiere atención, causa más probable.
- Causas habituales: saturación de audiencia, estacionalidad, calidad del anuncio, competencia, cambios de puja.
- Si hay tendencia histórica de semanas previas, úsala para distinguir si algo es puntual o sostenido.
- Si hay contexto adicional de la semana, úsalo para explicar anomalías.

Líneas de negocio Becier:
- VEHICLES: venta de coches de ocasión
- BECAR: rent a car
- GRUP-BECIER: marca corporativa
- BECSER: servicios (seguros, financiación)

FORMATO DE RESPUESTA — JSON estricto, sin texto adicional ni bloques markdown:
{
  "meta": {
    "campaign_summaries": [
      "• **[Nombre corto campaña]** ([Tipo]): [valoración general 1 frase]. CPM X€ (vs X€ ant.) — [bien/atención]: [causa en 6-8 palabras]. CTR X% (vs X% ant.) — [bien/atención]: [causa]. CPC X€ — [bien/atención]: [causa]. Conv./Interacciones X — [bien/atención/sin datos]: [causa].",
      "• **[Otra campaña]** ([Tipo]): ..."
    ],
    "conclusiones": [
      "### [Nombre corto campaña 1]",
      "• **CPM**: [valor actual] vs [valor anterior] ([variación%]). [Valoración] — [causa detallada en 1-2 frases].",
      "• **CTR**: ...",
      "• **CPC**: ...",
      "• **Conversiones/Interacciones**: ...",
      "### [Nombre corto campaña 2]",
      "• **CPM**: ..."
    ],
    "next_steps": [
      "• **[Acción concreta]**: [qué hacer y por qué, 1-2 frases]"
    ]
  },
  "google": {
    "campaign_summaries": [
      "• **[Línea]**: [valoración general]. CPM X€ — [bien/atención]: [causa]. CTR X% — [bien/atención]: [causa]. CPC X€ — [bien/atención]: [causa]. Conv. X / CPA X€ — [bien/atención/sin datos]: [causa]."
    ],
    "conclusiones": [
      "### [Línea de negocio 1]",
      "• **CPM**: ...",
      "• **CTR**: ...",
      "• **CPC**: ...",
      "• **Conversiones/CPA**: ..."
    ],
    "next_steps": [
      "• **[Acción]**: [detalle]"
    ]
  }
}"""


def generate_analysis(meta_wk, meta_pw, meta_mo, meta_pm,
                      goog_wk, goog_pw, goog_mo, goog_pm,
                      dates: dict,
                      week_context: str = "",
                      historical: str = "") -> dict:
    client = anthropic.Anthropic()
    wk = dates["week"]
    week_label = f"{wk[0].strftime('%d/%m')} - {wk[1].strftime('%d/%m/%Y')}"

    def cam_summary(cams, prev_cams):
        prev = {c["campaign_name"]: c for c in prev_cams}
        lines = []
        for c in sorted(cams, key=lambda x: x["spend_eur"], reverse=True):
            p    = prev.get(c["campaign_name"], {})
            t    = classify_meta_campaign(c["campaign_name"])
            conv = get_meta_conversion(t, c["actions"])
            cpl  = round(c["spend_eur"] / conv, 2) if conv else 0
            pcpl = round(p.get("spend_eur", 0) / get_meta_conversion(t, p.get("actions", {})), 2) \
                   if get_meta_conversion(t, p.get("actions", {})) else 0
            lines.append(
                f"  {shorten(c['campaign_name'], 40)}: gasto={c['spend_eur']:.2f}€ "
                f"CPM={c['cpm']:.2f} CTR={c['ctr_pct']:.2f}% CPC={c['cpc']:.2f} "
                f"conv={conv} CPL={cpl:.2f}€ "
                f"(sem.ant: CPM={p.get('cpm',0):.2f} CTR={p.get('ctr_pct',0):.2f}% CPL={pcpl:.2f}€)"
            )
        return "\n".join(lines)

    def goog_summary(current, previous):
        lines = []
        for line in GOOGLE_LINES:
            if line not in current:
                continue
            g  = current[line]
            pg = previous.get(line, {})
            lines.append(
                f"  {line}: gasto={g['spend']:.2f}€ "
                f"CPM={g['cpm']:.2f} CTR={g['ctr']:.2f}% CPC={g['cpc']:.2f} "
                f"conv={int(g['conversions'])} CPA={g['cpa']:.2f}€ "
                f"(sem.ant: CPM={pg.get('cpm',0):.2f} CTR={pg.get('ctr',0):.2f}% CPA={pg.get('cpa',0):.2f}€)"
            )
        return "\n".join(lines)

    engega_note = ""
    if any("ENGEGA" in c["campaign_name"].upper() for c in meta_wk):
        engega_note = "\nNOTA ESPECIAL PLA-ENGEGA: Las conversiones de campañas PLA-ENGEGA son interacciones con el botón de la landing, no leads reales. No interpretar como captación de clientes, sino como engagement con la oferta. Indícalo en el análisis de esa campaña."

    user_prompt = f"""SEMANA: {week_label}
{f"CONTEXTO DE ESTA SEMANA: {week_context}" if week_context else ""}
{historical if historical else ""}
=== META ADS — Semana actual vs anterior (campaña por campaña) ==={engega_note}
{cam_summary(meta_wk, meta_pw)}

=== META ADS — Mes actual vs mes anterior ===
{cam_summary(meta_mo, meta_pm)}

=== GOOGLE ADS — Semana actual vs anterior (por línea de negocio) ===
{goog_summary(goog_wk, goog_pw)}

=== GOOGLE ADS — Mes actual vs mes anterior ===
{goog_summary(goog_mo, goog_pm)}"""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            system=[{
                "type": "text",
                "text": ANALYSIS_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text.strip()
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return json.loads(m.group())
    except Exception as e:
        print(f"  AVISO analisis Claude: {e}")

    return {
        "meta":   {"campaign_summaries": ["Análisis no disponible."], "conclusiones": [], "next_steps": []},
        "google": {"campaign_summaries": ["Análisis no disponible."], "conclusiones": [], "next_steps": []},
    }


# ── Google Docs helpers ───────────────────────────────────────────────────────
def get_docs_service():
    return build("docs", "v1", credentials=get_google_credentials())


def _get_end_index(service, doc_id: str) -> int:
    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    return max(1, body[-1].get("endIndex", 2) - 1) if body else 1


def clear_doc(service, doc_id: str) -> None:
    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    end_index = body[-1].get("endIndex", 2) if body else 2
    if end_index > 2:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end_index - 1}
            }}]}
        ).execute()


def _utf16_len(text: str) -> int:
    return sum(2 if ord(c) > 0xFFFF else 1 for c in text)


def _parse_bold(line: str):
    """Parsea **bold** en una línea. Devuelve (texto_limpio, [(start, end)])."""
    plain, spans, i = "", [], 0
    while i < len(line):
        if line[i:i+2] == "**":
            j = line.find("**", i + 2)
            if j != -1:
                start = len(plain)
                plain += line[i+2:j]
                spans.append((start, len(plain)))
                i = j + 2
            else:
                plain += line[i]; i += 1
        else:
            plain += line[i]; i += 1
    return plain, spans


def append_text(service, doc_id: str, content: str) -> None:
    end_index = _get_end_index(service, doc_id)

    blocks = []
    for line in content.split("\n"):
        line = line.rstrip()
        if line.startswith("### "):
            plain, spans = _parse_bold(line[4:])
            blocks.append(("HEADING_3", plain, spans, False))
        elif line.startswith("## "):
            plain, spans = _parse_bold(line[3:])
            blocks.append(("HEADING_2", plain, spans, False))
        elif line.startswith("# "):
            plain, spans = _parse_bold(line[2:])
            blocks.append(("HEADING_1", plain, spans, False))
        elif line.startswith("• "):
            plain, spans = _parse_bold(line[2:])
            blocks.append(("NORMAL_TEXT", plain, spans, True))   # True = bullet real
        else:
            plain, spans = _parse_bold("" if line == "---" else line)
            blocks.append(("NORMAL_TEXT", plain, spans, False))

    FONT_SIZE = {"HEADING_1": 16, "HEADING_2": 13, "HEADING_3": 11, "NORMAL_TEXT": 10}

    insert_reqs, style_reqs, bold_reqs, font_reqs = [], [], [], []
    bullet_ranges = []
    cur = end_index

    for style, text, bold_spans, is_bullet in blocks:
        full = text + "\n"
        tlen = _utf16_len(full)
        insert_reqs.append({"insertText": {"location": {"index": cur}, "text": full}})
        if style != "NORMAL_TEXT" and text:
            style_reqs.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": cur, "endIndex": cur + tlen},
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            })
        for s, e in bold_spans:
            doc_s = cur + _utf16_len(text[:s])
            doc_e = cur + _utf16_len(text[:e])
            if doc_e > doc_s:
                bold_reqs.append({
                    "updateTextStyle": {
                        "range": {"startIndex": doc_s, "endIndex": doc_e},
                        "textStyle": {"bold": True},
                        "fields": "bold",
                    }
                })
        if text:
            font_reqs.append({
                "updateTextStyle": {
                    "range": {"startIndex": cur, "endIndex": cur + tlen - 1},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Arial"},
                        "fontSize": {"magnitude": FONT_SIZE.get(style, 10), "unit": "PT"},
                    },
                    "fields": "weightedFontFamily,fontSize",
                }
            })
        if is_bullet:
            bullet_ranges.append((cur, cur + tlen))
        cur += tlen

    service.documents().batchUpdate(
        documentId=doc_id, body={"requests": insert_reqs + style_reqs}
    ).execute()
    if bold_reqs:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": bold_reqs}
        ).execute()
    if font_reqs:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": font_reqs}
        ).execute()
    if bullet_ranges:
        bullet_reqs = [
            {
                "createParagraphBullets": {
                    "range": {"startIndex": start, "endIndex": end},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            }
            for start, end in bullet_ranges
        ]
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": bullet_reqs}
        ).execute()


def insert_table(service, doc_id: str, headers: list, rows: list,
                 color_cols: list = None, invert_cols: list = None) -> None:
    """
    Inserta tabla al final del doc.
    color_cols: índices de columnas con vs% (+ verde / - rojo)
    invert_cols: subconjunto de color_cols donde el color se invierte (bajar es bueno)
    """
    end_index = _get_end_index(service, doc_id)
    n_rows = len(rows) + 1
    n_cols = len(headers)

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertTable": {
            "rows": n_rows, "columns": n_cols,
            "location": {"index": end_index}
        }}]}
    ).execute()

    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    table_element = next((e["table"] for e in reversed(body) if "table" in e), None)
    if not table_element:
        return

    # Recopilar (idx, texto, row_idx, col_idx) en orden inverso de índice
    all_rows_data = [headers] + rows
    insertions = []
    for row_idx, (table_row, data_row) in enumerate(
            zip(table_element.get("tableRows", []), all_rows_data)):
        for col_idx, (cell, cell_value) in enumerate(
                zip(table_row.get("tableCells", []), data_row)):
            cell_content = cell.get("content", [])
            if not cell_content or "paragraph" not in cell_content[0]:
                continue
            elements = cell_content[0]["paragraph"].get("elements", [])
            if not elements:
                continue
            idx = elements[0].get("startIndex", cell_content[0].get("startIndex", 0))
            insertions.append((idx, str(cell_value), row_idx, col_idx))

    insertions.sort(key=lambda x: x[0], reverse=True)
    text_requests = [
        {"insertText": {"location": {"index": idx}, "text": text}}
        for idx, text, _, _ in insertions
    ]
    if not text_requests:
        return

    service.documents().batchUpdate(
        documentId=doc_id, body={"requests": text_requests}
    ).execute()

    # Re-leer para aplicar estilos (negrita cabecera + colores)
    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    table_element = next((e["table"] for e in reversed(body) if "table" in e), None)
    if not table_element:
        return

    format_requests = []
    all_rows_data = [headers] + rows
    color_cols   = set(color_cols or [])
    invert_cols  = set(invert_cols or [])

    for row_idx, (table_row, data_row) in enumerate(
            zip(table_element.get("tableRows", []), all_rows_data)):
        for col_idx, (cell, cell_value) in enumerate(
                zip(table_row.get("tableCells", []), data_row)):
            for para in cell.get("content", []):
                if "paragraph" not in para:
                    continue
                for elem in para["paragraph"].get("elements", []):
                    if "textRun" not in elem:
                        continue
                    start = elem["startIndex"]
                    end   = elem["endIndex"] - 1  # excluir \n
                    if end <= start:
                        continue

                    text_style = {}

                    # Negrita en cabecera
                    if row_idx == 0:
                        text_style["bold"] = True

                    # Color en columnas vs%
                    if col_idx in color_cols and row_idx > 0:
                        val = str(cell_value).strip()
                        is_positive = val.startswith("+")
                        is_negative = val.startswith("-")
                        if is_positive or is_negative:
                            if col_idx in invert_cols:
                                color = RED if is_positive else GREEN
                            else:
                                color = GREEN if is_positive else RED
                            text_style["foregroundColor"] = {"color": {"rgbColor": color}}

                    if text_style:
                        format_requests.append({
                            "updateTextStyle": {
                                "range": {"startIndex": start, "endIndex": end},
                                "textStyle": text_style,
                                "fields": ",".join(text_style.keys()),
                            }
                        })

    if format_requests:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": format_requests}
        ).execute()


def insert_paired_table(service, doc_id: str, headers: list,
                        flat_rows: list, cell_colors: dict) -> None:
    end_index = _get_end_index(service, doc_id)
    n_rows = len(flat_rows) + 1
    n_cols = len(headers)

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertTable": {
            "rows": n_rows, "columns": n_cols,
            "location": {"index": end_index}
        }}]}
    ).execute()

    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    full_table_elem = next((e for e in reversed(body) if "table" in e), None)
    table_element   = full_table_elem["table"] if full_table_elem else None
    table_start_idx = full_table_elem.get("startIndex", 0) if full_table_elem else 0
    if not table_element:
        return

    all_rows_data = [headers] + flat_rows
    insertions = []
    for row_idx, (table_row, data_row) in enumerate(
            zip(table_element.get("tableRows", []), all_rows_data)):
        for col_idx, (cell, cell_value) in enumerate(
                zip(table_row.get("tableCells", []), data_row)):
            cell_content = cell.get("content", [])
            if not cell_content or "paragraph" not in cell_content[0]:
                continue
            elements = cell_content[0]["paragraph"].get("elements", [])
            if not elements:
                continue
            idx = elements[0].get("startIndex", cell_content[0].get("startIndex", 0))
            insertions.append((idx, str(cell_value), row_idx, col_idx))

    insertions.sort(key=lambda x: x[0], reverse=True)
    text_reqs = [
        {"insertText": {"location": {"index": idx}, "text": text}}
        for idx, text, _, _ in insertions
        if text
    ]
    if not text_reqs:
        return
    service.documents().batchUpdate(documentId=doc_id, body={"requests": text_reqs}).execute()

    # Re-leer para aplicar estilos
    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])
    full_table_elem = next((e for e in reversed(body) if "table" in e), None)
    table_element   = full_table_elem["table"] if full_table_elem else None
    table_start_idx = full_table_elem.get("startIndex", 0) if full_table_elem else 0
    if not table_element:
        return

    bg_reqs   = []
    fmt_reqs  = []

    for row_idx, (table_row, data_row) in enumerate(
            zip(table_element.get("tableRows", []), all_rows_data)):
        flat_row_idx  = row_idx - 1
        row_color_map = cell_colors.get(flat_row_idx, {})
        first_cell    = str(data_row[0]) if data_row else ""

        is_header = (row_idx == 0)
        is_total  = (not is_header and first_cell == "TOTAL")
        is_prev   = (not is_header and not is_total and first_cell == "")

        if is_header:
            bg_reqs.append(_doc_row_bg_req(table_start_idx, row_idx, n_cols, DOC_HEADER_BG))
        elif is_total:
            bg_reqs.append(_doc_row_bg_req(table_start_idx, row_idx, n_cols, DOC_TOTAL_ROW_BG))
        elif is_prev:
            bg_reqs.append(_doc_row_bg_req(table_start_idx, row_idx, n_cols, DOC_PREV_ROW_BG))

        for col_idx, cell in enumerate(table_row.get("tableCells", [])):
            for para in cell.get("content", []):
                if "paragraph" not in para:
                    continue
                for elem in para["paragraph"].get("elements", []):
                    if "textRun" not in elem:
                        continue
                    start = elem["startIndex"]
                    end   = elem["endIndex"] - 1
                    if end <= start:
                        continue

                    ts        = {}
                    font_size = 9.0

                    if is_header:
                        ts["bold"] = True
                        ts["foregroundColor"] = {"color": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}}
                    elif is_total:
                        ts["bold"] = True
                    elif is_prev:
                        ts["foregroundColor"] = {"color": {"rgbColor": DOC_GRAY_TEXT}}
                        font_size = 8.5
                    else:
                        color_name = row_color_map.get(col_idx)
                        if color_name == "green":
                            ts["foregroundColor"] = {"color": {"rgbColor": GREEN}}
                        elif color_name == "red":
                            ts["foregroundColor"] = {"color": {"rgbColor": RED}}

                    ts["weightedFontFamily"] = {"fontFamily": "Arial"}
                    ts["fontSize"] = {"magnitude": font_size, "unit": "PT"}

                    fields = ["weightedFontFamily", "fontSize"]
                    if "bold" in ts:
                        fields.append("bold")
                    if "foregroundColor" in ts:
                        fields.append("foregroundColor")

                    fmt_reqs.append({
                        "updateTextStyle": {
                            "range": {"startIndex": start, "endIndex": end},
                            "textStyle": ts,
                            "fields": ",".join(fields),
                        }
                    })

    if bg_reqs:
        service.documents().batchUpdate(documentId=doc_id, body={"requests": bg_reqs}).execute()
    if fmt_reqs:
        service.documents().batchUpdate(documentId=doc_id, body={"requests": fmt_reqs}).execute()


# ── Google Sheets ─────────────────────────────────────────────────────────────
def get_sheets_service():
    return build("sheets", "v4", credentials=get_google_credentials())


def _get_or_create_tab(service, name: str) -> int:
    ss = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    for sheet in ss.get("sheets", []):
        if sheet["properties"]["title"] == name:
            return sheet["properties"]["sheetId"]
    resp = service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{"addSheet": {"properties": {"title": name}}}]}
    ).execute()
    return resp["replies"][0]["addSheet"]["properties"]["sheetId"]


def _last_row(service, tab_name: str) -> int:
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{tab_name}'!A:A"
    ).execute()
    return len(result.get("values", []))


def _sh_fmt(sheet_id, r0, r1, c0, c1, **fmt):
    return {"repeatCell": {
        "range": {"sheetId": sheet_id, "startRowIndex": r0, "endRowIndex": r1,
                  "startColumnIndex": c0, "endColumnIndex": c1},
        "cell": {"userEnteredFormat": fmt},
        "fields": "userEnteredFormat(" + ",".join(fmt.keys()) + ")"
    }}


def _write_weekly_tab(service, tab_name: str, headers: list,
                      paired_rows: list, cell_bg: dict,
                      total_row: list, dates: dict,
                      euro_cols: list, pct_cols: list) -> None:
    """
    Escribe datos semanales en un tab de Sheets.
    paired_rows: lista plana de filas (actual + anterior intercaladas)
    cell_bg: {row_idx_en_paired: {col_idx: SH_GREEN|SH_RED}}
    """
    tab_id = _get_or_create_tab(service, tab_name)

    # Limpiar todo el contenido, formato y combinaciones antes de escribir
    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [
            {"unmergeCells": {"range": {"sheetId": tab_id}}},
            {"updateCells": {
                "range": {"sheetId": tab_id},
                "fields": "userEnteredValue,userEnteredFormat"
            }},
        ]}
    ).execute()

    last_row   = 0
    first_time = True
    start      = 0

    wk = dates["week"]
    pw = dates["prev_week"]
    week_label = f"Semana {wk[0].strftime('%d/%m')} - {wk[1].strftime('%d/%m/%Y')}"
    n_cols = len(headers)

    rows_to_write = []
    if first_time:
        rows_to_write.append(headers)
        start += 1

    section_abs = start + len(rows_to_write)   # fila absoluta (0-based) del título de semana
    rows_to_write.append([week_label] + [""] * (n_cols - 1))

    data_start_abs = start + len(rows_to_write)
    rows_to_write.extend(paired_rows)

    total_abs = start + len(rows_to_write)
    rows_to_write.append(total_row)
    rows_to_write.append([""] * n_cols)         # separador vacío

    # ── Escribir valores ──────────────────────────────────────────────────────
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"'{tab_name}'!A{start + 1}",
        valueInputOption="RAW",
        body={"values": rows_to_write}
    ).execute()

    # ── Formatear ─────────────────────────────────────────────────────────────
    fmt_reqs = []
    white_text = {"foregroundColor": SH_WHITE}

    # Cabecera (primera vez)
    if first_time:
        fmt_reqs.append(_sh_fmt(tab_id, 0, 1, 0, n_cols,
            backgroundColor=SH_HEADER,
            textFormat={"bold": True, **white_text},
            horizontalAlignment="CENTER"))
        fmt_reqs.append({"updateSheetProperties": {
            "properties": {"sheetId": tab_id,
                           "gridProperties": {"frozenRowCount": 1}},
            "fields": "gridProperties.frozenRowCount"
        }})

    # Fila título semana
    fmt_reqs.append(_sh_fmt(tab_id, section_abs, section_abs + 1, 0, n_cols,
        backgroundColor=SH_WEEK,
        textFormat={"bold": True},
        horizontalAlignment="LEFT"))
    fmt_reqs.append({"mergeCells": {
        "range": {"sheetId": tab_id,
                  "startRowIndex": section_abs, "endRowIndex": section_abs + 1,
                  "startColumnIndex": 0, "endColumnIndex": n_cols},
        "mergeType": "MERGE_ALL"
    }})

    # Fondo blanco para todas las filas de datos (reset)
    fmt_reqs.append(_sh_fmt(tab_id,
        data_start_abs, total_abs, 0, n_cols,
        backgroundColor=SH_WHITE))

    # Fondo gris muy suave para filas "Sem. anterior" (índices impares en paired_rows)
    for i in range(1, len(paired_rows), 2):
        abs_row = data_start_abs + i
        fmt_reqs.append(_sh_fmt(tab_id,
            abs_row, abs_row + 1, 0, n_cols,
            backgroundColor=SH_PREV))

    # Colores celda a celda en filas "Sem. actual"
    for paired_idx, col_colors in cell_bg.items():
        abs_row = data_start_abs + paired_idx
        for col_idx, bg in col_colors.items():
            fmt_reqs.append(_sh_fmt(tab_id,
                abs_row, abs_row + 1, col_idx, col_idx + 1,
                backgroundColor=bg))

    # Fila TOTAL
    fmt_reqs.append(_sh_fmt(tab_id, total_abs, total_abs + 1, 0, n_cols,
        backgroundColor=SH_HEADER,
        textFormat={"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}))

    # Formatos numéricos (todas las filas de datos + total)
    euro_pat = '#,##0.00"€"'
    pct_pat  = '0.00"%"'
    for col in euro_cols:
        fmt_reqs.append({"repeatCell": {
            "range": {"sheetId": tab_id,
                      "startRowIndex": data_start_abs, "endRowIndex": total_abs + 1,
                      "startColumnIndex": col, "endColumnIndex": col + 1},
            "cell": {"userEnteredFormat": {
                "numberFormat": {"type": "NUMBER", "pattern": euro_pat}}},
            "fields": "userEnteredFormat(numberFormat)"
        }})
    for col in pct_cols:
        fmt_reqs.append({"repeatCell": {
            "range": {"sheetId": tab_id,
                      "startRowIndex": data_start_abs, "endRowIndex": total_abs + 1,
                      "startColumnIndex": col, "endColumnIndex": col + 1},
            "cell": {"userEnteredFormat": {
                "numberFormat": {"type": "NUMBER", "pattern": pct_pat}}},
            "fields": "userEnteredFormat(numberFormat)"
        }})

    # Bordes en filas de datos
    fmt_reqs.append({"updateBorders": {
        "range": {"sheetId": tab_id,
                  "startRowIndex": section_abs, "endRowIndex": total_abs + 1,
                  "startColumnIndex": 0, "endColumnIndex": n_cols},
        "innerHorizontal": {"style": "SOLID", "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
        "innerVertical":   {"style": "SOLID", "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
    }})

    # Alineación derecha para columnas numéricas
    for col in euro_cols + pct_cols:
        fmt_reqs.append(_sh_fmt(tab_id,
            data_start_abs, total_abs + 1, col, col + 1,
            horizontalAlignment="RIGHT"))

    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": fmt_reqs}
    ).execute()

    # Auto-ajuste de columnas tras escribir el contenido
    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{"autoResizeDimensions": {
            "dimensions": {"sheetId": tab_id, "dimension": "COLUMNS",
                           "startIndex": 0, "endIndex": n_cols}
        }}]}
    ).execute()


# Columnas Meta: Semana|Campaña|Tipo|Gasto|CPM|CTR|CPC|Conv.|CPL
META_SHEET_HEADERS = ["Semana", "Campaña", "Tipo",
                      "Gasto €", "CPM €", "CTR %", "CPC €", "Conv.", "CPL €"]
# 0=Semana 1=Campaña 2=Tipo 3=Gasto 4=CPM 5=CTR 6=CPC 7=Conv 8=CPL
META_EURO_COLS = [3, 4, 6, 8]
META_PCT_COLS  = [5]


def write_meta_to_sheet(service, week_cams: list, prev_cams: list, dates: dict) -> None:
    wk = dates["week"]
    pw = dates["prev_week"]
    prev_by_name = {c["campaign_name"]: c for c in prev_cams}

    paired_rows = []
    cell_bg     = {}

    for c in sorted(week_cams, key=lambda x: x["spend_eur"], reverse=True):
        prev      = prev_by_name.get(c["campaign_name"], {})
        t         = classify_meta_campaign(c["campaign_name"])
        conv      = get_meta_conversion(t, c["actions"])
        prev_conv = get_meta_conversion(t, prev.get("actions", {})) if prev else 0
        cpl       = round(c["spend_eur"] / conv, 2) if conv else 0
        prev_cpl  = round(prev.get("spend_eur", 0) / prev_conv, 2) if prev_conv else 0

        cur_idx = len(paired_rows)
        paired_rows.append([
            wk[0].strftime("%d/%m/%Y"), c["campaign_name"], t,
            round(c["spend_eur"], 2), round(c["cpm"], 2), round(c["ctr_pct"], 2),
            round(c["cpc"], 2), conv, cpl or 0,
        ])
        paired_rows.append([
            pw[0].strftime("%d/%m/%Y"), c["campaign_name"], t,
            round(prev.get("spend_eur", 0), 2), round(prev.get("cpm", 0), 2),
            round(prev.get("ctr_pct", 0), 2), round(prev.get("cpc", 0), 2),
            prev_conv, prev_cpl or 0,
        ])

        row_colors = {}
        for col, cur_v, prev_v, lib in [
            (4, c["cpm"],     prev.get("cpm", 0),     True),
            (5, c["ctr_pct"], prev.get("ctr_pct", 0), False),
            (6, c["cpc"],     prev.get("cpc", 0),     True),
            (7, float(conv),  float(prev_conv),        False),
            (8, cpl,          prev_cpl,                True),
        ]:
            c_name = _cell_color(cur_v, prev_v, lib)
            if c_name:
                row_colors[col] = SH_GREEN if c_name == "green" else SH_RED
        if row_colors:
            cell_bg[cur_idx] = row_colors

    total_spend = sum(c["spend_eur"] for c in week_cams)
    total_conv  = sum(get_meta_conversion(classify_meta_campaign(c["campaign_name"]), c["actions"]) for c in week_cams)
    total_cpl   = round(total_spend / total_conv, 2) if total_conv else 0
    total_row   = ["", "TOTAL", "", round(total_spend, 2), "", "", "", total_conv, total_cpl or 0]

    _write_weekly_tab(service, "META ADS", META_SHEET_HEADERS,
                      paired_rows, cell_bg, total_row, dates,
                      META_EURO_COLS, META_PCT_COLS)


# Columnas Google: Semana|Línea|Gasto|CPM|CTR|CPC|Conv.|CPA
GOOGLE_SHEET_HEADERS = ["Semana", "Línea",
                        "Gasto €", "CPM €", "CTR %", "CPC €", "Conv.", "CPA €"]
# 0=Semana 1=Línea 2=Gasto 3=CPM 4=CTR 5=CPC 6=Conv 7=CPA
GOOGLE_EURO_COLS = [2, 3, 5, 7]
GOOGLE_PCT_COLS  = [4]

# Headers para tablas en Google Docs (sin columna Semana)
META_DOC_HEADERS   = ["Campaña", "Tipo", "Gasto €", "CPM €", "CTR %", "CPC €", "Conv.", "CPL €"]
GOOGLE_DOC_HEADERS = ["Línea", "Gasto €", "CPM €", "CTR %", "CPC €", "Conv.", "CPA €"]


def google_doc_paired_rows(goog_wk: dict, goog_pw: dict):
    """Devuelve (flat_rows, cell_colors) para la tabla de Google en Docs."""
    flat_rows   = []
    cell_colors = {}

    for line in GOOGLE_LINES:
        if line not in goog_wk:
            continue
        g  = goog_wk[line]
        pg = goog_pw.get(line, {})

        cur_idx = len(flat_rows)
        flat_rows.append([
            line,
            fmt_eur(g["spend"]), fmt_eur(g["cpm"]), fmt_pct(g["ctr"]),
            fmt_eur(g["cpc"]), str(int(g["conversions"])),
            fmt_eur(g["cpa"]) if g["cpa"] else "—",
        ])
        flat_rows.append([
            "",
            fmt_eur(pg.get("spend", 0)), fmt_eur(pg.get("cpm", 0)), fmt_pct(pg.get("ctr", 0)),
            fmt_eur(pg.get("cpc", 0)), str(int(pg.get("conversions", 0))),
            fmt_eur(pg.get("cpa", 0)) if pg.get("cpa") else "—",
        ])

        row_colors = {}
        for col, cur_v, prev_v, lib in [
            (2, g["cpm"],          pg.get("cpm", 0),         True),
            (3, g["ctr"],          pg.get("ctr", 0),          False),
            (4, g["cpc"],          pg.get("cpc", 0),          True),
            (5, g["conversions"],  pg.get("conversions", 0),  False),
            (6, g["cpa"] or 0,    pg.get("cpa", 0),          True),
        ]:
            c_name = _cell_color(cur_v, prev_v, lib)
            if c_name:
                row_colors[col] = c_name
        if row_colors:
            cell_colors[cur_idx] = row_colors

    total_spend = sum(g["spend"] for g in goog_wk.values())
    total_conv  = sum(g["conversions"] for g in goog_wk.values())
    flat_rows.append(["TOTAL", fmt_eur(total_spend), "—", "—", "—", str(int(total_conv)), "—"])

    return flat_rows, cell_colors


def write_google_to_sheet(service, goog_wk: dict, goog_pw: dict, dates: dict) -> None:
    wk = dates["week"]
    pw = dates["prev_week"]

    paired_rows = []
    cell_bg     = {}

    for line in GOOGLE_LINES:
        if line not in goog_wk:
            continue
        g  = goog_wk[line]
        pg = goog_pw.get(line, {})

        cur_idx = len(paired_rows)
        paired_rows.append([
            wk[0].strftime("%d/%m/%Y"), line,
            round(g["spend"], 2), round(g["cpm"], 2), round(g["ctr"], 2),
            round(g["cpc"], 2), int(g["conversions"]), round(g["cpa"], 2) if g["cpa"] else 0,
        ])
        paired_rows.append([
            pw[0].strftime("%d/%m/%Y"), line,
            round(pg.get("spend", 0), 2), round(pg.get("cpm", 0), 2),
            round(pg.get("ctr", 0), 2), round(pg.get("cpc", 0), 2),
            int(pg.get("conversions", 0)), round(pg.get("cpa", 0), 2),
        ])

        row_colors = {}
        for col, cur_v, prev_v, lib in [
            (3, g["cpm"],          pg.get("cpm", 0),         True),
            (4, g["ctr"],          pg.get("ctr", 0),          False),
            (5, g["cpc"],          pg.get("cpc", 0),          True),
            (6, g["conversions"],  pg.get("conversions", 0),  False),
            (7, g["cpa"],          pg.get("cpa", 0),          True),
        ]:
            c_name = _cell_color(cur_v, prev_v, lib)
            if c_name:
                row_colors[col] = SH_GREEN if c_name == "green" else SH_RED
        if row_colors:
            cell_bg[cur_idx] = row_colors

    total_spend = sum(g["spend"]       for g in goog_wk.values())
    total_conv  = sum(g["conversions"] for g in goog_wk.values())
    total_row   = ["", "TOTAL", round(total_spend, 2), "", "", "", int(total_conv), ""]

    _write_weekly_tab(service, "GOOGLE ADS", GOOGLE_SHEET_HEADERS,
                      paired_rows, cell_bg, total_row, dates,
                      GOOGLE_EURO_COLS, GOOGLE_PCT_COLS)


# ── Histórico desde Google Sheets ────────────────────────────────────────────
def get_historical_summary(sheets_service) -> str:
    """Lee las últimas semanas del Sheet y devuelve un bloque de texto para Claude."""
    lines = []
    tabs = [
        ("META ADS",   3, 4, 5, 6, 7, 8, "CPL"),   # spend, cpm, ctr, cpc, conv, cpl
        ("GOOGLE ADS", 2, 3, 4, 5, 6, 7, "CPA"),
    ]
    for tab, si, cpmi, ctri, cpci, convi, cpai, label in tabs:
        try:
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=SHEET_ID,
                range=f"'{tab}'",
                valueRenderOption="UNFORMATTED_VALUE",
            ).execute()
            rows = result.get("values", [])
        except Exception:
            continue

        current_week = None
        week_totals  = []
        for row in rows:
            if row and str(row[0]).startswith("Semana"):
                current_week = str(row[0]).replace("Semana ", "").strip()
            if len(row) > 1 and str(row[1]) == "TOTAL" and current_week:
                def _f(r, i):
                    try: return float(r[i]) if len(r) > i and r[i] != "" else 0.0
                    except: return 0.0
                week_totals.append({
                    "week": current_week,
                    "spend": _f(row, si),
                    "cpm":   _f(row, cpmi),
                    "ctr":   _f(row, ctri),
                    "cpc":   _f(row, cpci),
                    "conv":  int(_f(row, convi)),
                    "cpa":   _f(row, cpai),
                })

        if week_totals:
            lines.append(f"\n=== {tab} — Tendencia histórica (semanas previas) ===")
            lines.append(f"  {'Semana':<25} {'Gasto':>8} {'CPM':>7} {'CTR':>7} {'CPC':>7} {label:>7} {'Conv':>6}")
            for wt in week_totals[-6:]:
                lines.append(
                    f"  {wt['week']:<25} {wt['spend']:>7.2f}€ {wt['cpm']:>6.2f}€ "
                    f"{wt['ctr']:>6.2f}% {wt['cpc']:>6.2f}€ {wt['cpa']:>6.2f}€ {wt['conv']:>5}"
                )
    return "\n".join(lines)


# ── Doc acumulativo — gestión de secciones semanales ─────────────────────────
def find_and_delete_week(service, doc_id: str, week_label: str) -> bool:
    """Busca la sección de la semana en el Doc y la borra. Devuelve True si existía."""
    doc  = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])

    heading_text  = f"SEMANA {week_label}"
    section_start = None
    section_end   = None

    for elem in body:
        if "paragraph" not in elem:
            continue
        style = elem["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        text  = "".join(
            e.get("textRun", {}).get("content", "")
            for e in elem["paragraph"].get("elements", [])
        ).strip()

        if style == "HEADING_1" and heading_text in text:
            section_start = elem["startIndex"]
        elif section_start is not None and style == "HEADING_1":
            section_end = elem["startIndex"]
            break

    if section_start is None:
        return False

    if section_end is None:
        section_end = max(body[-1].get("endIndex", section_start + 2) - 1, section_start + 1)

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"deleteContentRange": {
            "range": {"startIndex": section_start, "endIndex": section_end}
        }}]}
    ).execute()
    return True


# ── Email de entrega ──────────────────────────────────────────────────────────
def send_report_email(analysis: dict, dates: dict, doc_url: str, sheet_url: str) -> None:
    creds   = get_google_credentials()
    service = build("gmail", "v1", credentials=creds)

    wk         = dates["week"]
    week_label = f"{wk[0].strftime('%d/%m')} - {wk[1].strftime('%d/%m/%Y')}"
    meta_res   = analysis.get("meta",   {}).get("resumen", "—")
    goog_res   = analysis.get("google", {}).get("resumen", "—")

    body = (
        f"Informe Semanal Becier — Semana {week_label}\n\n"
        f"META ADS\n{meta_res}\n\n"
        f"GOOGLE ADS\n{goog_res}\n\n"
        f"{'─'*60}\n"
        f"• Análisis completo: {doc_url}\n"
        f"• Datos detallados:  {sheet_url}\n\n"
        f"Generado automáticamente el {date.today().strftime('%d/%m/%Y')}."
    )
    msg              = MIMEText(body, "plain", "utf-8")
    msg["to"]        = "jordi@rocketgrowthlab.com"
    msg["subject"]   = f"Informe Semanal Becier — {week_label}"
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("  Email enviado a jordi@rocketgrowthlab.com")


# ── Construcción del informe ──────────────────────────────────────────────────
def build_report(meta_wk_raw, meta_pw_raw, meta_mo_raw, meta_pm_raw,
                 goog_wk, goog_pw, goog_mo, goog_pm,
                 analysis: dict, dates: dict,
                 week_context: str = "") -> None:

    wk = dates["week"]
    fmt_d = lambda d: d.strftime("%d/%m/%Y")
    fmt_s = lambda d: d.strftime("%d/%m")
    week_label = f"{fmt_s(wk[0])} - {fmt_d(wk[1])}"

    doc_url   = f"https://docs.google.com/document/d/{DOC_ID}/edit"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

    # ── Google Sheets — tablas de datos ───────────────────────────────────────
    print("  Escribiendo en Google Sheets...")
    sheets_svc = get_sheets_service()
    write_meta_to_sheet(sheets_svc, meta_wk_raw, meta_pw_raw, dates)
    write_google_to_sheet(sheets_svc, goog_wk, goog_pw, dates)

    # ── Google Docs — informe acumulativo ─────────────────────────────────────
    print("  Actualizando Google Docs...")
    docs_svc = get_docs_service()

    week_existed = find_and_delete_week(docs_svc, DOC_ID, week_label)
    if week_existed:
        print(f"  Semana {week_label} ya existía — sección reemplazada.")

    # Cabecera de sección: HEADING_1 "SEMANA X" para navegación en outline
    meta_analysis   = analysis.get("meta", {})
    google_analysis = analysis.get("google", {})

    append_text(docs_svc, DOC_ID,
        f"# SEMANA {week_label}\n"
        f"### Generado el {date.today().strftime('%d/%m/%Y')}  ·  "
        f"{'Contexto: ' + week_context + '  ·  ' if week_context else ''}"
        f"Datos: {sheet_url}\n")

    # ── META ADS ──────────────────────────────────────────────────────────────
    append_text(docs_svc, DOC_ID, "\n## META ADS\n")
    meta_summaries = meta_analysis.get("campaign_summaries", [])
    if meta_summaries:
        append_text(docs_svc, DOC_ID, "\n".join(meta_summaries) + "\n")
    meta_flat_rows, meta_cell_colors = meta_campaign_paired_rows(meta_wk_raw, meta_pw_raw)
    insert_paired_table(docs_svc, DOC_ID, META_DOC_HEADERS, meta_flat_rows, meta_cell_colors)

    if meta_analysis.get("conclusiones"):
        append_text(docs_svc, DOC_ID,
            "\n### Conclusiones\n" + "\n".join(meta_analysis["conclusiones"]) + "\n")
    if meta_analysis.get("next_steps"):
        append_text(docs_svc, DOC_ID,
            "\n### Próximos pasos\n" + "\n".join(meta_analysis["next_steps"]) + "\n")

    # ── GOOGLE ADS ────────────────────────────────────────────────────────────
    append_text(docs_svc, DOC_ID, "\n## GOOGLE ADS\n")
    goog_summaries = google_analysis.get("campaign_summaries", [])
    if goog_summaries:
        append_text(docs_svc, DOC_ID, "\n".join(goog_summaries) + "\n")
    goog_flat_rows, goog_cell_colors = google_doc_paired_rows(goog_wk, goog_pw)
    insert_paired_table(docs_svc, DOC_ID, GOOGLE_DOC_HEADERS, goog_flat_rows, goog_cell_colors)

    if google_analysis.get("conclusiones"):
        append_text(docs_svc, DOC_ID,
            "\n### Conclusiones\n" + "\n".join(google_analysis["conclusiones"]) + "\n")
    if google_analysis.get("next_steps"):
        append_text(docs_svc, DOC_ID,
            "\n### Próximos pasos\n" + "\n".join(google_analysis["next_steps"]) + "\n")

    print(f"  Doc: {doc_url}")
    print(f"  Sheet: {sheet_url}")

    # ── Email (solo en primera entrega, no en correcciones) ───────────────────
    if not week_existed:
        print("  Enviando email...")
        try:
            send_report_email(analysis, dates, doc_url, sheet_url)
        except Exception as e:
            print(f"  AVISO email: {e}")
    else:
        print("  Semana ya existía — email omitido (corrección).")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Contexto de la semana (solo si se ejecuta en terminal interactivo)
    week_context = ""
    if sys.stdin.isatty():
        print("\n¿Contexto relevante esta semana? (promociones, cambios de presupuesto, incidencias...)")
        print("Pulsa Enter para omitir.")
        week_context = input("  > ").strip()

    print("\nCalculando fechas...")
    dates = calculate_dates()
    wk, pw, mo, pm = dates["week"], dates["prev_week"], dates["month"], dates["prev_month"]
    fmt = lambda d: d.strftime("%Y-%m-%d")

    print(f"  Semana actual  : {fmt(wk[0])} - {fmt(wk[1])}")
    print(f"  Semana anterior: {fmt(pw[0])} - {fmt(pw[1])}")
    print(f"  Mes actual     : {fmt(mo[0])} - {fmt(mo[1])}")
    print(f"  Mes anterior   : {fmt(pm[0])} - {fmt(pm[1])}")

    print("\nObteniendo datos Meta Ads...")
    meta_wk_raw = [c for c in get_campaigns_insights_range(META_ACCOUNT, fmt(wk[0]), fmt(wk[1])).get("campaigns", []) if c.get("spend_eur", 0) > 0.01]
    meta_pw_raw = get_campaigns_insights_range(META_ACCOUNT, fmt(pw[0]), fmt(pw[1])).get("campaigns", [])
    meta_mo_raw = [c for c in get_campaigns_insights_range(META_ACCOUNT, fmt(mo[0]), fmt(mo[1])).get("campaigns", []) if c.get("spend_eur", 0) > 0.01]
    meta_pm_raw = get_campaigns_insights_range(META_ACCOUNT, fmt(pm[0]), fmt(pm[1])).get("campaigns", [])
    print(f"  Meta: {len(meta_wk_raw)} campañas activas en semana actual")

    print("\nObteniendo datos Google Ads...")
    goog_wk = {k: v for k, v in aggregate_google(get_campaigns_stats_range(fmt(wk[0]), fmt(wk[1]), GOOGLE_ACCOUNT).get("campaigns", [])).items() if v.get("spend", 0) > 0.01}
    goog_pw = aggregate_google(get_campaigns_stats_range(fmt(pw[0]), fmt(pw[1]), GOOGLE_ACCOUNT).get("campaigns", []))
    goog_mo = {k: v for k, v in aggregate_google(get_campaigns_stats_range(fmt(mo[0]), fmt(mo[1]), GOOGLE_ACCOUNT).get("campaigns", [])).items() if v.get("spend", 0) > 0.01}
    goog_pm = aggregate_google(get_campaigns_stats_range(fmt(pm[0]), fmt(pm[1]), GOOGLE_ACCOUNT).get("campaigns", []))
    print(f"  Google: {len(goog_wk)} líneas activas en semana actual")

    print("\nLeyendo histórico de semanas previas...")
    sheets_svc = get_sheets_service()
    historical = get_historical_summary(sheets_svc)
    if historical:
        print("  Histórico encontrado, se incluirá en el análisis.")

    print("\nGenerando análisis con Claude...")
    analysis = generate_analysis(
        meta_wk_raw, meta_pw_raw, meta_mo_raw, meta_pm_raw,
        goog_wk, goog_pw, goog_mo, goog_pm, dates,
        week_context=week_context,
        historical=historical,
    )

    print("\nGenerando informe...")
    build_report(meta_wk_raw, meta_pw_raw, meta_mo_raw, meta_pm_raw,
                 goog_wk, goog_pw, goog_mo, goog_pm, analysis, dates,
                 week_context=week_context)


if __name__ == "__main__":
    main()
