# -*- coding: utf-8 -*-
"""
Dashboard de Rendimiento — DCORE
Meta Ads + Google Ads | Streamlit

Diferencias respecto a dashboard_becier.py (ver historial de conversación / clients/dcore.md):
- DCORE es un único negocio (reformas de lujo), no un grupo con sub-marcas: no hay
  filtro de "Vertical" ni funnel de CRM (Becier tiene un Sheet propio de ventas que
  DCORE no tiene). En su lugar se usa "Tema" (tools/dcore_naming.py) para agrupar
  campañas por ángulo comercial.
- Bloque nuevo: desglose por creatividad con miniatura + Ángulo/Landing/Hook (parseado
  de la convención de nombre propuesta a Vero, directora de marketing).
- Bloque nuevo: zona geográfica de leads (código postal, solo disponible en Meta Lead
  Ads) con clasificación Dentro M-30 / Fuera M-30 pero Comunidad de Madrid / Fuera CM.
- Bloque nuevo: rendimiento de landing pages de Google Ads (recurso landing_page_view).
- Disclaimers permanentes sobre el estado provisional del tracking (ver clients/dcore.md).
"""
import os
import re
import sys
import json
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import requests

from tools.sheets_tools import fetch_dcore_leads, fetch_dcore_known_landings
from tools.dcore_naming import (
    classify_tema, is_post_boost, TEMA_STYLES, parse_creative_name, KNOWN_LANDINGS, TEMA_DEFAULT,
)
from tools.madrid_postal import classify_postal_code, postal_coords, ZONE_COLOR
from tools.ga4_tools import fetch_ga4_landing_metrics, fetch_ga4_form_funnel
from tools.clarity_tools import get_cached_snapshot, refresh_snapshot, get_quota_status, DAILY_QUOTA

# ─── COMPONENTE: tabla de campañas Meta con clic para filtrar ────────────────
_clickable_meta_table = components.declare_component(
    "clickable_meta_table_dcore",
    path=str(Path(__file__).parent / "components" / "clickable_table"),
)

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DCORE · Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CREDENTIALS SETUP ───────────────────────────────────────────────────────
def _setup_credentials():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    try:
        secrets = st.secrets
        for key, val in secrets.items():
            if isinstance(val, str):
                os.environ.setdefault(key, val)
        tmp = Path("/tmp")
        if "GOOGLE_TOKEN_JSON" in secrets:
            (tmp / "token.json").write_text(secrets["GOOGLE_TOKEN_JSON"])
        if "GOOGLE_CLIENT_SECRET_JSON" in secrets:
            (tmp / "client_secret.json").write_text(secrets["GOOGLE_CLIENT_SECRET_JSON"])
    except Exception:
        pass

_setup_credentials()
sys.path.insert(0, str(Path(__file__).parent))

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #0d0f18; }
[data-testid="stHeader"] { background-color: #0d0f18; border-bottom: 1px solid #1a1e35; }
section[data-testid="stSidebar"] { background-color: #0b0d16; border-right: 1px solid #1a1e35; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

.kpi-card {
    background: #12152a; border: 1px solid #1e2440; border-radius: 10px;
    padding: 16px 18px 14px; margin-bottom: 10px; min-height: 112px;
    box-sizing: border-box; transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2e3560; }
.kpi-icon { font-size: 16px; margin-bottom: 6px; display: block; }
.kpi-label { color: #5a6080; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.9px; margin-bottom: 6px; }
.kpi-value { color: #eef0ff; font-size: 24px; font-weight: 800; line-height: 1; letter-spacing: -0.5px; }
.kpi-sub { color: #444c70; font-size: 10.5px; margin-top: 5px; }
.kpi-delta { font-size: 10.5px; margin-top: 6px; font-weight: 700; }
.kpi-delta-value { color: #8894c0; font-weight: 700; }
.kpi-delta-label { color: #444c70; font-weight: 500; margin-left: 3px; }

.platform-header { display: flex; align-items: center; gap: 10px; padding: 10px 16px; border-radius: 8px; margin-bottom: 14px; }
.ph-meta { background: rgba(74,127,255,0.08); border: 1px solid rgba(74,127,255,0.2); }
.ph-google { background: rgba(52,168,83,0.08); border: 1px solid rgba(52,168,83,0.2); }
.ph-combined { background: rgba(201,169,110,0.10); border: 1px solid rgba(201,169,110,0.28); }
.ph-icon { font-size: 18px; }
.ph-title { font-size: 13px; font-weight: 700; letter-spacing: 0.3px; }
.ph-meta .ph-title { color: #6a9fff; }
.ph-google .ph-title { color: #4fc870; }
.ph-combined .ph-title { color: #c9a96e; }
.ph-sub { font-size: 11px; color: #444c70; margin-left: auto; }

.disclaimer-strip { display:flex; flex-direction:column; gap:8px; margin: 14px 0 20px; }
.disclaimer {
    display:flex; align-items:flex-start; gap:10px; padding: 10px 16px; border-radius: 8px;
    font-size: 12.5px; line-height:1.5; background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.28); color: #d8c483;
}
.disclaimer b { color: #fbbf24; }

.alert-strip { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 20px; }
.alert-badge { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 600; }
.alert-warn { background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.3); color: #fbbf24; }
.alert-danger { background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.3); color: #f87171; }
.alert-ok { background: rgba(52,168,83,0.12); border: 1px solid rgba(52,168,83,0.3); color: #4fc870; }

.dash-header {
    background: linear-gradient(135deg, #141414 0%, #0d0f18 100%);
    border: 1px solid #2a2418; border-radius: 14px; padding: 22px 28px; margin-bottom: 18px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.dash-period { background: #1a1e35; border: 1px solid #252a48; border-radius: 8px; padding: 12px 20px; color: #6a7aaa; font-size: 14px; font-weight: 600; white-space: nowrap; }

.cmp-delta { font-weight: 700; font-size: 11px; }
.cmp-up { color: #4fc870; } .cmp-down { color: #f87171; } .cmp-flat { color: #5a6080; }

.divider { border: none; border-top: 1px solid #1a1e35; margin: 22px 0; }

.styled-table-wrap { overflow-x: auto; border-radius: 8px; border: 1px solid #1e2440; }
.tag { display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.4px; white-space: nowrap; }
.tag-b2b          { background: rgba(74,127,255,0.15); color: #6a9fff; }
.tag-cocinas      { background: rgba(251,191,36,0.15); color: #fbbf24; }
.tag-living       { background: rgba(192,132,252,0.15);color: #c084fc; }
.tag-evo          { background: rgba(20,184,166,0.15); color: #2dd4bf; }
.tag-reformas     { background: rgba(201,169,110,0.18);color: #c9a96e; }
.tag-other        { background: rgba(100,100,100,0.15);color: #888; }
.tag-m30          { background: rgba(79,200,112,0.15); color: #4fc870; }
.tag-cm           { background: rgba(251,191,36,0.15); color: #fbbf24; }
.tag-fuera        { background: rgba(248,113,113,0.15);color: #f87171; }

[data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1e2440; gap: 0; }
[data-baseweb="tab"] { color: #444c70 !important; font-weight: 600 !important; font-size: 13px !important; padding: 10px 20px !important; }
[aria-selected="true"] { color: #eef0ff !important; border-bottom: 2px solid #c9a96e !important; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS DE FECHA ─────────────────────────────────────────────────────────
def _period_last_month():
    today = date.today()
    first_current = today.replace(day=1)
    last_prev = first_current - timedelta(days=1)
    return str(last_prev.replace(day=1)), str(last_prev)

def _period_this_month():
    today = date.today()
    return str(today.replace(day=1)), str(today)

def _period_last_n(days: int):
    today = date.today()
    return str(today - timedelta(days=days)), str(today)

def get_prev_month_range():
    return _period_last_month()

import calendar

def _shift_months(d: date, n: int) -> date:
    month_idx = d.month - 1 + n
    year = d.year + month_idx // 12
    month = month_idx % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

COMPARISON_OPTIONS = ["Sin comparación", "Período anterior", "Mes anterior", "Trimestre anterior", "Año anterior"]

def compute_comparison_range(since_str: str, until_str: str, mode: str):
    if mode not in COMPARISON_OPTIONS or mode == "Sin comparación":
        return None, None
    since = date.fromisoformat(since_str)
    until = date.fromisoformat(until_str)
    if mode == "Período anterior":
        days = (until - since).days + 1
        comp_until = since - timedelta(days=1)
        comp_since = comp_until - timedelta(days=days - 1)
    elif mode == "Mes anterior":
        comp_since = _shift_months(since, -1); comp_until = _shift_months(until, -1)
    elif mode == "Trimestre anterior":
        comp_since = _shift_months(since, -3); comp_until = _shift_months(until, -3)
    elif mode == "Año anterior":
        comp_since = _shift_months(since, -12); comp_until = _shift_months(until, -12)
    else:
        return None, None
    return str(comp_since), str(comp_until)

def fmt_date_ddmmyyyy(iso_str: str) -> str:
    try:
        return date.fromisoformat(iso_str).strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return iso_str

# ─── META ADS FETCH ───────────────────────────────────────────────────────────
META_BASE = "https://graph.facebook.com/v21.0"
GOOGLE_CUSTOMER_ID = "1829150362"  # DCORE Group, sin guiones (182-915-0362)

def _meta_account_id() -> str:
    aid = os.environ.get("META_AD_ACCOUNT_ID_DCORE", "")
    return aid if aid.startswith("act_") else f"act_{aid}"

def _meta_token() -> str:
    return os.environ.get("META_ACCESS_TOKEN_DCORE", "")

_OPT_GOAL_TO_ACTION = {
    "LINK_CLICKS": "link_click", "CLICKS": "link_click",
    "LANDING_PAGE_VIEWS": "landing_page_view",
    "LEAD_GENERATION": "lead", "QUALITY_LEAD": "lead",
    "REACH": None, "IMPRESSIONS": None,
    "OFFSITE_CONVERSIONS": "__pixel__",
}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_adset_goals() -> dict:
    params = {
        "access_token": _meta_token(),
        "fields": "id,campaign_id,optimization_goal,promoted_object",
        "limit": 500,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/adsets", params=params, timeout=20)
        data = r.json()
        goals = {}
        for adset in data.get("data", []):
            aid = adset.get("id"); cid = adset.get("campaign_id")
            goal = adset.get("optimization_goal", "")
            promoted = adset.get("promoted_object") or {}
            event_type = promoted.get("custom_event_type", "")
            entry = {"goal": goal, "event": event_type}
            if aid: goals[aid] = entry
            if cid: goals.setdefault(cid, entry)
        return goals
    except Exception:
        return {}

_EVENT_TO_ACTION = {
    "LEAD": "offsite_conversion.fb_pixel_lead",
    "COMPLETE_REGISTRATION": "offsite_conversion.fb_pixel_complete_registration",
}
_ACTION_LABELS = {
    "link_click": "Clics enlace", "landing_page_view": "Visitas landing",
    "offsite_conversion.fb_pixel_lead": "Leads", "lead": "Leads",
    "onsite_conversion.lead_grouped": "Leads (formulario)",
}

def _result_from_actions(actions: dict, goal_info: dict, reach: int, impressions: int):
    goal = goal_info.get("goal", ""); event = goal_info.get("event", "")
    if goal == "REACH": return reach, "Alcance"
    if goal == "IMPRESSIONS": return impressions, "Impresiones"
    if goal in ("LEAD_GENERATION", "QUALITY_LEAD"):
        for key in ("lead", "onsite_conversion.lead_grouped", "onsite_conversion.lead"):
            if actions.get(key, 0) > 0:
                return int(actions[key]), _ACTION_LABELS.get(key, "Leads")
        return 0, "Leads"
    if goal == "OFFSITE_CONVERSIONS":
        action_key = _EVENT_TO_ACTION.get(event)
        if action_key:
            return int(actions.get(action_key, 0)), _ACTION_LABELS.get(action_key, "Conversión")
        pixel = {k: v for k, v in actions.items() if k.startswith("offsite_conversion.fb_pixel") and v > 0}
        if pixel:
            best = max(pixel, key=pixel.get)
            return int(pixel[best]), _ACTION_LABELS.get(best, "Conversión")
        return 0, "Conversión"
    action_key = _OPT_GOAL_TO_ACTION.get(goal)
    if not action_key or action_key == "__pixel__":
        return 0, "—"
    return int(actions.get(action_key, 0)), _ACTION_LABELS.get(action_key, "Resultados")

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_campaigns(since: str, until: str) -> list:
    params = {
        "access_token": _meta_token(),
        "fields": "campaign_id,campaign_name,spend,impressions,reach,cpm,cost_per_inline_link_click,"
                  "inline_link_click_ctr,inline_link_clicks,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "campaign", "limit": 300,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        if "error" in data:
            return []
        adset_goals = fetch_meta_adset_goals()
        campaigns = []
        for i in data.get("data", []):
            actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
            spend = float(i.get("spend", 0))
            name = i.get("campaign_name", "")
            cid = i.get("campaign_id", "")
            goal_info = adset_goals.get(cid, {"goal": "", "event": ""})
            result_val, result_key = _result_from_actions(
                actions, goal_info, reach=int(i.get("reach", 0)), impressions=int(i.get("impressions", 0)))
            campaigns.append({
                "_campaign_id": cid, "Campaña": name,
                "Tema": "Impulso publicaciones" if is_post_boost(name) else classify_tema(name),
                "Es boost": is_post_boost(name),
                "Gasto (€)": spend, "Impresiones": int(i.get("impressions", 0)),
                "Alcance": int(i.get("reach", 0)), "CPM": float(i.get("cpm", 0)),
                "CTR (%)": float(i.get("inline_link_click_ctr", 0)),
                "Clics enlace": int(i.get("inline_link_clicks", 0)),
                "CPC": float(i.get("cost_per_inline_link_click", 0) or 0),
                "Frecuencia": float(i.get("frequency", 0)),
                "Resultado": int(result_val), "Resultado Key": result_key,
                "Coste/Resultado": round(spend / result_val, 2) if result_val > 0 else None,
            })
        campaigns.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return campaigns
    except Exception:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_daily(since: str, until: str) -> list:
    """Gasto y leads por día (a nivel de campaña, para poder aplicar la detección de
    objetivo por campaña vía adset_goals) — usado por el gráfico de inversión mensual
    y por la evolución semanal de CPL. Excluye impulso de publicaciones."""
    params = {
        "access_token": _meta_token(),
        "fields": "campaign_id,campaign_name,spend,reach,impressions,actions,date_start",
        "time_range": json.dumps({"since": since, "until": until}),
        "time_increment": 1, "level": "campaign", "limit": 500,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        if "error" in data:
            return []
        adset_goals = fetch_meta_adset_goals()
        by_day: dict[str, dict] = {}
        for i in data.get("data", []):
            name = i.get("campaign_name", "")
            if is_post_boost(name):
                continue
            d = i["date_start"]
            cid = i.get("campaign_id", "")
            goal_info = adset_goals.get(cid, {"goal": "", "event": ""})
            actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
            result_val, _ = _result_from_actions(
                actions, goal_info, reach=int(i.get("reach", 0)), impressions=int(i.get("impressions", 0)))
            entry = by_day.setdefault(d, {"spend": 0.0, "leads": 0})
            entry["spend"] += float(i.get("spend", 0))
            entry["leads"] += int(result_val)
        return [{"date": d, "spend": round(v["spend"], 2), "leads": v["leads"]} for d, v in sorted(by_day.items())]
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_device_breakdown(since: str, until: str) -> list:
    """Gasto/impresiones/leads por dispositivo (mobile_app + mobile_web se agrupan en
    'Móvil'). Requiere resolver el objetivo por campaña igual que fetch_meta_campaigns
    para que 'Leads' no mezcle campañas que optimizan a cosas distintas."""
    params = {
        "access_token": _meta_token(),
        "fields": "campaign_id,campaign_name,spend,reach,impressions,actions",
        "breakdowns": "device_platform",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "campaign", "limit": 500,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        if "error" in data:
            return []
        adset_goals = fetch_meta_adset_goals()
        DEVICE_LABEL = {"mobile_app": "Móvil", "mobile_web": "Móvil", "desktop": "Desktop"}
        agg: dict[str, dict] = {}
        for i in data.get("data", []):
            name = i.get("campaign_name", "")
            if is_post_boost(name):
                continue
            cid = i.get("campaign_id", "")
            goal_info = adset_goals.get(cid, {"goal": "", "event": ""})
            actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
            spend = float(i.get("spend", 0))
            impressions = int(i.get("impressions", 0))
            result_val, _ = _result_from_actions(
                actions, goal_info, reach=int(i.get("reach", 0)), impressions=impressions)
            device = DEVICE_LABEL.get(i.get("device_platform", ""), "Otros")
            entry = agg.setdefault(device, {"spend": 0.0, "impressions": 0, "leads": 0})
            entry["spend"] += spend; entry["impressions"] += impressions; entry["leads"] += int(result_val)
        rows = []
        for device, v in agg.items():
            rows.append({
                "Dispositivo": device, "Gasto (€)": round(v["spend"], 2), "Impresiones": v["impressions"],
                "Leads": v["leads"], "CPL": round(v["spend"] / v["leads"], 2) if v["leads"] else None,
            })
        rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return rows
    except Exception:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_adsets_detail(since: str, until: str) -> list:
    params = {
        "access_token": _meta_token(),
        "fields": "adset_id,adset_name,campaign_id,campaign_name,spend,impressions,reach,"
                  "cpm,cost_per_inline_link_click,inline_link_click_ctr,inline_link_clicks,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "adset", "limit": 500,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        if "error" in data:
            return []
        adset_goals = fetch_meta_adset_goals()
        rows = []
        for i in data.get("data", []):
            actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
            spend = float(i.get("spend", 0))
            aid = i.get("adset_id", ""); cid = i.get("campaign_id", "")
            name = i.get("campaign_name", "")
            goal_info = adset_goals.get(aid) or adset_goals.get(cid, {"goal": "", "event": ""})
            result_val, result_key = _result_from_actions(
                actions, goal_info, reach=int(i.get("reach", 0)), impressions=int(i.get("impressions", 0)))
            rows.append({
                "_adset_id": aid, "Campaña": name, "Adset": i.get("adset_name", ""),
                "Tema": "Impulso publicaciones" if is_post_boost(name) else classify_tema(name),
                "Gasto (€)": spend, "Impresiones": int(i.get("impressions", 0)),
                "Alcance": int(i.get("reach", 0)), "CPM": float(i.get("cpm", 0)),
                "CPC": float(i.get("cost_per_inline_link_click", 0) or 0),
                "CTR (%)": float(i.get("inline_link_click_ctr", 0)),
                "Clics enlace": int(i.get("inline_link_clicks", 0)),
                "Frecuencia": float(i.get("frequency", 0)),
                "Resultado": int(result_val), "Resultado Key": result_key,
                "Coste/Resultado": round(spend / result_val, 2) if result_val > 0 else None,
            })
        rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return rows
    except Exception:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_ads_for_adset(adset_id: str, since: str, until: str) -> list:
    token = _meta_token()
    ins_params = {
        "access_token": token,
        "fields": "ad_id,ad_name,spend,impressions,reach,cpm,cost_per_inline_link_click,"
                  "inline_link_click_ctr,inline_link_clicks,frequency,actions,"
                  "video_play_actions,video_thruplay_watched_actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "ad",
        "filtering": json.dumps([{"field": "adset.id", "operator": "EQUAL", "value": adset_id}]),
        "limit": 200,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=ins_params, timeout=20)
        insights_raw = r.json().get("data", [])
    except Exception:
        return []
    if not insights_raw:
        return []
    ins_map = {}
    for i in insights_raw:
        actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
        video_plays = sum(float(a["value"]) for a in i.get("video_play_actions", []))
        thruplays = sum(float(a["value"]) for a in i.get("video_thruplay_watched_actions", []))
        ins_map[i["ad_id"]] = {
            "spend": float(i.get("spend", 0)), "impressions": int(i.get("impressions", 0)),
            "reach": int(i.get("reach", 0)), "cpm": float(i.get("cpm", 0)),
            "cpc": float(i.get("cost_per_inline_link_click", 0) or 0),
            "ctr": float(i.get("inline_link_click_ctr", 0)),
            "clics": int(i.get("inline_link_clicks", 0)),
            "frequency": float(i.get("frequency", 0)), "actions": actions,
            "video_plays": video_plays, "thruplays": thruplays,
        }
    ads_params = {
        "access_token": token,
        "fields": "id,name,effective_status,creative{id,name,image_url,thumbnail_url,video_id,object_type,image_hash}",
        "limit": 200,
    }
    try:
        r2 = requests.get(f"{META_BASE}/{adset_id}/ads", params=ads_params, timeout=20)
        ads_raw = r2.json().get("data", [])
    except Exception:
        ads_raw = []
    adset_goals = fetch_meta_adset_goals()
    goal_info = adset_goals.get(adset_id, {"goal": "", "event": ""})
    rows = []
    for ad in ads_raw:
        aid = ad.get("id", "")
        metrics = ins_map.get(aid, {})
        if not metrics:
            continue
        creative = ad.get("creative") or {}
        img_url = creative.get("image_url", ""); thumb_url = creative.get("thumbnail_url", "")
        obj_type = creative.get("object_type", "")
        is_video = bool(creative.get("video_id")) or obj_type in ("VIDEO", "SHARE")
        preview_url = thumb_url if is_video else img_url
        result_val, _ = _result_from_actions(
            metrics.get("actions", {}), goal_info, reach=metrics.get("reach", 0), impressions=metrics.get("impressions", 0))
        spend = metrics.get("spend", 0)
        ad_name = ad.get("name", "")
        parsed = parse_creative_name(ad_name)
        impressions = metrics.get("impressions", 0)
        video_plays = metrics.get("video_plays", 0)
        thruplays = metrics.get("thruplays", 0)
        hook_rate = round(video_plays / impressions * 100, 2) if (is_video and impressions) else None
        hold_rate = round(thruplays / video_plays * 100, 2) if (is_video and video_plays) else None
        rows.append({
            "ad_id": aid, "Anuncio": ad_name, "Estado": ad.get("effective_status", ""),
            "preview_url": preview_url, "is_video": is_video,
            "Ángulo": parsed["angulo"], "Landing": parsed["landing"], "Hook": parsed["hook"], "Formato": parsed["formato"],
            "Gasto (€)": spend, "Impresiones": impressions,
            "Alcance": metrics.get("reach", 0), "CPM": metrics.get("cpm", 0), "CPC": metrics.get("cpc", 0),
            "CTR (%)": metrics.get("ctr", 0), "Clics": metrics.get("clics", 0),
            "Frecuencia": metrics.get("frequency", 0), "Resultado": int(result_val),
            "CPR": round(spend / result_val, 2) if result_val > 0 else None,
            "Hook Rate (%)": hook_rate, "Hold Rate (%)": hold_rate,
        })
    rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
    return rows


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_ads_all(since: str, until: str) -> list:
    """Todas las creatividades de campañas estructuradas (no boost) en el período,
    para la pestaña 'Todas las creatividades' — sin necesidad de navegar campaña a campaña."""
    token = _meta_token()
    ins_params = {
        "access_token": token,
        "fields": "ad_id,ad_name,adset_id,adset_name,campaign_id,campaign_name,spend,impressions,reach,"
                  "cpm,cost_per_inline_link_click,inline_link_click_ctr,inline_link_clicks,frequency,actions,"
                  "video_play_actions,video_thruplay_watched_actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "ad", "limit": 500,
    }
    insights_raw = []
    url = f"{META_BASE}/{_meta_account_id()}/insights"
    params = ins_params
    for _ in range(10):  # tope de seguridad: 10 páginas × 500 = 5.000 anuncios
        try:
            r = requests.get(url, params=params, timeout=20)
            data = r.json()
        except Exception:
            break
        if "error" in data:
            break
        insights_raw.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")
        if not next_url:
            break
        url, params = next_url, None
    if not insights_raw:
        return []

    adset_goals = fetch_meta_adset_goals()
    ins_by_ad = {}
    ad_ids_to_lookup = []
    for i in insights_raw:
        campaign_name = i.get("campaign_name", "")
        if is_post_boost(campaign_name):
            continue  # el ruido de impulso de publicaciones queda fuera de esta pestaña
        aid = i.get("ad_id", "")
        actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
        adset_id = i.get("adset_id", ""); cid = i.get("campaign_id", "")
        goal_info = adset_goals.get(adset_id) or adset_goals.get(cid, {"goal": "", "event": ""})
        result_val, _ = _result_from_actions(
            actions, goal_info, reach=int(i.get("reach", 0)), impressions=int(i.get("impressions", 0)))
        spend = float(i.get("spend", 0))
        video_plays = sum(float(a["value"]) for a in i.get("video_play_actions", []))
        thruplays = sum(float(a["value"]) for a in i.get("video_thruplay_watched_actions", []))
        ins_by_ad[aid] = {
            "Campaña": campaign_name, "Tema": classify_tema(campaign_name),
            "Adset": i.get("adset_name", ""), "Anuncio": i.get("ad_name", ""),
            "Gasto (€)": spend, "Impresiones": int(i.get("impressions", 0)),
            "Alcance": int(i.get("reach", 0)), "CPM": float(i.get("cpm", 0)),
            "CPC": float(i.get("cost_per_inline_link_click", 0) or 0),
            "CTR (%)": float(i.get("inline_link_click_ctr", 0)),
            "Clics": int(i.get("inline_link_clicks", 0)),
            "Frecuencia": float(i.get("frequency", 0)), "Resultado": int(result_val),
            "CPR": round(spend / result_val, 2) if result_val > 0 else None,
            "_video_plays": video_plays, "_thruplays": thruplays,
        }
        ad_ids_to_lookup.append(aid)

    if not ad_ids_to_lookup:
        return []

    # Creatives (miniatura) — se piden en lotes de 50 ids para no exceder límites de URL
    creative_by_ad = {}
    for i in range(0, len(ad_ids_to_lookup), 50):
        chunk = ad_ids_to_lookup[i:i + 50]
        ads_params = {
            "access_token": token,
            "fields": "id,name,effective_status,creative{id,video_id,object_type,image_url,thumbnail_url}",
            "filtering": json.dumps([{"field": "ad.id", "operator": "IN", "value": chunk}]),
            "limit": 50,
        }
        try:
            r2 = requests.get(f"{META_BASE}/{_meta_account_id()}/ads", params=ads_params, timeout=20)
            for ad in r2.json().get("data", []):
                creative_by_ad[ad.get("id", "")] = ad
        except Exception:
            continue

    rows = []
    for aid, base in ins_by_ad.items():
        ad_meta = creative_by_ad.get(aid, {})
        creative = ad_meta.get("creative") or {}
        img_url = creative.get("image_url", ""); thumb_url = creative.get("thumbnail_url", "")
        obj_type = creative.get("object_type", "")
        is_video = bool(creative.get("video_id")) or obj_type in ("VIDEO", "SHARE")
        parsed = parse_creative_name(base["Anuncio"])
        video_plays = base["_video_plays"]
        thruplays = base["_thruplays"]
        hook_rate = round(video_plays / base["Impresiones"] * 100, 2) if (is_video and base["Impresiones"]) else None
        hold_rate = round(thruplays / video_plays * 100, 2) if (is_video and video_plays) else None
        rows.append({
            **base,
            "Estado": ad_meta.get("effective_status", "—"),
            "preview_url": thumb_url if is_video else img_url, "is_video": is_video,
            "Ángulo": parsed["angulo"], "Landing": parsed["landing"], "Hook": parsed["hook"], "Formato": parsed["formato"],
            "Hook Rate (%)": hook_rate, "Hold Rate (%)": hold_rate,
        })
    rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
    return rows


# ─── GOOGLE ADS FETCH ─────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_campaigns(since: str, until: str) -> dict:
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT campaign.id, campaign.name, campaign.status,
                   metrics.impressions, metrics.clicks, metrics.cost_micros,
                   metrics.conversions, metrics.ctr, metrics.average_cpc, metrics.average_cpm,
                   metrics.search_impression_share, metrics.search_rank_lost_impression_share,
                   metrics.search_budget_lost_impression_share
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
              AND metrics.impressions > 0
            ORDER BY metrics.cost_micros DESC
        """
        response = ga_service.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)

        def pct(v):
            return f"{v*100:.1f}%" if v and v > 0 else "—"

        campaigns = []
        for row in response:
            cost = round(row.metrics.cost_micros / 1_000_000, 2)
            conv = round(row.metrics.conversions, 1)
            clics = row.metrics.clicks
            campaigns.append({
                "Campaña": row.campaign.name, "Tema": classify_tema(row.campaign.name),
                "Gasto (€)": cost,
                "Impresiones": row.metrics.impressions,
                "CPM (€)": round(row.metrics.average_cpm / 1_000_000, 2),
                "CPC (€)": round(row.metrics.average_cpc / 1_000_000, 2),
                "Clics": clics, "CTR (%)": round(row.metrics.ctr * 100, 2),
                "Tasa conv. (%)": round(conv / clics * 100, 2) if clics > 0 else 0,
                "Conversiones": conv,
                "Coste/conv.": round(cost / conv, 2) if conv > 0 else None,
                "Cuota impr. (%)": pct(row.metrics.search_impression_share),
                "Cuota perd. ranking": pct(row.metrics.search_rank_lost_impression_share),
                "Cuota perd. presup.": pct(row.metrics.search_budget_lost_impression_share),
            })
        return {"campaigns": campaigns}
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_daily(since: str, until: str) -> list:
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT segments.date, metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
            ORDER BY segments.date
        """
        response = ga_service.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)
        daily: dict[str, dict] = {}
        for row in response:
            d = row.segments.date
            entry = daily.setdefault(d, {"spend": 0.0, "conv": 0.0})
            entry["spend"] += row.metrics.cost_micros / 1_000_000
            entry["conv"] += row.metrics.conversions
        return [{"date": k, "spend": round(v["spend"], 2), "leads": round(v["conv"], 1)} for k, v in sorted(daily.items())]
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_device_breakdown(since: str, until: str) -> list:
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT segments.device, metrics.cost_micros, metrics.impressions, metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
        """
        response = ga_service.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)
        DEVICE_LABEL = {"MOBILE": "Móvil", "DESKTOP": "Desktop", "TABLET": "Tablet",
                         "CONNECTED_TV": "Smart TV", "OTHER": "Otros"}
        agg: dict[str, dict] = {}
        for row in response:
            device = DEVICE_LABEL.get(row.segments.device.name, "Otros")
            entry = agg.setdefault(device, {"spend": 0.0, "impressions": 0, "conv": 0.0})
            entry["spend"] += row.metrics.cost_micros / 1_000_000
            entry["impressions"] += row.metrics.impressions
            entry["conv"] += row.metrics.conversions
        rows = []
        for device, v in agg.items():
            conv = round(v["conv"], 1)
            rows.append({
                "Dispositivo": device, "Gasto (€)": round(v["spend"], 2), "Impresiones": v["impressions"],
                "Leads": conv, "CPL": round(v["spend"] / conv, 2) if conv else None,
            })
        rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return rows
    except Exception:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_landing_pages(since: str, until: str) -> dict:
    """Rendimiento por landing page (recurso landing_page_view de la API de Google Ads).
    Si la cuenta/versión de API no soporta el recurso, devuelve error para mostrar aviso
    en vez de romper el dashboard."""
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT landing_page_view.unexpanded_final_url, campaign.name,
                   metrics.impressions, metrics.clicks, metrics.cost_micros,
                   metrics.conversions, metrics.ctr, metrics.average_cpc
            FROM landing_page_view
            WHERE segments.date BETWEEN '{since}' AND '{until}'
              AND metrics.impressions > 0
            ORDER BY metrics.cost_micros DESC
            LIMIT 100
        """
        response = ga_service.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)
        pages = []
        for row in response:
            cost = round(row.metrics.cost_micros / 1_000_000, 2)
            conv = round(row.metrics.conversions, 1)
            pages.append({
                "Landing": row.landing_page_view.unexpanded_final_url,
                "Tema": classify_tema(row.campaign.name),
                "Gasto (€)": cost, "Impresiones": row.metrics.impressions,
                "Clics": row.metrics.clicks, "CTR (%)": round(row.metrics.ctr * 100, 2),
                "CPC (€)": round(row.metrics.average_cpc / 1_000_000, 2),
                "Conversiones": conv,
                "Coste/conv.": round(cost / conv, 2) if conv > 0 else None,
            })
        return {"pages": pages}
    except Exception as e:
        return {"error": str(e)}


_KW_QUALITY = {"ABOVE_AVERAGE": "✅ Por encima", "AVERAGE": "🟡 Promedio",
               "BELOW_AVERAGE": "🔴 Por debajo", "UNKNOWN": "—"}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_keywords(since: str, until: str) -> dict:
    """Keywords con métricas completas de rendimiento y Quality Score."""
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_svc = client.get_service("GoogleAdsService")
        query = f"""
            SELECT
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group_criterion.status,
                ad_group_criterion.quality_info.quality_score,
                ad_group_criterion.quality_info.search_predicted_ctr,
                ad_group_criterion.quality_info.post_click_quality_score,
                ad_group_criterion.quality_info.creative_quality_score,
                ad_group_criterion.final_urls,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.search_impression_share,
                metrics.search_rank_lost_impression_share,
                metrics.search_click_share
            FROM keyword_view
            WHERE segments.date BETWEEN '{since}' AND '{until}'
              AND metrics.impressions > 0
            ORDER BY metrics.cost_micros DESC
            LIMIT 200
        """
        response = ga_svc.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)
        MATCH = {"EXACT": "[Exacta]", "PHRASE": '"Frase"', "BROAD": "Amplia"}

        def pct(v):
            return f"{v*100:.1f}%" if v and v > 0 else "—"

        keywords = []
        for row in response:
            crit = row.ad_group_criterion
            m = row.metrics
            cost = round(m.cost_micros / 1_000_000, 2)
            conv = round(m.conversions, 1)
            clics = m.clicks
            urls = list(crit.final_urls) if crit.final_urls else []
            campaign_name = row.campaign.name
            keywords.append({
                "Keyword": crit.keyword.text,
                "Concordancia": MATCH.get(crit.keyword.match_type.name, "—"),
                "Estado": crit.status.name,
                "Campaña": campaign_name,
                "Tema": classify_tema(campaign_name),
                "Coste": cost,
                "CTR (%)": round(m.ctr * 100, 2),
                "CPC medio": round(m.average_cpc / 1_000_000, 2),
                "Conversiones": conv,
                "Coste/conv.": round(cost / conv, 2) if conv > 0 else None,
                "Tasa conv. (%)": round(conv / clics * 100, 2) if clics > 0 else 0,
                "Cuota impr. (%)": pct(m.search_impression_share),
                "Cuota perd. ranking": pct(m.search_rank_lost_impression_share),
                "Cuota clics (%)": pct(m.search_click_share),
                "Nivel calidad": crit.quality_info.quality_score or "—",
                "URL final": urls[0] if urls else "—",
                "CTR esperado": _KW_QUALITY.get(crit.quality_info.search_predicted_ctr.name, "—"),
                "Exp. landing": _KW_QUALITY.get(crit.quality_info.post_click_quality_score.name, "—"),
                "Relevancia anuncio": _KW_QUALITY.get(crit.quality_info.creative_quality_score.name, "—"),
            })
        return {"keywords": keywords}
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_search_terms(since: str, until: str) -> dict:
    """Términos de búsqueda reales que activaron los anuncios (search_term_view) — el
    complemento natural de la tabla de Keywords: aquí se ve qué buscó de verdad la gente,
    no solo la keyword que se pujó. Flag de 'candidata a negativa': clics suficientes
    para tener señal (>=5) y cero conversiones."""
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_svc = client.get_service("GoogleAdsService")
        query = f"""
            SELECT
                search_term_view.search_term,
                campaign.name,
                metrics.impressions, metrics.clicks, metrics.cost_micros,
                metrics.conversions, metrics.ctr
            FROM search_term_view
            WHERE segments.date BETWEEN '{since}' AND '{until}'
              AND metrics.clicks > 0
            ORDER BY metrics.cost_micros DESC
            LIMIT 200
        """
        response = ga_svc.search(customer_id=GOOGLE_CUSTOMER_ID, query=query)
        terms = []
        for row in response:
            m = row.metrics
            cost = round(m.cost_micros / 1_000_000, 2)
            conv = round(m.conversions, 1)
            clics = m.clicks
            campaign_name = row.campaign.name
            terms.append({
                "Término": row.search_term_view.search_term,
                "Campaña": campaign_name, "Tema": classify_tema(campaign_name),
                "Clics": clics, "Impresiones": m.impressions,
                "CTR (%)": round(m.ctr * 100, 2),
                "Coste": cost, "Conversiones": conv,
                "Coste/conv.": round(cost / conv, 2) if conv > 0 else None,
                "Candidata a negativa": clics >= 5 and conv == 0,
            })
        return {"terms": terms}
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_ga4_landing_metrics_cached(property_id: str, since: str, until: str) -> dict:
    """Envoltorio con caché de tools.ga4_tools.fetch_ga4_landing_metrics — sin esto, la
    llamada a la API de GA4 se repetía en cada rerun del dashboard (cualquier clic en
    cualquier pestaña), no solo al cambiar de período."""
    return fetch_ga4_landing_metrics(property_id, since, until)


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_ga4_form_funnel_cached(property_id: str, since: str, until: str) -> dict:
    return fetch_ga4_form_funnel(property_id, since, until)


# ─── LEADS / CÓDIGO POSTAL ────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_dcore_leads_cached() -> dict:
    return fetch_dcore_leads()


@st.cache_data(ttl=1800, show_spinner=False)
def get_known_landings() -> list:
    """Landings principales de la pestaña Landings — se leen en vivo del Sheet de
    taxonomía (editable por Jordi/Vero sin tocar código) y, si el Sheet falla o está
    vacío, se cae a la lista fija de tools/dcore_naming.py::KNOWN_LANDINGS para que la
    pestaña nunca se quede sin filas por un problema de conexión puntual."""
    res = fetch_dcore_known_landings()
    landings = res.get("landings", [])
    return landings if landings else KNOWN_LANDINGS


# ─── FORMATO ──────────────────────────────────────────────────────────────────
def fmt_eur(v) -> str:
    if v is None: return "—"
    return f"{v:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_num(v) -> str:
    if v is None: return "—"
    return f"{int(v):,}".replace(",", ".")

def fmt_pct(v) -> str:
    if v is None: return "—"
    return f"{v:.2f}%"


_CSV_EXCLUDE_KEYS = {"preview_url", "is_video", "ad_id", "_adset_id", "_campaign_id", "_total", "_path", "_video_plays", "_thruplays"}

def render_csv_download(rows: list, filename: str, label: str, key: str):
    """Botón de descarga CSV reutilizable para las tablas del dashboard (Excel abre
    utf-8-sig sin problemas de acentos, a diferencia de utf-8 a secas)."""
    if not rows:
        return
    clean_rows = [{k: v for k, v in r.items() if k not in _CSV_EXCLUDE_KEYS} for r in rows]
    csv_bytes = pd.DataFrame(clean_rows).to_csv(index=False).encode("utf-8-sig")
    st.download_button(label, data=csv_bytes, file_name=filename, mime="text/csv", key=key)


# ─── COMPONENTES UI ───────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, icon: str = "", sub: str = "", accent: str = "#1e2440", delta: str = "") -> str:
    icon_html = f'<span class="kpi-icon">{icon}</span>' if icon else ""
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi-card" style="border-top:2px solid {accent}">'
            f'{icon_html}<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{sub_html}{delta}</div>')

def platform_header(title: str, subtitle: str, platform: str) -> str:
    icons = {"meta": "📘", "google": "📗", "combined": "🏛️"}
    cls = {"meta": "ph-meta", "google": "ph-google", "combined": "ph-combined"}
    return (f'<div class="platform-header {cls.get(platform,"")}">'
            f'<span class="ph-icon">{icons.get(platform,"")}</span>'
            f'<span class="ph-title">{title}</span>'
            f'<span class="ph-sub">{subtitle}</span></div>')

def _delta_html(current, comp, invert: bool = False) -> str:
    if current is None or comp is None or comp == 0:
        return '<span class="cmp-delta cmp-flat">—</span>'
    delta = (current - comp) / comp * 100
    is_up = delta >= 0
    good = is_up if not invert else not is_up
    cls = "cmp-up" if good else "cmp-down"
    arrow = "▲" if is_up else "▼"
    return f'<span class="cmp-delta {cls}">{arrow} {abs(delta):.1f}%</span>'

def kpi_delta(comp_display: str, current_val, comp_val, comparison_label: str, invert: bool = False) -> str:
    delta = _delta_html(current_val, comp_val, invert)
    return (f'<div class="kpi-delta"><span class="kpi-delta-value">{comp_display}</span> {delta}'
            f'<span class="kpi-delta-label">vs {comparison_label}</span></div>')

def render_disclaimers():
    st.markdown(
        '<div class="disclaimer-strip">'
        '<div class="disclaimer">⚠️ <div><b>Conversión Google Ads provisional:</b> la cuenta tiene 5 acciones de conversión "lead" activas '
        'a la vez y sin resolver cuál es la fiable (Form send / form_submit / Registro). Este dashboard usa <b>Form send (GA4)</b> '
        'mientras se confirma con Javier. No tomar decisiones de presupuesto solo con este número — ver <code>clients/dcore.md</code>.</div></div>'
        '<div class="disclaimer">📍 <div><b>Código postal solo en Meta:</b> el formulario de la web (Google Ads) no pide código postal. '
        'La zona geográfica de leads de este dashboard solo cubre leads de Meta Lead Ads. Pendiente pedir a Vero que se añada también en el '
        'formulario web si se quiere cubrir Google Ads.</div></div>'
        '</div>', unsafe_allow_html=True)


def render_dcore_alerts(meta_camps: list, google_camps: list, keywords: list, clarity_state: dict):
    """Franja de alertas automáticas — mismo criterio que dashboard_becier.py, más las
    señales propias de DCORE (Quality Score bajo, Rage clicks de Clarity) que ya se
    calculan en otras pestañas pero no saltaban a la vista sin entrar a mirarlas."""
    alerts = []

    structured = [c for c in meta_camps if not c.get("Es boost")]
    m_imp = sum(c.get("Impresiones", 0) for c in structured)
    m_cli = sum(c.get("Clics enlace", 0) for c in structured)
    if structured and m_imp:
        m_ctr = m_cli / m_imp * 100
        max_freq = max((c.get("Frecuencia", 0) for c in structured), default=0)
        if max_freq > 3.0:
            alerts.append(("warn", f"⚠️ Frecuencia Meta: {max_freq:.2f} en alguna campaña — riesgo de saturación de audiencia"))
        if m_ctr < 0.8:
            alerts.append(("danger", f"🔴 CTR Meta: {m_ctr:.2f}% — bajo umbral mínimo (0,80%)"))
        elif m_ctr >= 2.0:
            alerts.append(("ok", f"✅ CTR Meta: {m_ctr:.2f}% — buen rendimiento de creatividades"))

    if google_camps:
        g_imp = sum(c["Impresiones"] for c in google_camps)
        g_cli = sum(c["Clics"] for c in google_camps)
        g_ctr = (g_cli / g_imp * 100) if g_imp else 0
        if g_ctr < 1.0:
            alerts.append(("danger", f"🔴 CTR Google: {g_ctr:.2f}% — revisar keywords y anuncios"))
        elif g_ctr > 5.0:
            alerts.append(("ok", f"✅ CTR Google: {g_ctr:.2f}% — excelente rendimiento"))

    qs_bajo = sum(1 for k in keywords if isinstance(k["Nivel calidad"], int) and k["Nivel calidad"] <= 4)
    if qs_bajo:
        alerts.append(("warn", f"⚠️ {qs_bajo} keyword(s) con Quality Score ≤4 — revisar en la pestaña Google Ads"))

    if clarity_state.get("cached") and clarity_state.get("rows"):
        rage_landings = {r["url"] for r in clarity_state["rows"] if r["metrica"] == "Rage clicks" and r["valor"] > 0}
        if rage_landings:
            alerts.append(("danger", f"🔴 Rage clicks detectados en {len(rage_landings)} landing(s) — revisar en la pestaña Landings"))

    if not alerts:
        return
    badges = "".join(f'<span class="alert-badge alert-{level}">{msg}</span>' for level, msg in alerts)
    st.markdown(f'<div class="alert-strip">{badges}</div>', unsafe_allow_html=True)


# ─── GRÁFICOS ─────────────────────────────────────────────────────────────────
_CHART_BASE = dict(
    template="plotly_dark", paper_bgcolor="#12152a", plot_bgcolor="#12152a",
    font=dict(family="sans-serif", color="#6a7aaa"),
    hoverlabel=dict(bgcolor="#12152a", bordercolor="#2e3560", font_color="#eef0ff"),
)
_NO_INTERACT = {"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showTips": False}
_LEGEND_STATIC = dict(itemclick=False, itemdoubleclick=False, bgcolor="rgba(0,0,0,0)", font=dict(size=12, color="#b0b8d8"))

TEMA_COLORS = {
    "B2B": "#6a9fff", "Cocinas": "#fbbf24", "Evo": "#2dd4bf", "Living": "#c084fc",
    "Reformas B2C": "#c9a96e", "Impulso publicaciones": "#555",
}

_MONTHS_CA = {"January":"Enero","February":"Febrero","March":"Marzo","April":"Abril",
              "May":"Mayo","June":"Junio","July":"Julio","August":"Agosto",
              "September":"Septiembre","October":"Octubre","November":"Noviembre","December":"Diciembre"}

def chart_inversion_mensual(meta_daily: list, google_daily: list) -> go.Figure:
    def to_monthly(dl):
        if not dl:
            return pd.DataFrame(columns=["month", "month_order", "spend"])
        df = pd.DataFrame(dl)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").apply(
            lambda r: _MONTHS_CA.get(r.start_time.strftime("%B"), r.start_time.strftime("%B")) + " " + r.start_time.strftime("%Y"))
        df["month_order"] = df["date"].dt.to_period("M").apply(lambda r: str(r))
        return df.groupby(["month", "month_order"])["spend"].sum().reset_index().sort_values("month_order")

    meta_m, google_m = to_monthly(meta_daily), to_monthly(google_daily)
    months = sorted(set(list(meta_m["month"]) + list(google_m["month"])),
                     key=lambda m: meta_m.set_index("month")["month_order"].to_dict().get(
                         m, google_m.set_index("month")["month_order"].to_dict().get(m, m)))
    meta_idx, google_idx = meta_m.set_index("month")["spend"], google_m.set_index("month")["spend"]
    meta_vals = [meta_idx.get(w, 0) for w in months]
    google_vals = [google_idx.get(w, 0) for w in months]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(months), y=meta_vals, name="Meta Ads", marker_color="#4a7fff",
                         hovertemplate="<b>Meta</b>: %{y:,.2f} €<extra></extra>"))
    fig.add_trace(go.Bar(x=list(months), y=google_vals, name="Google Ads", marker_color="#34a853",
                         hovertemplate="<b>Google</b>: %{y:,.2f} €<extra></extra>"))
    fig.update_layout(**_CHART_BASE, barmode="group", height=300, margin=dict(l=4, r=4, t=10, b=4),
                      hovermode="x unified",
                      legend=dict(**_LEGEND_STATIC, orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
                      xaxis=dict(gridcolor="#1a1e35", showgrid=False),
                      yaxis=dict(gridcolor="#1a1e35", ticksuffix=" €", showgrid=True),
                      bargap=0.25, bargroupgap=0.08)
    return fig

def chart_desglose_tema(meta_camps: list) -> go.Figure:
    spend: dict[str, float] = {}
    for c in meta_camps:
        t = c.get("Tema", "Otros")
        spend[t] = spend.get(t, 0) + c.get("Gasto (€)", 0)
    labels = [t for t, s in spend.items() if s > 0]
    values = [spend[t] for t in labels]
    colors = [TEMA_COLORS.get(t, "#555") for t in labels]
    total = sum(values)
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color="#12152a", width=2)),
        textinfo="label+percent", textfont=dict(size=11, color="#eef0ff"),
        hovertemplate="<b>%{label}</b><br>%{value:,.2f} €  (%{percent})<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{fmt_eur(total)}</b><br>Total", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=13, color="#eef0ff"), xanchor="center", align="center")
    fig.update_layout(**_CHART_BASE, height=300, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
    return fig

def chart_cpl_por_tema(meta_camps: list) -> go.Figure:
    by_tema: dict[str, dict] = {}
    for c in meta_camps:
        if c.get("Es boost"):
            continue
        t = c.get("Tema", "Otros")
        by_tema.setdefault(t, {"spend": 0, "results": 0})
        by_tema[t]["spend"] += c.get("Gasto (€)", 0)
        by_tema[t]["results"] += c.get("Resultado", 0)
    temas, cpls = [], []
    for t, v in sorted(by_tema.items(), key=lambda kv: kv[1]["spend"], reverse=True):
        if v["results"] > 0:
            temas.append(t); cpls.append(round(v["spend"] / v["results"], 2))
    if not temas:
        return go.Figure()
    fig = go.Figure(go.Bar(
        y=temas, x=cpls, orientation="h", cliponaxis=False,
        marker_color=[TEMA_COLORS.get(t, "#c9a96e") for t in temas],
        text=[fmt_eur(v) for v in cpls], textposition="outside", textfont=dict(size=11, color="#8898cc"),
        hovertemplate="<b>%{y}</b>: %{x:,.2f} €<extra></extra>",
    ))
    # Margen extra a la derecha del máximo para que la etiqueta del valor más alto
    # (p. ej. el CPL de la vertical más cara) no quede cortada por el borde del gráfico.
    x_max = max(cpls) * 1.35 if cpls else 1
    fig.update_layout(**_CHART_BASE, height=300, margin=dict(l=4, r=90, t=10, b=4),
                      xaxis=dict(gridcolor="#1a1e35", ticksuffix=" €", showgrid=True, range=[0, x_max],
                                 title=dict(text="Coste por lead", font=dict(size=11, color="#5a6080"))),
                      yaxis=dict(gridcolor="rgba(0,0,0,0)"))
    return fig

_DEVICE_COLORS = {"Móvil": "#c9a96e", "Desktop": "#4a7fff", "Tablet": "#a855f7", "Smart TV": "#34a853", "Otros": "#555"}

def chart_device_breakdown(rows: list, accent: str) -> go.Figure:
    """Gasto por dispositivo (donut), con Leads/CPL en el hover."""
    rows = [r for r in rows if r["Gasto (€)"] > 0]
    if not rows:
        return go.Figure()
    devices = [r["Dispositivo"] for r in rows]
    spend = [r["Gasto (€)"] for r in rows]
    customdata = [[r["Leads"], r["CPL"] if r["CPL"] is not None else 0] for r in rows]
    total = sum(spend)
    fig = go.Figure(go.Pie(
        labels=devices, values=spend, hole=0.62,
        marker=dict(colors=[_DEVICE_COLORS.get(d, accent) for d in devices], line=dict(color="#12152a", width=2)),
        textinfo="label+percent", textfont=dict(size=11, color="#eef0ff"),
        customdata=customdata,
        hovertemplate="<b>%{label}</b>: %{value:,.2f} €  (%{percent})<br>Leads: %{customdata[0]}<br>CPL: %{customdata[1]:,.2f} €<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{fmt_eur(total)}</b><br>Total", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=13, color="#eef0ff"), xanchor="center", align="center")
    fig.update_layout(**_CHART_BASE, height=220, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
    return fig

def chart_cpl_semanal(meta_daily: list, google_daily: list) -> go.Figure:
    """Evolución del CPL/CPA por semana dentro del período — para ver si la eficiencia
    mejora o empeora semana a semana, algo que el delta de comparación (todo el período
    contra todo el período anterior) no muestra."""
    def to_weekly(dl):
        if not dl:
            return pd.DataFrame(columns=["week", "week_order", "spend", "leads"])
        df = pd.DataFrame(dl)
        df["date"] = pd.to_datetime(df["date"])
        iso = df["date"].dt.isocalendar()
        df["week_order"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
        df["week"] = "Sem " + iso["week"].astype(str)
        return df.groupby(["week", "week_order"])[["spend", "leads"]].sum().reset_index().sort_values("week_order")

    meta_w, google_w = to_weekly(meta_daily), to_weekly(google_daily)
    weeks = sorted(set(list(meta_w["week_order"])) | set(list(google_w["week_order"])))
    if not weeks:
        return go.Figure()
    meta_idx = meta_w.set_index("week_order")
    google_idx = google_w.set_index("week_order")
    week_labels = [meta_idx["week"].get(w, google_idx["week"].get(w, w)) for w in weeks]

    def cpl_series(idx):
        out = []
        for w in weeks:
            if w in idx.index:
                spend, leads = idx.loc[w, "spend"], idx.loc[w, "leads"]
                out.append(round(spend / leads, 2) if leads else None)
            else:
                out.append(None)
        return out

    def leads_series(idx):
        return [round(idx.loc[w, "leads"], 0) if w in idx.index else 0 for w in weeks]

    meta_cpl = cpl_series(meta_idx)
    google_cpl = cpl_series(google_idx)
    meta_leads = leads_series(meta_idx)
    google_leads = leads_series(google_idx)

    # Barras de volumen de leads en el eje secundario, detras de las lineas de CPL --
    # el CPL solo no dice si una semana con pocos leads es ruido estadistico o una
    # tendencia real (peticion de Jordi 2026-08-31, tras ver picos raros en el grafico).
    fig = go.Figure()
    fig.add_trace(go.Bar(x=week_labels, y=meta_leads, name="Leads Meta", yaxis="y2",
                         marker_color="#4a7fff", opacity=0.25,
                         hovertemplate="<b>Leads Meta</b>: %{y}<extra></extra>"))
    fig.add_trace(go.Bar(x=week_labels, y=google_leads, name="Leads Google", yaxis="y2",
                         marker_color="#34a853", opacity=0.25,
                         hovertemplate="<b>Leads Google</b>: %{y}<extra></extra>"))
    fig.add_trace(go.Scatter(x=week_labels, y=meta_cpl, name="CPL Meta", mode="lines+markers",
                             line=dict(color="#4a7fff", width=2), connectgaps=True,
                             hovertemplate="<b>CPL Meta</b>: %{y:,.2f} €<extra></extra>"))
    fig.add_trace(go.Scatter(x=week_labels, y=google_cpl, name="CPL Google", mode="lines+markers",
                             line=dict(color="#34a853", width=2), connectgaps=True,
                             hovertemplate="<b>CPL Google</b>: %{y:,.2f} €<extra></extra>"))
    fig.update_layout(**_CHART_BASE, height=260, margin=dict(l=4, r=4, t=10, b=4), hovermode="x unified",
                      barmode="group", bargap=0.35, bargroupgap=0.1,
                      legend=dict(**_LEGEND_STATIC, orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
                      xaxis=dict(gridcolor="#1a1e35", showgrid=False),
                      yaxis=dict(gridcolor="#1a1e35", ticksuffix=" €", showgrid=True),
                      yaxis2=dict(overlaying="y", side="right", showgrid=False, title=dict(text="Leads", font=dict(size=11, color="#5a6080"))))
    return fig

def chart_leads_map(leads_by_cp: list) -> go.Figure:
    """Mapa de puntos por CP (tamaño = nº de leads, color = zona)."""
    lats, lons, sizes, colors, texts = [], [], [], [], []
    for row in leads_by_cp:
        coords = postal_coords(row["cp"])
        if not coords:
            continue
        lats.append(coords[0]); lons.append(coords[1])
        sizes.append(8 + min(row["count"], 20) * 2.2)
        colors.append(ZONE_COLOR.get(row["zona"], "#888"))
        texts.append(f"CP {row['cp']} · {row['zona']}<br>{row['count']} lead(s)")
    fig = go.Figure(go.Scattermapbox(
        lat=lats, lon=lons, mode="markers",
        marker=dict(size=sizes, color=colors, opacity=0.85),
        text=texts, hoverinfo="text",
    ))
    fig.update_layout(
        mapbox=dict(style="open-street-map", center=dict(lat=40.4260, lon=-3.7030), zoom=9.3),
        margin=dict(l=0, r=0, t=0, b=0), height=420,
        paper_bgcolor="#12152a", font=dict(color="#6a7aaa"),
    )
    return fig


# ─── TABLA SORTABLE (iframe con JS) — reutilizado del patrón de dashboard_becier.py ──
_TABLE_CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0f18;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:2px 0;overflow-y:hidden;overflow-x:hidden}
.wrap{overflow-x:auto;border-radius:8px;border:1px solid #1e2440}
table{width:100%;border-collapse:collapse;font-size:12.5px;color:#b0b8d8}
td{white-space:nowrap}
thead{position:sticky;top:0;z-index:1}
th{background:#0f1220;color:#444c70;font-size:10.5px;font-weight:700;text-transform:uppercase;
   letter-spacing:.7px;padding:11px 14px;text-align:center;border-bottom:1px solid #1e2440;
   white-space:nowrap;cursor:pointer;user-select:none;transition:color .15s}
th:hover{color:#8898cc}
th.asc::after{content:" ▲";color:#c9a96e;font-size:9px}
th.desc::after{content:" ▼";color:#c9a96e;font-size:9px}
td{padding:10px 14px;border-bottom:1px solid #161930;text-align:center}
tr:last-child td{border-bottom:none}
tr:hover td{background:#12152a}
.num{text-align:center;font-variant-numeric:tabular-nums}
.tag{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;letter-spacing:.4px;white-space:nowrap}
tr.sec-hdr td{background:#161d32;color:#5a6898;font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:.8px;padding:12px 14px 8px;
  border-top:2px solid #1e2440;border-bottom:1px solid #1e2440;text-align:left !important}
tr.sec-hdr:first-child td{border-top:none}
tr.total-row td{background:#0f1628;color:#eef0ff;font-weight:700;font-size:12.5px;border-top:2px solid #2e3560;white-space:nowrap}
tr.cmp-row td{background:#10142a;color:#5a6080;font-size:11.5px;border-bottom:1px solid #161930}
tr.cmp-row td:first-child{padding-left:26px;font-weight:600;color:#5a6080;text-align:left}
th{position:relative}
th[data-tip]:hover::after{content:attr(data-tip);position:absolute;top:calc(100% + 6px);
  left:50%;transform:translateX(-50%);background:#1c2040;color:#c8d0f0;
  padding:7px 12px;border-radius:7px;font-size:11px;font-weight:400;
  text-transform:none;letter-spacing:0;white-space:normal;max-width:220px;
  z-index:999;border:1px solid #2e3a60;pointer-events:none;box-shadow:0 6px 16px rgba(0,0,0,.5);line-height:1.5;text-align:left}
</style>"""

_TABLE_JS = """
<script>
function sortTable(idx,th){
  const tb=document.querySelector('tbody');
  if(!tb) return;
  const allRows=Array.from(tb.children);
  const asc=th.classList.contains('asc');
  document.querySelectorAll('th').forEach(h=>h.classList.remove('asc','desc'));
  const isNum=v=>/^-?\\d+(\\.\\d+)?$/.test(String(v).trim());
  const cmp=(a,b)=>{
    const ac=a.cells[idx]; const bc=b.cells[idx];
    if(!ac||!bc) return 0;
    const av=ac.dataset.v!==undefined?ac.dataset.v:ac.textContent.trim();
    const bv=bc.dataset.v!==undefined?bc.dataset.v:bc.textContent.trim();
    if(isNum(av)&&isNum(bv)){ const an=parseFloat(av), bn=parseFloat(bv); return asc?bn-an:an-bn; }
    return asc?String(bv).localeCompare(String(av),'es'):String(av).localeCompare(String(bv),'es');
  };
  const groupRows=rows=>{
    const items=[];
    rows.forEach(r=>{ if(r.dataset.cmp && items.length) items[items.length-1].cmpRows.push(r); else items.push({main:r,cmpRows:[]}); });
    return items;
  };
  const hasSec=allRows.some(r=>r.dataset.sec);
  if(!hasSec){
    const items=groupRows(allRows);
    items.sort((a,b)=>cmp(a.main,b.main));
    items.forEach(it=>{ tb.appendChild(it.main); it.cmpRows.forEach(r=>tb.appendChild(r)); });
  } else {
    const secs=[]; let cur={hdr:null,rows:[]};
    allRows.forEach(r=>{ if(r.dataset.sec){secs.push(cur);cur={hdr:r,rows:[]};} else cur.rows.push(r); });
    secs.push(cur);
    secs.forEach(s=>{
      const items=groupRows(s.rows);
      items.sort((a,b)=>cmp(a.main,b.main));
      if(s.hdr) tb.appendChild(s.hdr);
      items.forEach(it=>{ tb.appendChild(it.main); it.cmpRows.forEach(r=>tb.appendChild(r)); });
    });
  }
  th.classList.add(asc?'desc':'asc');
}
</script>"""

def _th(label: str, idx: int, num: bool = False, tip: str = "") -> str:
    cls = "num-h" if num else ""
    dtip = f' data-tip="{tip}"' if tip else ""
    return f'<th class="{cls}" onclick="sortTable({idx},this)"{dtip}>{label}</th>'

def _num_td(display: str, raw) -> str:
    return f'<td class="num" data-v="{raw}">{display}</td>'

def _tag_cell(text: str, css: str) -> str:
    return f'<td data-v="{text}"><span class="tag {css}">{text}</span></td>'

def _campaign_cell(name: str, active_campaign) -> str:
    import html as _html
    is_active = bool(active_campaign) and name == active_campaign
    safe_name = _html.escape(name)
    cls = "camp-link active" if is_active else "camp-link"
    title = "Clic para quitar el filtro" if is_active else "Clic para filtrar Adsets y Creatividades"
    return (f'<td data-v="{safe_name}"><span class="{cls}" data-campaign="{safe_name}" title="{title}">{safe_name}</span></td>')


META_TIPS = {
    "Importe gastado": "Importe total invertido en el período", "Impresiones": "Número total de veces que se mostró el anuncio",
    "Alcance": "Personas únicas que vieron el anuncio al menos una vez", "CPM": "Coste por cada 1.000 impresiones",
    "CPC": "Coste medio por clic en el enlace del anuncio", "CTR": "% de personas que hicieron clic tras ver el anuncio",
    "Clics": "Clics en el enlace del anuncio", "Leads": "Leads conseguidos", "CPL": "Coste medio por lead",
    "Objetivo": "Qué está optimizando/midiendo realmente esta campaña — no comparar CPL entre objetivos distintos",
}


def render_meta_table(campaigns: list, active_campaign=None) -> str | None:
    if not campaigns:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de campañas.</p>', unsafe_allow_html=True)
        return active_campaign

    structured = [c for c in campaigns if not c.get("Es boost")]
    boosts = [c for c in campaigns if c.get("Es boost")]

    COLS = [
        {"key": "Campaña", "label": "Campaña"}, {"key": "Tema", "label": "Tema"},
        {"key": "Resultado Key", "label": "Objetivo"},
        {"key": "Gasto (€)", "label": "Importe gastado", "num": True, "eur": True},
        {"key": "Impresiones", "label": "Impresiones", "num": True},
        {"key": "Alcance", "label": "Alcance", "num": True},
        {"key": "CPM", "label": "CPM", "num": True, "eur": True},
        {"key": "CPC", "label": "CPC", "num": True, "eur": True},
        {"key": "CTR (%)", "label": "CTR", "num": True},
        {"key": "Clics enlace", "label": "Clics", "num": True},
        {"key": "Resultado", "label": "Leads", "num": True},
        {"key": "Coste/Resultado", "label": "CPL", "num": True, "eur": True},
    ]
    ncols = len(COLS)

    def make_row(c):
        cells = ""
        for col in COLS:
            key = col["key"]
            if key == "Campaña":
                cells += _campaign_cell(c["Campaña"], active_campaign)
            elif key == "Tema":
                cells += _tag_cell(c.get("Tema", "—"), TEMA_STYLES.get(c.get("Tema", ""), "tag-other"))
            elif key == "CTR (%)":
                cells += f'<td class="num" data-v="{c.get(key,0)}">{fmt_pct(c.get(key,0))}</td>'
            elif col.get("eur"):
                cells += _num_td(fmt_eur(c.get(key)), c.get(key) or 0)
            elif col.get("num"):
                cells += _num_td(fmt_num(c.get(key)), c.get(key) or 0)
            else:
                cells += f'<td>{c.get(key,"—")}</td>'
        return f"<tr>{cells}</tr>"

    tbody = f'<tr class="sec-hdr" data-sec="1"><td colspan="{ncols}">🎯  Campañas (Lead Ads y tráfico estructurado)</td></tr>'
    tbody += "".join(make_row(c) for c in structured)

    if boosts:
        b_spend = sum(c["Gasto (€)"] for c in boosts)
        b_imp = sum(c["Impresiones"] for c in boosts)
        b_alc = sum(c["Alcance"] for c in boosts)
        b_cli = sum(c.get("Clics enlace", 0) for c in boosts)
        b_cpm = round(b_spend / b_imp * 1000, 2) if b_imp else 0
        b_cpc = round(b_spend / b_cli, 2) if b_cli else 0
        b_ctr = round(b_cli / b_imp * 100, 2) if b_imp else 0
        tbody += f'<tr class="sec-hdr" data-sec="1"><td colspan="{ncols}">📸  Impulso de publicaciones de Instagram (agregado, {len(boosts)} campañas)</td></tr>'
        tbody += (f'<tr><td>Impulso de publicaciones (orgánico)</td>' + _tag_cell("Impulso publicaciones", "tag-other")
                  + '<td>—</td>'
                  + _num_td(fmt_eur(b_spend), b_spend) + _num_td(fmt_num(b_imp), b_imp) + _num_td(fmt_num(b_alc), b_alc)
                  + _num_td(fmt_eur(b_cpm), b_cpm) + _num_td(fmt_eur(b_cpc), b_cpc)
                  + f'<td class="num">{fmt_pct(b_ctr)}</td>' + _num_td(fmt_num(b_cli), b_cli)
                  + '<td class="num">—</td><td class="num">—</td></tr>')

    t_spend = sum(c["Gasto (€)"] for c in campaigns)
    t_imp = sum(c["Impresiones"] for c in campaigns)
    t_alc = sum(c["Alcance"] for c in campaigns)
    t_cli = sum(c.get("Clics enlace", 0) for c in campaigns)
    t_res = sum(c.get("Resultado", 0) for c in structured)
    t_cpm = round(t_spend / t_imp * 1000, 2) if t_imp else 0
    t_cpc = round(t_spend / t_cli, 2) if t_cli else 0
    t_ctr = round(t_cli / t_imp * 100, 2) if t_imp else 0
    t_cpr = round(sum(c["Gasto (€)"] for c in structured) / t_res, 2) if t_res else None
    total_row = (f'<tr class="total-row"><td>TOTAL</td><td></td><td></td>'
                 + _num_td(fmt_eur(t_spend), t_spend) + _num_td(fmt_num(t_imp), t_imp) + _num_td(fmt_num(t_alc), t_alc)
                 + _num_td(fmt_eur(t_cpm), t_cpm) + _num_td(fmt_eur(t_cpc), t_cpc)
                 + f'<td class="num">{fmt_pct(t_ctr)}</td>' + _num_td(fmt_num(t_cli), t_cli)
                 + _num_td(fmt_num(t_res), t_res) + _num_td(fmt_eur(t_cpr), t_cpr or 0) + '</tr>')

    heads = "".join(_th(c["label"], i, c.get("num", False), META_TIPS.get(c["label"], "")) for i, c in enumerate(COLS))
    table_html = f'<table><thead><tr>{heads}</tr></thead><tbody>{tbody}{total_row}</tbody></table>'
    new_active = _clickable_meta_table(html=table_html, active=active_campaign, key="dcore_campaign_click", default=active_campaign)
    return new_active


def render_meta_adsets_table(adsets: list):
    if not adsets:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de adsets.</p>', unsafe_allow_html=True)
        return
    COLS = [
        {"key": "Adset", "label": "Adset"}, {"key": "Tema", "label": "Tema"},
        {"key": "Resultado Key", "label": "Objetivo"},
        {"key": "Gasto (€)", "label": "Importe gastado", "num": True, "eur": True},
        {"key": "Impresiones", "label": "Impresiones", "num": True}, {"key": "Alcance", "label": "Alcance", "num": True},
        {"key": "CPM", "label": "CPM", "num": True, "eur": True}, {"key": "CPC", "label": "CPC", "num": True, "eur": True},
        {"key": "CTR (%)", "label": "CTR", "num": True}, {"key": "Clics enlace", "label": "Clics", "num": True},
        {"key": "Resultado", "label": "Leads", "num": True}, {"key": "Coste/Resultado", "label": "CPL", "num": True, "eur": True},
    ]
    heads = "".join(_th(c["label"], i, c.get("num", False), META_TIPS.get(c["label"], "")) for i, c in enumerate(COLS))
    rows = ""
    for a in adsets:
        cells = ""
        for col in COLS:
            key = col["key"]
            if key == "Tema":
                cells += _tag_cell(a.get("Tema", "—"), TEMA_STYLES.get(a.get("Tema", ""), "tag-other"))
            elif key == "CTR (%)":
                cells += f'<td class="num" data-v="{a.get(key,0)}">{fmt_pct(a.get(key,0))}</td>'
            elif col.get("eur"):
                cells += _num_td(fmt_eur(a.get(key)), a.get(key) or 0)
            elif col.get("num"):
                cells += _num_td(fmt_num(a.get(key)), a.get(key) or 0)
            else:
                cells += f'<td>{a.get(key,"—")}</td>'
        rows += f"<tr>{cells}</tr>"
    height = len(adsets) * 42 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


def render_creatives_table(ads: list):
    if not ads:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de anuncios.</p>', unsafe_allow_html=True)
        return
    THUMB_CSS = "width:80px;height:80px;object-fit:cover;border-radius:6px;display:block;background:#1a1e35"
    VIDEO_OVERLAY = ("<div style='position:relative;width:80px;height:80px'><img src='{url}' style='" + THUMB_CSS + "'>"
                     "<div style='position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.65);"
                     "border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff'>▶</div></div>")
    IMG_HTML = "<img src='{url}' style='" + THUMB_CSS + "'>"
    NO_IMG = "<div style='" + THUMB_CSS + ";border:1px dashed #2a3060'></div>"

    heads = ('<th style="cursor:default">Vista previa</th>' + _th("Anuncio", 1) + _th("Ángulo", 2) + _th("Landing", 3)
             + _th("Hook", 4) + _th("Formato", 5) + _th("Estado", 6) + _th("Gasto", 7, True) + _th("Impresiones", 8, True)
             + _th("CPM", 9, True) + _th("CPC", 10, True) + _th("CTR", 11, True) + _th("Clics", 12, True)
             + _th("Hook Rate", 13, True, "Reproducciones 2seg / Impresiones — solo vídeo") + _th("Hold Rate", 14, True, "ThruPlay / Reproducciones 2seg — solo vídeo")
             + _th("Leads", 15, True) + _th("CPL", 16, True))
    STATUS_COLOR = {"ACTIVE": "#22c55e", "PAUSED": "#fbbf24", "DELETED": "#f87171", "ARCHIVED": "#888", "ADSET_PAUSED": "#a855f7"}
    rows = ""
    for a in ads:
        url = a.get("preview_url", "")
        thumb = VIDEO_OVERLAY.format(url=url) if (url and a["is_video"]) else (IMG_HTML.format(url=url) if url else NO_IMG)
        status = a.get("Estado", "")
        status_html = f'<span style="color:{STATUS_COLOR.get(status,"#888")};font-size:11px;font-weight:600">{status}</span>'
        rows += (f'<tr><td style="padding:8px 14px">{thumb}</td>'
                 f'<td data-v="{a["Anuncio"]}" style="max-width:220px;white-space:normal;text-align:left">{a["Anuncio"]}</td>'
                 f'<td data-v="{a["Ángulo"]}">{a["Ángulo"]}</td><td data-v="{a["Landing"]}">{a["Landing"]}</td>'
                 f'<td data-v="{a["Hook"]}">{a["Hook"]}</td><td data-v="{a.get("Formato","—")}">{a.get("Formato","—")}</td>'
                 f'<td data-v="{status}">{status_html}</td>'
                 + _num_td(fmt_eur(a["Gasto (€)"]), a["Gasto (€)"]) + _num_td(fmt_num(a["Impresiones"]), a["Impresiones"])
                 + _num_td(fmt_eur(a["CPM"]), a["CPM"]) + _num_td(fmt_eur(a["CPC"]), a["CPC"])
                 + f'<td class="num" data-v="{a["CTR (%)"]}">{fmt_pct(a["CTR (%)"])}</td>'
                 + _num_td(fmt_num(a["Clics"]), a["Clics"])
                 + f'<td class="num" data-v="{a.get("Hook Rate (%)") or 0}">{fmt_pct(a.get("Hook Rate (%)"))}</td>'
                 + f'<td class="num" data-v="{a.get("Hold Rate (%)") or 0}">{fmt_pct(a.get("Hold Rate (%)"))}</td>'
                 + _num_td(fmt_num(a["Resultado"]), a["Resultado"])
                 + _num_td(fmt_eur(a["CPR"]), a["CPR"] or 0) + '</tr>')
    height = len(ads) * 100 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


CREATIVES_EXTRA_COLS = ["Ángulo", "Landing", "Hook", "Formato", "Impresiones", "CPM", "CPC", "Clics"]


def render_all_creatives_table(ads: list, extra_cols: list = None):
    """Como render_creatives_table pero con Campaña/Tema, para la pestaña 'Todas las
    creatividades' (todas las campañas juntas, sin tener que entrar campaña a campaña)."""
    if not ads:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin creatividades para este filtro.</p>', unsafe_allow_html=True)
        return
    THUMB_CSS = "width:70px;height:70px;object-fit:cover;border-radius:6px;display:block;background:#1a1e35"
    VIDEO_OVERLAY = ("<div style='position:relative;width:70px;height:70px'><img src='{url}' style='" + THUMB_CSS + "'>"
                     "<div style='position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.65);"
                     "border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#fff'>▶</div></div>")
    IMG_HTML = "<img src='{url}' style='" + THUMB_CSS + "'>"
    NO_IMG = "<div style='" + THUMB_CSS + ";border:1px dashed #2a3060'></div>"
    STATUS_COLOR = {"ACTIVE": "#22c55e", "PAUSED": "#fbbf24", "DELETED": "#f87171", "ARCHIVED": "#888", "ADSET_PAUSED": "#a855f7"}

    def _thumb_cell(a):
        url = a.get("preview_url", "")
        thumb = VIDEO_OVERLAY.format(url=url) if (url and a["is_video"]) else (IMG_HTML.format(url=url) if url else NO_IMG)
        return f'<td style="padding:8px 14px">{thumb}</td>'

    def _status_cell(a):
        status = a.get("Estado", "")
        return f'<td data-v="{status}"><span style="color:{STATUS_COLOR.get(status,"#888")};font-size:11px;font-weight:600">{status}</span></td>'

    # (label, tip, esencial, es_num, celda)
    COLS = [
        ("Vista previa", "", True, False, _thumb_cell),
        ("Campaña", "", True, False,
         lambda a: f'<td data-v="{a["Campaña"]}" title="{a["Campaña"]}" style="max-width:170px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:left">{a["Campaña"]}</td>'),
        ("Tema", "", True, False, lambda a: _tag_cell(a.get("Tema", "—"), TEMA_STYLES.get(a.get("Tema", ""), "tag-other"))),
        ("Anuncio", "", True, False,
         lambda a: f'<td data-v="{a["Anuncio"]}" title="{a["Anuncio"]}" style="max-width:190px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:left">{a["Anuncio"]}</td>'),
        ("Ángulo", "", False, False, lambda a: f'<td data-v="{a["Ángulo"]}">{a["Ángulo"]}</td>'),
        ("Landing", "", False, False, lambda a: f'<td data-v="{a["Landing"]}">{a["Landing"]}</td>'),
        ("Hook", "", False, False, lambda a: f'<td data-v="{a["Hook"]}">{a["Hook"]}</td>'),
        ("Formato", "", False, False, lambda a: f'<td data-v="{a.get("Formato","—")}">{a.get("Formato","—")}</td>'),
        ("Estado", "", True, False, _status_cell),
        ("Gasto", "", True, True, lambda a: _num_td(fmt_eur(a["Gasto (€)"]), a["Gasto (€)"])),
        ("Impresiones", "", False, True, lambda a: _num_td(fmt_num(a["Impresiones"]), a["Impresiones"])),
        ("CPM", "", False, True, lambda a: _num_td(fmt_eur(a["CPM"]), a["CPM"])),
        ("CPC", "", False, True, lambda a: _num_td(fmt_eur(a["CPC"]), a["CPC"])),
        ("CTR", "", True, True, lambda a: f'<td class="num" data-v="{a["CTR (%)"]}">{fmt_pct(a["CTR (%)"])}</td>'),
        ("Clics", "", False, True, lambda a: _num_td(fmt_num(a["Clics"]), a["Clics"])),
        ("Hook Rate", "Reproducciones 2seg / Impresiones — solo vídeo", True, True,
         lambda a: f'<td class="num" data-v="{a.get("Hook Rate (%)") or 0}">{fmt_pct(a.get("Hook Rate (%)"))}</td>'),
        ("Hold Rate", "ThruPlay / Reproducciones 2seg — solo vídeo", True, True,
         lambda a: f'<td class="num" data-v="{a.get("Hold Rate (%)") or 0}">{fmt_pct(a.get("Hold Rate (%)"))}</td>'),
        ("Leads", "", True, True, lambda a: _num_td(fmt_num(a["Resultado"]), a["Resultado"])),
        ("CPL", "", True, True, lambda a: _num_td(fmt_eur(a["CPR"]), a["CPR"] or 0)),
    ]
    extra_set = set(extra_cols or [])
    visible = [c for c in COLS if c[2] or c[0] in extra_set]
    heads = "".join(
        ('<th style="cursor:default">Vista previa</th>' if label == "Vista previa" else _th(label, i, is_num, tip))
        for i, (label, tip, ess, is_num, fn) in enumerate(visible)
    )
    rows = ""
    for a in ads:
        rows += "<tr>" + "".join(fn(a) for (_, _, _, _, fn) in visible) + "</tr>"
    height = min(len(ads) * 90 + 56, 900)
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


def render_google_table(campaigns: list):
    if not campaigns:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de campañas.</p>', unsafe_allow_html=True)
        return
    heads = (_th("Campaña", 0) + _th("Tema", 1) + _th("Coste", 2, True) + _th("Impresiones", 3, True) + _th("CPM medio", 4, True)
             + _th("CPC medio", 5, True) + _th("Clics", 6, True) + _th("CTR", 7, True) + _th("Conv.", 8, True) + _th("Coste/conv.", 9, True)
             + _th("Tasa conv.", 10, True, "% de clics que generaron una conversión")
             + _th("Cuota impr.", 11, True, "% de impresiones obtenidas vs. total posible en búsquedas")
             + _th("Cuota perd. ranking", 12, True, "% de impresiones perdidas por baja posición del anuncio. Mejorar puja o Quality Score")
             + _th("Cuota perd. presup.", 13, True, "% de impresiones perdidas por falta de presupuesto"))
    rows = ""
    for c in campaigns:
        rows += (f'<tr><td data-v="{c["Campaña"]}">{c["Campaña"]}</td>'
                 + _tag_cell(c.get("Tema", "—"), TEMA_STYLES.get(c.get("Tema", ""), "tag-other"))
                 + _num_td(fmt_eur(c["Gasto (€)"]), c["Gasto (€)"]) + _num_td(fmt_num(c["Impresiones"]), c["Impresiones"])
                 + _num_td(fmt_eur(c["CPM (€)"]), c["CPM (€)"]) + _num_td(fmt_eur(c["CPC (€)"]), c["CPC (€)"])
                 + _num_td(fmt_num(c["Clics"]), c["Clics"]) + f'<td class="num" data-v="{c["CTR (%)"]}">{fmt_pct(c["CTR (%)"])}</td>'
                 + _num_td(str(int(c["Conversiones"])), c["Conversiones"]) + _num_td(fmt_eur(c["Coste/conv."]), c["Coste/conv."] or 0)
                 + f'<td class="num" data-v="{c.get("Tasa conv. (%)",0)}">{fmt_pct(c.get("Tasa conv. (%)"))}</td>'
                 + f'<td data-v="{c.get("Cuota impr. (%)","—")}">{c.get("Cuota impr. (%)","—")}</td>'
                 + f'<td data-v="{c.get("Cuota perd. ranking","—")}">{c.get("Cuota perd. ranking","—")}</td>'
                 + f'<td data-v="{c.get("Cuota perd. presup.","—")}">{c.get("Cuota perd. presup.","—")}</td>' + '</tr>')
    g_spend = sum(c["Gasto (€)"] for c in campaigns); g_imp = sum(c["Impresiones"] for c in campaigns)
    g_cli = sum(c["Clics"] for c in campaigns); g_conv = sum(c["Conversiones"] for c in campaigns)
    g_cpm = round(g_spend / g_imp * 1000, 2) if g_imp else 0
    g_cpc = round(g_spend / g_cli, 2) if g_cli else 0
    g_ctr = round(g_cli / g_imp * 100, 2) if g_imp else 0
    g_cpa = round(g_spend / g_conv, 2) if g_conv else None
    g_tasa_conv = round(g_conv / g_cli * 100, 2) if g_cli else 0
    total_row = (f'<tr class="total-row"><td>TOTAL</td><td></td>' + _num_td(fmt_eur(g_spend), g_spend) + _num_td(fmt_num(g_imp), g_imp)
                 + _num_td(fmt_eur(g_cpm), g_cpm) + _num_td(fmt_eur(g_cpc), g_cpc) + _num_td(fmt_num(g_cli), g_cli)
                 + f'<td class="num">{fmt_pct(g_ctr)}</td>' + _num_td(str(int(g_conv)), g_conv) + _num_td(fmt_eur(g_cpa), g_cpa or 0)
                 + f'<td class="num">{fmt_pct(g_tasa_conv)}</td><td>—</td><td>—</td><td>—</td>' + '</tr>')
    height = len(campaigns) * 42 + 100
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}{total_row}</tbody></table></div>',
                    height=height, scrolling=True)


KEYWORDS_EXTRA_COLS = ["Tasa conv.", "Cuota impr.", "Cuota perd. ranking", "Cuota clics",
                       "URL final", "CTR esperado", "Exp. landing", "Relevancia anuncio"]


def render_google_keywords_table(keywords: list, extra_cols: list = None):
    if not keywords:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de keywords.</p>', unsafe_allow_html=True)
        return

    MATCH_CSS = {"[Exacta]": "tl", '"Frase"': "tp", "Amplia": "to"}
    STATUS_COLOR = {"ENABLED": "#22c55e", "PAUSED": "#fbbf24", "REMOVED": "#f87171"}

    def _status_cell(k):
        status = k.get("Estado", "—")
        return f'<td data-v="{status}"><span style="color:{STATUS_COLOR.get(status,"#888")};font-size:11px;font-weight:600">{status}</span></td>'

    def _url_cell(k):
        url = k["URL final"]
        url_display = url[:35] + "…" if len(url) > 37 else url
        if url and url != "—":
            return f'<td title="{url}" data-v="{url}" style="text-align:left"><a href="{url}" target="_blank" style="color:inherit;text-decoration:underline dotted">{url_display}</a></td>'
        return f'<td title="{url}" data-v="{url}" style="text-align:left">{url_display}</td>'

    # (label, tip, esencial, es_num, celda)
    COLS = [
        ("Keyword", "", True, False, lambda k: f'<td data-v="{k["Keyword"]}" style="text-align:left">{k["Keyword"]}</td>'),
        ("Concordancia", "Tipo: [Exacta] busca la kw exacta · 'Frase' incluye variantes · Amplia muestra en búsquedas relacionadas", True, False,
         lambda k: _tag_cell(k["Concordancia"], MATCH_CSS.get(k["Concordancia"], "to"))),
        ("Estado", "", True, False, _status_cell),
        ("Tema", "", True, False, lambda k: _tag_cell(k.get("Tema", "—"), TEMA_STYLES.get(k.get("Tema", ""), "tag-other"))),
        ("Conversiones", "Conversiones registradas en el período", True, True,
         lambda k: _num_td(str(int(k["Conversiones"])), k["Conversiones"])),
        ("Coste/conv.", "Coste medio por conversión conseguida", True, True,
         lambda k: _num_td(fmt_eur(k["Coste/conv."]), k["Coste/conv."] or 0)),
        ("Coste", "Importe total invertido en esta keyword", True, True, lambda k: _num_td(fmt_eur(k["Coste"]), k["Coste"])),
        ("CTR", "% de clics sobre el total de impresiones", True, True,
         lambda k: f'<td class="num" data-v="{k["CTR (%)"]}">{fmt_pct(k["CTR (%)"])}</td>'),
        ("CPC medio", "Coste medio por clic en esta keyword", True, True, lambda k: _num_td(fmt_eur(k["CPC medio"]), k["CPC medio"])),
        ("Nivel calidad", "Puntuación de Google (1-10). Influye en el CPC real y la posición del anuncio", True, True,
         lambda k: f'<td class="num" data-v="{k["Nivel calidad"]}">{k["Nivel calidad"]}</td>'),
        ("Tasa conv.", "% de clics que generaron una conversión", False, True,
         lambda k: f'<td class="num" data-v="{k["Tasa conv. (%)"]}">{fmt_pct(k["Tasa conv. (%)"])}</td>'),
        ("Cuota impr.", "% de impresiones obtenidas vs. total posible en búsquedas", False, True,
         lambda k: f'<td class="num" data-v="{k["Cuota impr. (%)"]}">{k["Cuota impr. (%)"]}</td>'),
        ("Cuota perd. ranking", "% de impresiones perdidas por baja posición del anuncio. Mejorar puja o Quality Score", False, True,
         lambda k: f'<td class="num" data-v="{k["Cuota perd. ranking"]}">{k["Cuota perd. ranking"]}</td>'),
        ("Cuota clics", "% de clics obtenidos del total disponible", False, True,
         lambda k: f'<td class="num" data-v="{k["Cuota clics (%)"]}">{k["Cuota clics (%)"]}</td>'),
        ("URL final", "Página de destino a la que va el usuario al hacer clic", False, False, _url_cell),
        ("CTR esperado", "Predicción de Google sobre si esta keyword generará clics", False, False,
         lambda k: f'<td data-v="{k["CTR esperado"]}">{k["CTR esperado"]}</td>'),
        ("Exp. landing", "Valoración de Google sobre la relevancia de la página de destino para esta keyword", False, False,
         lambda k: f'<td data-v="{k["Exp. landing"]}">{k["Exp. landing"]}</td>'),
        ("Relevancia anuncio", "Grado de coincidencia entre el texto del anuncio y la intención de búsqueda del usuario", False, False,
         lambda k: f'<td data-v="{k["Relevancia anuncio"]}">{k["Relevancia anuncio"]}</td>'),
    ]
    extra_set = set(extra_cols or [])
    visible = [c for c in COLS if c[2] or c[0] in extra_set]
    heads = "".join(_th(label, i, is_num, tip) for i, (label, tip, ess, is_num, fn) in enumerate(visible))

    rows = ""
    for k in keywords:
        rows += "<tr>" + "".join(fn(k) for (_, _, _, _, fn) in visible) + "</tr>"

    t_sp = sum(k["Coste"] for k in keywords)
    t_conv = sum(k["Conversiones"] for k in keywords)
    t_cpa = round(t_sp / t_conv, 2) if t_conv else None
    TOTAL_FN = {
        "Conversiones": lambda: _num_td(str(int(t_conv)), t_conv),
        "Coste/conv.": lambda: _num_td(fmt_eur(t_cpa), t_cpa or 0),
        "Coste": lambda: _num_td(fmt_eur(t_sp), t_sp),
    }
    total_cells = []
    for i, (label, tip, ess, is_num, fn) in enumerate(visible):
        if i == 0:
            total_cells.append("<td>TOTAL</td>")
        elif label in TOTAL_FN:
            total_cells.append(TOTAL_FN[label]())
        else:
            total_cells.append("<td></td>")
    total_row = f'<tr class="total-row">{"".join(total_cells)}</tr>'

    height = len(keywords) * 42 + 56 + 44
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}{total_row}</tbody></table></div>',
                    height=height, scrolling=True)


def render_search_terms_table(terms: list):
    if not terms:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de términos de búsqueda.</p>', unsafe_allow_html=True)
        return
    heads = (_th("Término de búsqueda", 0)
             + _th("Tema", 1) + _th("Campaña", 2)
             + _th("Clics", 3, True) + _th("Impresiones", 4, True) + _th("CTR", 5, True)
             + _th("Coste", 6, True) + _th("Conv.", 7, True) + _th("Coste/conv.", 8, True)
             + _th("⚠ Negativa", 9, False, "Clics ≥5 y 0 conversiones — candidata a excluir como palabra negativa"))
    rows = ""
    for t in terms:
        flag = '<span style="color:#f87171;font-weight:700">Sí</span>' if t["Candidata a negativa"] else "—"
        rows += (f'<tr><td data-v="{t["Término"]}" style="text-align:left">{t["Término"]}</td>'
                 + _tag_cell(t.get("Tema", "—"), TEMA_STYLES.get(t.get("Tema", ""), "tag-other"))
                 + f'<td data-v="{t["Campaña"]}" title="{t["Campaña"]}" style="max-width:170px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:left">{t["Campaña"]}</td>'
                 + _num_td(fmt_num(t["Clics"]), t["Clics"]) + _num_td(fmt_num(t["Impresiones"]), t["Impresiones"])
                 + f'<td class="num" data-v="{t["CTR (%)"]}">{fmt_pct(t["CTR (%)"])}</td>'
                 + _num_td(fmt_eur(t["Coste"]), t["Coste"]) + _num_td(str(int(t["Conversiones"])), t["Conversiones"])
                 + _num_td(fmt_eur(t["Coste/conv."]), t["Coste/conv."] or 0)
                 + f'<td data-v="{1 if t["Candidata a negativa"] else 0}">{flag}</td></tr>')
    height = min(len(terms) * 42 + 56, 700)
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


def render_landings_scorecard(rows: list, show_ga4: bool):
    """Tabla de landings: Gasto/Clics/Conv. son SIEMPRE de Google Ads (nunca mezclan
    canales). Si hay GA4, las sesiones se separan explícitamente por canal (Google Ads
    vs Meta/Otros) en vez de un único número mezclado — evita leer 'sesiones altas' de
    una landing y asumir que vienen del gasto de Google Ads de al lado cuando en
    realidad son de Meta u orgánico."""
    if not rows:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de landing pages para el período.</p>', unsafe_allow_html=True)
        return
    heads = (_th("Landing", 0) + _th("Gasto (Google Ads)", 1, True) + _th("Impresiones", 2, True) + _th("Clics", 3, True)
             + _th("CTR", 4, True) + _th("CPC", 5, True) + _th("Conv.", 6, True) + _th("Coste/conv.", 7, True))
    if show_ga4:
        heads += (_th("Sesiones Google Ads", 8, True, "Sesiones de GA4 atribuidas al canal Paid Search — deben ir en línea con los Clics de la izquierda")
                  + _th("Sesiones Meta/Otros", 9, True, "Sesiones de GA4 de cualquier otro canal (Meta, orgánico, directo…). Aproximado a la baja: Meta no tiene UTMs en todos los anuncios")
                  + _th("Interacción GA4", 10, True, "% de sesiones con interacción (engagement), todos los canales"))
    rows_html = ""
    for p in rows:
        url_short = p["Landing"]
        full_url = f"https://dcore.es{p.get('_path', '')}" if p.get("_path") else ""
        landing_html = f'<a href="{full_url}" target="_blank" style="color:inherit;text-decoration:underline dotted">{url_short}</a>' if full_url else url_short
        row = (f'<tr><td data-v="{url_short}" style="max-width:260px;white-space:normal;text-align:left">{landing_html}</td>'
               + _num_td(fmt_eur(p["Gasto (€)"]), p["Gasto (€)"]) + _num_td(fmt_num(p["Impresiones"]), p["Impresiones"])
               + _num_td(fmt_num(p["Clics"]), p["Clics"]) + f'<td class="num" data-v="{p["CTR (%)"]}">{fmt_pct(p["CTR (%)"])}</td>'
               + _num_td(fmt_eur(p["CPC (€)"]), p["CPC (€)"]) + _num_td(str(int(p["Conversiones"])), p["Conversiones"])
               + _num_td(fmt_eur(p["Coste/conv."]), p["Coste/conv."] or 0))
        if show_ga4:
            row += (_num_td(fmt_num(p.get("Sesiones Google Ads")), p.get("Sesiones Google Ads") or 0)
                    + _num_td(fmt_num(p.get("Sesiones Meta/Otros")), p.get("Sesiones Meta/Otros") or 0)
                    + f'<td class="num" data-v="{p.get("Interacción GA4 (%)") or 0}">{fmt_pct(p.get("Interacción GA4 (%)"))}</td>')
        rows_html += row + '</tr>'
    height = len(rows) * 42 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows_html}</tbody></table></div>',
                    height=height, scrolling=True)


def pivot_clarity_by_landing(rows: list, device_filter: str = "Todos") -> list:
    """Convierte las filas planas de Clarity (métrica/url/device/valor) en una tabla
    con una fila por landing y una columna por métrica — mucho más legible que la lista
    plana original (ver conversación 2026-08-31)."""
    pivot: dict[str, dict] = {}
    for r in rows:
        if device_filter != "Todos" and r["device"] != device_filter:
            continue
        url = r["url"]
        entry = pivot.setdefault(url, {"Rage clicks": 0, "Quickback clicks": 0, "Dead clicks": 0, "_scroll": []})
        if r["metrica"] == "Scroll depth medio":
            entry["_scroll"].append(r["valor"])
        elif r["metrica"] in entry:
            entry[r["metrica"]] += r["valor"]
    result = []
    for url, entry in pivot.items():
        scroll_vals = entry.pop("_scroll")
        scroll_avg = round(sum(scroll_vals) / len(scroll_vals), 1) if scroll_vals else None
        total_problemas = entry["Rage clicks"] + entry["Quickback clicks"] + entry["Dead clicks"]
        result.append({"Landing": url, **entry, "Scroll depth medio (%)": scroll_avg, "_total": total_problemas})
    result.sort(key=lambda r: (-r["_total"], r["Landing"]))
    return result


def render_clarity_scorecard(rows: list):
    if not rows:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de Clarity para este filtro.</p>', unsafe_allow_html=True)
        return
    heads = (_th("Landing", 0) + _th("Rage clicks", 1, True, "Clics repetidos y frenéticos: algo no responde — CTA roto o formulario que falla")
             + _th("Quickback clicks", 2, True, "Entra y le da a 'atrás' casi al instante — desajuste entre el anuncio y la landing")
             + _th("Dead clicks", 3, True, "Clic en una zona que no hace nada — confusión de UI, menor urgencia que Rage clicks")
             + _th("Scroll depth medio", 4, True, "% medio de la página que ve el usuario antes de irse"))
    rows_html = ""
    for r in rows:
        rage = r["Rage clicks"]; quick = r["Quickback clicks"]; dead = r["Dead clicks"]; scroll = r["Scroll depth medio (%)"]
        rage_html = f'<span style="color:#f87171;font-weight:700">{fmt_num(rage)}</span>' if rage > 0 else fmt_num(rage)
        quick_html = f'<span style="color:#fbbf24;font-weight:700">{fmt_num(quick)}</span>' if quick > 0 else fmt_num(quick)
        dead_html = f'<span style="color:#fbbf24;font-weight:700">{fmt_num(dead)}</span>' if dead > 0 else fmt_num(dead)
        landing_path = r["Landing"]
        full_url = f"https://dcore.es{landing_path}" if landing_path and landing_path != "—" else ""
        landing_html = f'<a href="{full_url}" target="_blank" style="color:inherit;text-decoration:underline dotted">{landing_path}</a>' if full_url else landing_path
        rows_html += (f'<tr><td data-v="{landing_path}" style="max-width:260px;white-space:normal;text-align:left">{landing_html}</td>'
                      + f'<td class="num" data-v="{rage}">{rage_html}</td>'
                      + f'<td class="num" data-v="{quick}">{quick_html}</td>'
                      + f'<td class="num" data-v="{dead}">{dead_html}</td>'
                      + f'<td class="num" data-v="{scroll or 0}">{fmt_pct(scroll)}</td></tr>')
    height = len(rows) * 42 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows_html}</tbody></table></div>',
                    height=height, scrolling=True)


def render_leads_zone_table(leads_by_cp: list):
    if not leads_by_cp:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin leads con código postal en el período.</p>', unsafe_allow_html=True)
        return
    ZONE_TAG = {"Dentro M-30": "tag-m30", "Fuera M-30 (Madrid/CM)": "tag-cm", "Fuera de la Comunidad de Madrid": "tag-fuera", "CP inválido": "tag-other"}
    heads = _th("Código postal", 0) + _th("Zona", 1) + _th("Nº leads", 2, True)
    rows = ""
    for row in leads_by_cp:
        rows += (f'<tr><td data-v="{row["cp"]}">{row["cp"]}</td>'
                 + _tag_cell(row["zona"], ZONE_TAG.get(row["zona"], "tag-other"))
                 + _num_td(fmt_num(row["count"]), row["count"]) + '</tr>')
    height = len(leads_by_cp) * 42 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    default_since, default_until = get_prev_month_range()
    qp = st.query_params

    period_options = {
        "Mes anterior": _period_last_month(), "Este mes": _period_this_month(),
        "Últimos 7 días": _period_last_n(7), "Últimos 30 días": _period_last_n(30),
        "Últimos 90 días": _period_last_n(90), "Rango personalizado": None,
    }

    with st.sidebar:
        st.markdown(
            '<div style="padding:16px 0 20px">'
            '<img src="https://dcore.es/wp-content/uploads/2025/02/dcore-logo-black-gold-1-1.svg" '
            'style="height:34px;object-fit:contain;filter:invert(1) brightness(1.6)">'
            '<div style="font-size:11px;color:#3a4060;margin-top:6px">Performance Dashboard</div></div>',
            unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        if st.button("🔄  Refrescar datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        st.markdown('<div style="color:#2a3050;font-size:10px;margin-top:8px">Caché: 30 min</div>', unsafe_allow_html=True)

        st.markdown('<hr style="border-color:#1a1e35;margin:16px 0 12px">', unsafe_allow_html=True)
        st.markdown('<div style="color:#3a4060;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px">Vertical (Tema)</div>',
                    unsafe_allow_html=True)
        _tema_opts = ["🔘 Todas", "🔵 B2B", "🟡 Cocinas", "🟢 Evo", "🟣 Living", "🟤 Reformas B2C"]
        _tema_idx = _tema_opts.index(qp.get("tema")) if qp.get("tema") in _tema_opts else 0
        sel_tema_sidebar = st.selectbox("", _tema_opts, index=_tema_idx, key="dcore_tema_filter", label_visibility="collapsed")
        st.query_params["tema"] = sel_tema_sidebar

    col_sel, col_cmp, col_pad = st.columns([2, 2, 3])
    with col_sel:
        _period_keys = list(period_options.keys())
        _period_idx = _period_keys.index(qp.get("period")) if qp.get("period") in _period_keys else 0
        selected = st.selectbox("📅 Período", _period_keys, index=_period_idx, key="period_sel")
        st.query_params["period"] = selected
        if selected == "Rango personalizado":
            _qp_since = qp.get("since", default_since); _qp_until = qp.get("until", default_until)
            c_d1, c_d2 = st.columns(2)
            since = str(c_d1.date_input("Desde", value=date.fromisoformat(_qp_since)))
            until = str(c_d2.date_input("Hasta", value=date.fromisoformat(_qp_until)))
            st.query_params["since"] = since; st.query_params["until"] = until
        else:
            since, until = period_options[selected]
    period_label = selected if selected != "Rango personalizado" else f"{since} – {until}"

    with col_cmp:
        _cmp_idx = COMPARISON_OPTIONS.index(qp.get("cmp")) if qp.get("cmp") in COMPARISON_OPTIONS else 0
        comparison_mode = st.selectbox("🔁 Comparar con", COMPARISON_OPTIONS, index=_cmp_idx, key="cmp_sel")
        st.query_params["cmp"] = comparison_mode

    comp_since, comp_until = compute_comparison_range(since, until, comparison_mode)

    with st.spinner("Cargando datos…"):
        meta_camps = fetch_meta_campaigns(since, until)
        meta_adsets = fetch_meta_adsets_detail(since, until)
        meta_daily = fetch_meta_daily(since, until)
        google_res = fetch_google_campaigns(since, until)
        google_daily = fetch_google_daily(since, until)
        landing_res = fetch_google_landing_pages(since, until)
        keywords_res = fetch_google_keywords(since, until)
        leads_res = fetch_dcore_leads_cached()
        meta_devices = fetch_meta_device_breakdown(since, until)
        google_devices = fetch_google_device_breakdown(since, until)
        search_terms_res = fetch_google_search_terms(since, until)

    google_camps = google_res.get("campaigns", [])
    google_error = google_res.get("error")

    if comp_since:
        with st.spinner("Cargando comparación…"):
            meta_camps_cmp = fetch_meta_campaigns(comp_since, comp_until)
            google_camps_cmp = fetch_google_campaigns(comp_since, comp_until).get("campaigns", [])
            keywords_cmp = fetch_google_keywords(comp_since, comp_until).get("keywords", [])
    else:
        meta_camps_cmp, google_camps_cmp, keywords_cmp = [], [], []

    # Filtro de Tema/Vertical del sidebar — aplica a Meta y Google a la vez. El impulso
    # de publicaciones de Instagram nunca es una vertical elegible, así que un tema
    # seleccionado siempre lo excluye (no tiene sentido "boost de X vertical").
    _tema_map = {"🔵 B2B": "B2B", "🟡 Cocinas": "Cocinas", "🟢 Evo": "Evo",
                 "🟣 Living": "Living", "🟤 Reformas B2C": "Reformas B2C"}
    sel_tema = _tema_map.get(sel_tema_sidebar)
    keywords = keywords_res.get("keywords", [])
    if sel_tema:
        meta_camps = [c for c in meta_camps if c.get("Tema") == sel_tema]
        meta_adsets = [a for a in meta_adsets if a.get("Tema") == sel_tema]
        google_camps = [c for c in google_camps if c.get("Tema") == sel_tema]
        meta_camps_cmp = [c for c in meta_camps_cmp if c.get("Tema") == sel_tema]
        google_camps_cmp = [c for c in google_camps_cmp if c.get("Tema") == sel_tema]
        keywords = [k for k in keywords if k.get("Tema") == sel_tema]
        keywords_cmp = [k for k in keywords_cmp if k.get("Tema") == sel_tema]

    meta_spend = sum(c["Gasto (€)"] for c in meta_camps)
    google_spend = sum(c["Gasto (€)"] for c in google_camps)
    total_spend = meta_spend + google_spend

    st.markdown(
        f'<div class="dash-header">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<img src="https://dcore.es/wp-content/uploads/2025/02/dcore-logo-black-gold-1-1.svg" '
        f'style="height:30px;object-fit:contain;filter:invert(1) brightness(1.6)" alt="DCORE"></div>'
        f'<div class="dash-right" style="display:flex;align-items:center;gap:20px">'
        f'<div style="text-align:right">'
        f'<div style="color:#444c70;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.8px">Inversión total del período</div>'
        f'<div style="color:#eef0ff;font-size:38px;font-weight:800;letter-spacing:-1px;line-height:1.1">{fmt_eur(total_spend)}</div></div>'
        f'<div class="dash-period">📅 {period_label}<br><span style="font-size:12px;color:#3a4060">{fmt_date_ddmmyyyy(since)} – {fmt_date_ddmmyyyy(until)}</span></div>'
        f'</div></div>', unsafe_allow_html=True)

    render_disclaimers()
    clarity_state = get_cached_snapshot()  # solo lectura de disco, no gasta cuota de Clarity
    render_dcore_alerts(meta_camps, google_camps, keywords, clarity_state)

    # ── KPIs ──────────────────────────────────────────────────────────────
    col_meta, col_google = st.columns(2, gap="large")
    META_COLOR, GOOGLE_COLOR = "#4a7fff", "#34a853"

    with col_meta:
        st.markdown(platform_header("Meta Ads", f"Cuenta DCORE · {_meta_account_id()}", "meta"), unsafe_allow_html=True)
        structured = [c for c in meta_camps if not c.get("Es boost")]
        mf_imp = sum(c.get("Impresiones", 0) for c in meta_camps)
        mf_alc = sum(c.get("Alcance", 0) for c in meta_camps)
        mf_cli = sum(c.get("Clics enlace", 0) for c in meta_camps)
        mf_cpm = round(meta_spend / mf_imp * 1000, 2) if mf_imp else 0
        mf_ctr = round(mf_cli / mf_imp * 100, 2) if mf_imp else 0
        mf_cpc = round(meta_spend / mf_cli, 2) if mf_cli else 0
        leads_total = sum(c.get("Resultado", 0) for c in structured)
        leads_spend = sum(c.get("Gasto (€)", 0) for c in structured)
        cpl = round(leads_spend / leads_total, 2) if leads_total else None

        d_spend = d_alc = d_imp = d_cpm = d_ctr = d_cpc = d_leads = d_cpl = ""
        if comp_since:
            cstructured = [c for c in meta_camps_cmp if not c.get("Es boost")]
            c_spend = sum(c["Gasto (€)"] for c in meta_camps_cmp)
            c_imp = sum(c.get("Impresiones", 0) for c in meta_camps_cmp)
            c_alc = sum(c.get("Alcance", 0) for c in meta_camps_cmp)
            c_cli = sum(c.get("Clics enlace", 0) for c in meta_camps_cmp)
            c_cpm = round(c_spend / c_imp * 1000, 2) if c_imp else 0
            c_ctr = round(c_cli / c_imp * 100, 2) if c_imp else 0
            c_cpc = round(c_spend / c_cli, 2) if c_cli else 0
            c_leads = sum(c.get("Resultado", 0) for c in cstructured)
            c_leads_spend = sum(c.get("Gasto (€)", 0) for c in cstructured)
            c_cpl = round(c_leads_spend / c_leads, 2) if c_leads else None
            d_spend = kpi_delta(fmt_eur(c_spend), meta_spend, c_spend, comparison_mode)
            d_alc = kpi_delta(fmt_num(c_alc), mf_alc, c_alc, comparison_mode)
            d_imp = kpi_delta(fmt_num(c_imp), mf_imp, c_imp, comparison_mode)
            d_cpm = kpi_delta(fmt_eur(c_cpm), mf_cpm, c_cpm, comparison_mode, invert=True)
            d_ctr = kpi_delta(fmt_pct(c_ctr), mf_ctr, c_ctr, comparison_mode)
            d_cpc = kpi_delta(fmt_eur(c_cpc), mf_cpc, c_cpc, comparison_mode, invert=True)
            d_leads = kpi_delta(fmt_num(c_leads), leads_total, c_leads, comparison_mode)
            d_cpl = kpi_delta(fmt_eur(c_cpl), cpl, c_cpl, comparison_mode, invert=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(kpi_card("Gasto total", fmt_eur(meta_spend), "💰", accent=META_COLOR, delta=d_spend), unsafe_allow_html=True)
        c2.markdown(kpi_card("Alcance", fmt_num(mf_alc), "👁️", accent=META_COLOR, delta=d_alc), unsafe_allow_html=True)
        c3.markdown(kpi_card("Impresiones", fmt_num(mf_imp), "📊", accent=META_COLOR, delta=d_imp), unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        c4.markdown(kpi_card("CPM", fmt_eur(mf_cpm), "📈", accent=META_COLOR, delta=d_cpm), unsafe_allow_html=True)
        c5.markdown(kpi_card("CTR", fmt_pct(mf_ctr), "🖱️", accent=META_COLOR, delta=d_ctr), unsafe_allow_html=True)
        c6.markdown(kpi_card("CPC", fmt_eur(mf_cpc), "💶", accent=META_COLOR, delta=d_cpc), unsafe_allow_html=True)
        c7, c8, _ = st.columns(3)
        c7.markdown(kpi_card("Leads", fmt_num(leads_total), "🎯", accent=META_COLOR, delta=d_leads), unsafe_allow_html=True)
        c8.markdown(kpi_card("CPL", fmt_eur(cpl), "💡", accent=META_COLOR, delta=d_cpl), unsafe_allow_html=True)

    with col_google:
        st.markdown(platform_header("Google Ads", f"Cuenta DCORE · {GOOGLE_CUSTOMER_ID}", "google"), unsafe_allow_html=True)
        if google_error:
            st.markdown(f'<p style="color:#f87171;font-size:13px">⚠ {google_error}</p>', unsafe_allow_html=True)
        elif google_camps:
            total_imp = sum(c["Impresiones"] for c in google_camps)
            total_cli = sum(c["Clics"] for c in google_camps)
            total_conv = sum(c["Conversiones"] for c in google_camps)
            avg_ctr = (total_cli / total_imp * 100) if total_imp else 0
            avg_cpc = (google_spend / total_cli) if total_cli else 0
            avg_cpm = (google_spend / total_imp * 1000) if total_imp else 0
            cost_conv = (google_spend / total_conv) if total_conv else None

            d_g_spend = d_g_cli = d_g_imp = d_g_ctr = d_g_cpc = d_g_conv = d_g_cpa = ""
            if comp_since:
                cg_spend = sum(c["Gasto (€)"] for c in google_camps_cmp)
                cg_imp = sum(c["Impresiones"] for c in google_camps_cmp)
                cg_cli = sum(c["Clics"] for c in google_camps_cmp)
                cg_conv = sum(c["Conversiones"] for c in google_camps_cmp)
                cg_ctr = (cg_cli / cg_imp * 100) if cg_imp else 0
                cg_cpc = (cg_spend / cg_cli) if cg_cli else 0
                cg_cpa = (cg_spend / cg_conv) if cg_conv else None
                d_g_spend = kpi_delta(fmt_eur(cg_spend), google_spend, cg_spend, comparison_mode)
                d_g_cli = kpi_delta(fmt_num(cg_cli), total_cli, cg_cli, comparison_mode)
                d_g_imp = kpi_delta(fmt_num(cg_imp), total_imp, cg_imp, comparison_mode)
                d_g_ctr = kpi_delta(fmt_pct(cg_ctr), avg_ctr, cg_ctr, comparison_mode)
                d_g_cpc = kpi_delta(fmt_eur(cg_cpc), avg_cpc, cg_cpc, comparison_mode, invert=True)
                d_g_conv = kpi_delta(f"{cg_conv:.0f}", total_conv, cg_conv, comparison_mode)
                d_g_cpa = kpi_delta(fmt_eur(cg_cpa), cost_conv, cg_cpa, comparison_mode, invert=True)

            c1, c2, c3 = st.columns(3)
            c1.markdown(kpi_card("Gasto total", fmt_eur(google_spend), "💰", accent=GOOGLE_COLOR, delta=d_g_spend), unsafe_allow_html=True)
            c2.markdown(kpi_card("Clics", fmt_num(total_cli), "🖱️", accent=GOOGLE_COLOR, delta=d_g_cli), unsafe_allow_html=True)
            c3.markdown(kpi_card("Impresiones", fmt_num(total_imp), "📊", accent=GOOGLE_COLOR, delta=d_g_imp), unsafe_allow_html=True)
            c4, c5, c6 = st.columns(3)
            c4.markdown(kpi_card("CTR medio", fmt_pct(avg_ctr), "📈", accent=GOOGLE_COLOR, delta=d_g_ctr), unsafe_allow_html=True)
            c5.markdown(kpi_card("CPC medio", fmt_eur(avg_cpc), "💶", accent=GOOGLE_COLOR, delta=d_g_cpc), unsafe_allow_html=True)
            c6.markdown(kpi_card("Conversiones", f"{total_conv:.0f}", "✅", accent=GOOGLE_COLOR, delta=d_g_conv), unsafe_allow_html=True)
            c7, _, _ = st.columns(3)
            c7.markdown(kpi_card("Coste / conv.", fmt_eur(cost_conv), "💡", accent=GOOGLE_COLOR, delta=d_g_cpa), unsafe_allow_html=True)

            # Embudo de formulario (2026-08-31, a petición de Jordi): form_start/Form
            # Send/form_submit como 3 etapas independientes en vez de adivinar cuál es
            # "la" conversión — hasta que se decida con Javier cuál dejar como oficial
            # en Google Ads. Vienen de GA4 (Google Ads no tiene form_start importado
            # como acción de conversión), filtrados al canal Paid Search para que
            # reflejen solo tráfico de Google Ads, igual que el resto de esta sección.
            ga4_property_id_funnel = os.environ.get("GA4_PROPERTY_ID_DCORE", "")
            if ga4_property_id_funnel:
                funnel = fetch_ga4_form_funnel_cached(ga4_property_id_funnel, since, until)
                if funnel.get("error"):
                    st.markdown(f'<p style="color:#fbbf24;font-size:11.5px;margin-top:8px">⚠ Embudo de formulario (GA4) no disponible: {funnel["error"]}</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                    st.markdown(
                        '<div style="color:#5a6080;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.7px;margin:6px 0 4px">'
                        'Embudo de formulario (GA4, solo tráfico Google Ads) — 3 etapas, no 3 conversiones independientes</div>',
                        unsafe_allow_html=True)
                    fs, fsend, fsub = funnel["form_start"], funnel["form_send"], funnel["form_submit"]
                    total_funnel = fs + fsend + fsub
                    cf1, cf2, cf3, cf4 = st.columns(4)
                    cf1.markdown(kpi_card("form_start", fmt_num(fs), "1️⃣", accent=GOOGLE_COLOR), unsafe_allow_html=True)
                    cf2.markdown(kpi_card("Form Send", fmt_num(fsend), "2️⃣", accent=GOOGLE_COLOR), unsafe_allow_html=True)
                    cf3.markdown(kpi_card("form_submit", fmt_num(fsub), "3️⃣", accent=GOOGLE_COLOR), unsafe_allow_html=True)
                    cf4.markdown(kpi_card("Suma de las 3", fmt_num(total_funnel), "Σ", accent="#c9a96e"), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de Google Ads para el período.</p>', unsafe_allow_html=True)

    # ── Gráficos ──────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(platform_header("Análisis visual", f"{fmt_date_ddmmyyyy(since)} – {fmt_date_ddmmyyyy(until)}", "combined"), unsafe_allow_html=True)
    col_evo, col_donut, col_cpl = st.columns([5, 3, 3], gap="medium")

    def chart_label(text):
        st.markdown(f'<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">{text}</div>', unsafe_allow_html=True)

    with col_evo:
        chart_label("Inversión mensual — Meta vs Google")
        if sel_tema:
            # Con filtro de Tema activo: el desglose diario de fetch_meta_daily/fetch_google_daily
            # es a nivel de cuenta (no por campaña), así que se sustituye por un único punto con
            # el gasto ya filtrado, para no mostrar el total de la cuenta como si fuera del tema.
            _mock_meta = [{"date": since, "spend": meta_spend}] if meta_spend else []
            _mock_google = [{"date": since, "spend": google_spend}] if google_spend else []
            st.plotly_chart(chart_inversion_mensual(_mock_meta, _mock_google), use_container_width=True, config=_NO_INTERACT)
        elif meta_daily or google_daily:
            st.plotly_chart(chart_inversion_mensual(meta_daily, google_daily), use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos diarios.</p>', unsafe_allow_html=True)

    with col_donut:
        chart_label("Presupuesto Meta por tema")
        if meta_camps:
            st.plotly_chart(chart_desglose_tema(meta_camps), use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos.</p>', unsafe_allow_html=True)

    with col_cpl:
        chart_label("CPL por tema (Meta)")
        fig_cpl = chart_cpl_por_tema(meta_camps)
        if fig_cpl.data:
            st.plotly_chart(fig_cpl, use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de resultados.</p>', unsafe_allow_html=True)

    # meta_daily/google_daily y los desgloses de dispositivo se calculan a nivel de
    # cuenta completa (sin Tema), igual que el gráfico de inversión mensual de arriba —
    # con el filtro de Tema activo se ocultan en vez de mostrar un dato mezclado que
    # parecería del tema seleccionado sin serlo.
    if not sel_tema:
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        col_weekly, col_dev = st.columns([6, 4], gap="medium")
        with col_weekly:
            chart_label("Evolución CPL/CPA por semana")
            fig_weekly = chart_cpl_semanal(meta_daily, google_daily)
            if fig_weekly.data:
                st.plotly_chart(fig_weekly, use_container_width=True, config=_NO_INTERACT)
            else:
                st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos suficientes para una evolución semanal.</p>', unsafe_allow_html=True)
        with col_dev:
            chart_label("Gasto por dispositivo")
            col_dm, col_dg = st.columns(2)
            with col_dm:
                st.markdown('<div style="color:#4a7fff;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:4px">Meta</div>', unsafe_allow_html=True)
                fig_dm = chart_device_breakdown(meta_devices, "#4a7fff")
                if fig_dm.data:
                    st.plotly_chart(fig_dm, use_container_width=True, config=_NO_INTERACT)
                else:
                    st.markdown('<p style="color:#5a6080;font-size:12px">Sin datos.</p>', unsafe_allow_html=True)
            with col_dg:
                st.markdown('<div style="color:#34a853;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:4px">Google</div>', unsafe_allow_html=True)
                fig_dg = chart_device_breakdown(google_devices, "#34a853")
                if fig_dg.data:
                    st.plotly_chart(fig_dg, use_container_width=True, config=_NO_INTERACT)
                else:
                    st.markdown('<p style="color:#5a6080;font-size:12px">Sin datos.</p>', unsafe_allow_html=True)

    # ── Tablas ────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    tab_meta, tab_google, tab_creatives, tab_landings, tab_quality = st.tabs(
        ["📘  Meta Ads", "📗  Google Ads", "🎬  Todas las creatividades", "🔗  Landings", "🏆  Calidad de leads"])

    with tab_meta:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        _valid_campaigns = {c["Campaña"] for c in meta_camps}
        _seed_campaign = st.session_state.get("dcore_campaign_click")
        if _seed_campaign not in _valid_campaigns:
            _seed_campaign = None
        active_campaign = render_meta_table(meta_camps, _seed_campaign)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        if active_campaign:
            st.markdown(f'<div style="color:#c9a96e;font-size:12px;font-weight:700;margin-bottom:10px">🎯 Adsets y creatividades de: {active_campaign}</div>', unsafe_allow_html=True)
            camp_adsets = [a for a in meta_adsets if a["Campaña"] == active_campaign]
            render_meta_adsets_table(camp_adsets)

            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Creatividades</div>', unsafe_allow_html=True)
            adset_names = [a["Adset"] for a in camp_adsets]
            if adset_names:
                sel_adset_name = st.selectbox("Adset", adset_names, key="dcore_adset_sel")
                sel_adset_id = next((a["_adset_id"] for a in camp_adsets if a["Adset"] == sel_adset_name), None)
                if sel_adset_id:
                    ads = fetch_meta_ads_for_adset(sel_adset_id, since, until)
                    render_creatives_table(ads)
        else:
            st.markdown('<p style="color:#5a6080;font-size:12px">Clic en el nombre de una campaña de la tabla para ver sus adsets y creatividades (con Ángulo/Landing/Hook cuando el nombre siga la convención propuesta a Vero).</p>', unsafe_allow_html=True)

    with tab_google:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        render_google_table(google_camps)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Keywords</div>', unsafe_allow_html=True)
        if keywords_res.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:12px">⚠ No se pudo obtener el informe de keywords: {keywords_res["error"]}</p>', unsafe_allow_html=True)
        else:
            kw_status_filter = st.selectbox("Estado", ["Activas", "Pausadas", "Todas"], key="dcore_kw_status_filter")
            if kw_status_filter == "Activas":
                kw_view = [k for k in keywords if k.get("Estado") == "ENABLED"]
                kw_cmp_view = [k for k in keywords_cmp if k.get("Estado") == "ENABLED"]
            elif kw_status_filter == "Pausadas":
                kw_view = [k for k in keywords if k.get("Estado") == "PAUSED"]
                kw_cmp_view = [k for k in keywords_cmp if k.get("Estado") == "PAUSED"]
            else:
                kw_view, kw_cmp_view = keywords, keywords_cmp

            if kw_view:
                kk1, kk2, kk3, kk4 = st.columns(4)
                t_kw_cost = sum(k["Coste"] for k in kw_view)
                t_kw_conv = sum(k["Conversiones"] for k in kw_view)
                t_kw_cpa = round(t_kw_cost / t_kw_conv, 2) if t_kw_conv else None
                bajo_qs = sum(1 for k in kw_view if isinstance(k["Nivel calidad"], int) and k["Nivel calidad"] <= 4)

                d_kw_n = d_kw_cost = d_kw_cpa = d_kw_qs = ""
                if comp_since:
                    c_kw_cost = sum(k["Coste"] for k in kw_cmp_view)
                    c_kw_conv = sum(k["Conversiones"] for k in kw_cmp_view)
                    c_kw_cpa = round(c_kw_cost / c_kw_conv, 2) if c_kw_conv else None
                    c_bajo_qs = sum(1 for k in kw_cmp_view if isinstance(k["Nivel calidad"], int) and k["Nivel calidad"] <= 4)
                    d_kw_n = kpi_delta(fmt_num(len(kw_cmp_view)), len(kw_view), len(kw_cmp_view), comparison_mode)
                    d_kw_cost = kpi_delta(fmt_eur(c_kw_cost), t_kw_cost, c_kw_cost, comparison_mode)
                    d_kw_cpa = kpi_delta(fmt_eur(c_kw_cpa), t_kw_cpa, c_kw_cpa, comparison_mode, invert=True)
                    d_kw_qs = kpi_delta(fmt_num(c_bajo_qs), bajo_qs, c_bajo_qs, comparison_mode, invert=True)

                kk1.markdown(kpi_card("Keywords", fmt_num(len(kw_view)), "🔑", accent="#34a853", delta=d_kw_n), unsafe_allow_html=True)
                kk2.markdown(kpi_card("Gasto", fmt_eur(t_kw_cost), "💰", accent="#34a853", delta=d_kw_cost), unsafe_allow_html=True)
                kk3.markdown(kpi_card("Coste/conv. medio", fmt_eur(t_kw_cpa), "💡", accent="#34a853", delta=d_kw_cpa), unsafe_allow_html=True)
                kk4.markdown(kpi_card("Con Quality Score bajo (≤4)", fmt_num(bajo_qs), "⚠️", accent="#fbbf24" if bajo_qs else "#34a853", delta=d_kw_qs), unsafe_allow_html=True)
                render_csv_download(kw_view, f"dcore_keywords_{since}_{until}.csv", "⬇️ Descargar CSV", "dcore_kw_csv")
                kw_extra_cols = st.multiselect("Columnas adicionales", KEYWORDS_EXTRA_COLS, key="dcore_kw_extra_cols")
                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            else:
                kw_extra_cols = []
            render_google_keywords_table(kw_view, kw_extra_cols)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Términos de búsqueda</div>', unsafe_allow_html=True)
        if search_terms_res.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:12px">⚠ No se pudo obtener el informe de términos de búsqueda: {search_terms_res["error"]}</p>', unsafe_allow_html=True)
        else:
            terms = search_terms_res.get("terms", [])
            if sel_tema:
                terms = [t for t in terms if t.get("Tema") == sel_tema]
            n_neg = sum(1 for t in terms if t["Candidata a negativa"])
            if n_neg:
                st.markdown(f'<p style="color:#fbbf24;font-size:12px;margin-bottom:8px">⚠ {n_neg} término(s) con clics sin ninguna conversión — candidatos a excluir como negativa.</p>', unsafe_allow_html=True)
            render_csv_download(terms, f"dcore_search_terms_{since}_{until}.csv", "⬇️ Descargar CSV", "dcore_st_csv")
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            render_search_terms_table(terms)

    with tab_creatives:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#5a6080;font-size:12px">Todas las creatividades de campañas Lead Ad/tráfico estructurado del período, en una sola tabla ordenable — sin entrar campaña a campaña. El impulso de publicaciones de Instagram (sin convención de nombre) queda fuera.</p>', unsafe_allow_html=True)
        with st.spinner("Cargando todas las creatividades…"):
            all_ads = fetch_meta_ads_all(since, until)

        if not all_ads:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin creatividades estructuradas para el período.</p>', unsafe_allow_html=True)
        else:
            f1, f2 = st.columns(2)
            temas_disponibles = ["🔘 Todos"] + sorted({a["Tema"] for a in all_ads})
            tc_sel_tema = f1.selectbox("Filtrar por tema", temas_disponibles, key="dcore_all_creatives_tema")
            campanas_disponibles = ["🔘 Todas"]
            if tc_sel_tema != "🔘 Todos":
                campanas_disponibles += sorted({a["Campaña"] for a in all_ads if a["Tema"] == tc_sel_tema})
            else:
                campanas_disponibles += sorted({a["Campaña"] for a in all_ads})
            sel_campana = f2.selectbox("Filtrar por campaña", campanas_disponibles, key="dcore_all_creatives_camp")

            filtered = all_ads
            if tc_sel_tema != "🔘 Todos":
                filtered = [a for a in filtered if a["Tema"] == tc_sel_tema]
            if sel_campana != "🔘 Todas":
                filtered = [a for a in filtered if a["Campaña"] == sel_campana]

            n_ads = len(filtered)
            total_gasto = sum(a["Gasto (€)"] for a in filtered)
            total_resultados = sum(a["Resultado"] for a in filtered)
            cpr_medio = round(total_gasto / total_resultados, 2) if total_resultados else None

            d_ads_n = d_ads_gasto = d_ads_res = d_ads_cpr = ""
            if comp_since:
                with st.spinner("Cargando comparación de creatividades…"):
                    all_ads_cmp = fetch_meta_ads_all(comp_since, comp_until)
                filtered_cmp = all_ads_cmp
                if tc_sel_tema != "🔘 Todos":
                    filtered_cmp = [a for a in filtered_cmp if a["Tema"] == tc_sel_tema]
                if sel_campana != "🔘 Todas":
                    filtered_cmp = [a for a in filtered_cmp if a["Campaña"] == sel_campana]
                c_gasto = sum(a["Gasto (€)"] for a in filtered_cmp)
                c_res = sum(a["Resultado"] for a in filtered_cmp)
                c_cpr = round(c_gasto / c_res, 2) if c_res else None
                d_ads_n = kpi_delta(fmt_num(len(filtered_cmp)), n_ads, len(filtered_cmp), comparison_mode)
                d_ads_gasto = kpi_delta(fmt_eur(c_gasto), total_gasto, c_gasto, comparison_mode)
                d_ads_res = kpi_delta(fmt_num(c_res), total_resultados, c_res, comparison_mode)
                d_ads_cpr = kpi_delta(fmt_eur(c_cpr), cpr_medio, c_cpr, comparison_mode, invert=True)

            k1, k2, k3, k4 = st.columns(4)
            k1.markdown(kpi_card("Creatividades", fmt_num(n_ads), "🎬", accent="#c9a96e", delta=d_ads_n), unsafe_allow_html=True)
            k2.markdown(kpi_card("Gasto", fmt_eur(total_gasto), "💰", accent="#c9a96e", delta=d_ads_gasto), unsafe_allow_html=True)
            k3.markdown(kpi_card("Leads", fmt_num(total_resultados), "🎯", accent="#c9a96e", delta=d_ads_res), unsafe_allow_html=True)
            k4.markdown(kpi_card("CPL medio", fmt_eur(cpr_medio), "💡", accent="#c9a96e", delta=d_ads_cpr), unsafe_allow_html=True)
            render_csv_download(filtered, f"dcore_creatividades_{since}_{until}.csv", "⬇️ Descargar CSV", "dcore_creatives_csv")
            creas_extra_cols = st.multiselect("Columnas adicionales", CREATIVES_EXTRA_COLS, key="dcore_creas_extra_cols")

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            render_all_creatives_table(filtered, creas_extra_cols)

    with tab_landings:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:#5a6080;font-size:12px">Landings principales de DCORE, siempre visibles aunque no hayan tenido '
            'gasto de Google Ads ese período (reciben tráfico sobre todo de Meta). Gasto/Clics/Conv. son siempre de Google Ads; '
            'las sesiones de GA4 se separan por canal para no mezclarlas. '
            '<a href="https://docs.google.com/spreadsheets/d/1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k/edit#gid=1717543581" target="_blank">'
            'Añadir/editar landings aquí</a> (pestaña "LANDINGS" de Creatividades Dcore, rellena "Url activa") — no hace falta tocar código.</p>',
            unsafe_allow_html=True)

        ga4_property_id = os.environ.get("GA4_PROPERTY_ID_DCORE", "")
        ga4_by_path, ga4_error = {}, None
        if ga4_property_id:
            ga4_res = fetch_ga4_landing_metrics_cached(ga4_property_id, since, until)
            if ga4_res.get("error"):
                ga4_error = ga4_res["error"]
            else:
                ga4_by_path = {r["path"]: r for r in ga4_res.get("rows", [])}

        # Agregar el informe de Google Ads por path limpio (varias combinaciones de UTM
        # pueden compartir la misma landing real, ej. con/sin {ignore} sin expandir).
        # Se guarda también el gasto por Tema de cada path, para poder filtrar esta
        # pestaña con el mismo selector de Vertical del sidebar que el resto del
        # dashboard (antes esta pestaña ignoraba ese filtro por completo).
        google_by_path: dict[str, dict] = {}
        if landing_res.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:12px">⚠ No se pudo obtener el informe de Google Ads: {landing_res["error"]}</p>', unsafe_allow_html=True)
        else:
            for p in landing_res.get("pages", []):
                raw_url = p["Landing"] if "://" in p["Landing"] else f"https://{p['Landing']}"
                raw_path = urlparse(raw_url).path or "/"
                path = re.sub(r"\{[^}]*\}", "", raw_path) or "/"
                g = google_by_path.setdefault(path, {"Gasto (€)": 0.0, "Impresiones": 0, "Clics": 0, "Conversiones": 0.0, "_tema_gasto": {}})
                g["Gasto (€)"] += p["Gasto (€)"]; g["Impresiones"] += p["Impresiones"]
                g["Clics"] += p["Clics"]; g["Conversiones"] += p["Conversiones"]
                g["_tema_gasto"][p["Tema"]] = g["_tema_gasto"].get(p["Tema"], 0) + p["Gasto (€)"]
            for g in google_by_path.values():
                g["CTR (%)"] = round(g["Clics"] / g["Impresiones"] * 100, 2) if g["Impresiones"] else 0
                g["CPC (€)"] = round(g["Gasto (€)"] / g["Clics"], 2) if g["Clics"] else 0
                g["Coste/conv."] = round(g["Gasto (€)"] / g["Conversiones"], 2) if g["Conversiones"] else None
                tema_gasto = g.pop("_tema_gasto")
                g["Tema"] = max(tema_gasto, key=tema_gasto.get) if tema_gasto else None

        def _merge_row(path: str, label: str, fallback_tema: str) -> dict:
            g = google_by_path.get(path, {"Gasto (€)": 0, "Impresiones": 0, "Clics": 0, "CTR (%)": 0, "CPC (€)": 0, "Conversiones": 0, "Coste/conv.": None, "Tema": None})
            row = {"Landing": f"{label} ({path})", "_path": path, "Tema": g.get("Tema") or fallback_tema,
                   **{k: v for k, v in g.items() if k != "Tema"}}
            if ga4_property_id:
                a = ga4_by_path.get(path, {})
                row["Sesiones Google Ads"] = a.get("sesiones_google_ads")
                row["Sesiones Meta/Otros"] = a.get("sesiones_meta", 0) + a.get("sesiones_otros", 0) if a else None
                row["Interacción GA4 (%)"] = a.get("tasa_interaccion")
            return row

        active_landings = get_known_landings()
        known_paths = {p for p, _, _ in active_landings}
        main_rows = [_merge_row(path, label, tema) for path, label, tema in active_landings]
        if sel_tema:
            main_rows = [r for r in main_rows if r["Tema"] == sel_tema]

        total_gasto_lp = sum(r["Gasto (€)"] for r in main_rows)
        total_conv_lp = sum(r["Conversiones"] for r in main_rows)
        cpa_medio_lp = round(total_gasto_lp / total_conv_lp, 2) if total_conv_lp else None

        d_lp_gasto = d_lp_conv = d_lp_cpa = ""
        if comp_since:
            with st.spinner("Cargando comparación de landings…"):
                landing_res_cmp = fetch_google_landing_pages(comp_since, comp_until)
            google_by_path_cmp: dict[str, dict] = {}
            for p in landing_res_cmp.get("pages", []):
                raw_url = p["Landing"] if "://" in p["Landing"] else f"https://{p['Landing']}"
                raw_path = urlparse(raw_url).path or "/"
                path = re.sub(r"\{[^}]*\}", "", raw_path) or "/"
                gc = google_by_path_cmp.setdefault(path, {"Gasto (€)": 0.0, "Conversiones": 0.0})
                gc["Gasto (€)"] += p["Gasto (€)"]; gc["Conversiones"] += p["Conversiones"]
            main_paths_active = {r["_path"] for r in main_rows}
            c_gasto_lp = sum(google_by_path_cmp.get(p, {}).get("Gasto (€)", 0) for p in main_paths_active)
            c_conv_lp = sum(google_by_path_cmp.get(p, {}).get("Conversiones", 0) for p in main_paths_active)
            c_cpa_lp = round(c_gasto_lp / c_conv_lp, 2) if c_conv_lp else None
            d_lp_gasto = kpi_delta(fmt_eur(c_gasto_lp), total_gasto_lp, c_gasto_lp, comparison_mode)
            d_lp_conv = kpi_delta(fmt_num(c_conv_lp), total_conv_lp, c_conv_lp, comparison_mode)
            d_lp_cpa = kpi_delta(fmt_eur(c_cpa_lp), cpa_medio_lp, c_cpa_lp, comparison_mode, invert=True)

        lk1, lk2, lk3, lk4 = st.columns(4)
        lk1.markdown(kpi_card("Landings principales", fmt_num(len(main_rows)), "🔗", accent="#34a853"), unsafe_allow_html=True)
        lk2.markdown(kpi_card("Gasto (Google Ads)", fmt_eur(total_gasto_lp), "💰", accent="#34a853", delta=d_lp_gasto), unsafe_allow_html=True)
        lk3.markdown(kpi_card("Conversiones (Google Ads)", fmt_num(total_conv_lp), "✅", accent="#34a853", delta=d_lp_conv), unsafe_allow_html=True)
        lk4.markdown(kpi_card("Coste/conv. medio", fmt_eur(cpa_medio_lp), "💡", accent="#34a853", delta=d_lp_cpa), unsafe_allow_html=True)
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        render_landings_scorecard(main_rows, show_ga4=bool(ga4_property_id))

        if ga4_error:
            st.markdown(f'<p style="color:#fbbf24;font-size:11.5px;margin-top:8px">⚠ GA4 no disponible: {ga4_error}</p>', unsafe_allow_html=True)
        elif not ga4_property_id:
            st.markdown(
                '<p style="color:#5a6080;font-size:11.5px;margin-top:8px">📊 GA4 pendiente: falta habilitar '
                '<a href="https://console.developers.google.com/apis/api/analyticsadmin.googleapis.com/overview?project=843483082013" target="_blank">Analytics Admin API</a> y '
                '<a href="https://console.developers.google.com/apis/api/analyticsdata.googleapis.com/overview?project=843483082013" target="_blank">Analytics Data API</a> '
                'en Cloud Console, y añadir <code>GA4_PROPERTY_ID_DCORE</code> a <code>.env</code>.</p>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:#5a6080;font-size:11px;margin-top:6px">⚠ "Sesiones Meta/Otros" está aproximado a la baja: '
                'Meta Ads no tiene UTMs en todos los anuncios, así que parte de su tráfico real cae mal clasificado en GA4.</p>',
                unsafe_allow_html=True)

        # Otras páginas con tráfico de Google Ads que no están en la lista de landings
        # principales (nuevas landings sin añadir aún, o páginas normales del sitio).
        other_paths = {p: g for p, g in google_by_path.items() if p not in known_paths}
        if sel_tema:
            other_paths = {p: g for p, g in other_paths.items() if g.get("Tema") == sel_tema}
        if other_paths:
            with st.expander(f"Otras páginas con tráfico de Google Ads ({len(other_paths)})"):
                other_rows = [_merge_row(path, path, TEMA_DEFAULT) for path in sorted(other_paths, key=lambda p: -other_paths[p]["Gasto (€)"])]
                render_landings_scorecard(other_rows, show_ga4=bool(ga4_property_id))

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">🖱️ Salud de landing (Microsoft Clarity)</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:#5a6080;font-size:12px">Una fila por landing, con el recuento de cada señal de fricción. '
            '<b>Rage clicks</b> = algo está roto (arréglalo ya). <b>Quickback clicks</b> = el anuncio promete algo que la landing '
            'no entrega. <b>Dead clicks</b> = confusión de UI, menos urgente.'
            + (' <span style="color:#5a6080">(Este bloque no respeta el filtro de Vertical del sidebar: Clarity mide tráfico '
               'real a la URL, sin dato de campaña/tema asociado.)</span>' if sel_tema else '') + '</p>', unsafe_allow_html=True)

        if not clarity_state.get("configured"):
            st.markdown(
                '<p style="color:#5a6080;font-size:12px">Pendiente de configurar: añade <code>CLARITY_API_TOKEN_DCORE</code> y '
                '<code>CLARITY_PROJECT_ID_DCORE</code> a <code>.env</code> (Clarity → proyecto dcore.es → Settings → Data Export → '
                'Generate new API token).</p>', unsafe_allow_html=True)
        else:
            quota = get_quota_status()
            col_btn, col_device, col_info = st.columns([1.2, 1, 3])
            with col_btn:
                quota_disabled = quota["remaining"] <= 0
                if st.button("🔄 Actualizar Clarity", disabled=quota_disabled,
                             help=f"Quedan {quota['remaining']}/{DAILY_QUOTA} peticiones hoy." if not quota_disabled else "Cuota de hoy agotada, vuelve mañana."):
                    with st.spinner("Consultando Clarity…"):
                        result = refresh_snapshot()
                    if result.get("error"):
                        st.error(result["error"])
                    else:
                        st.success("Instantánea actualizada.")
                        st.rerun()
                st.markdown(f'<div style="color:#5a6080;font-size:10.5px;margin-top:4px">Cuota hoy: {quota["used"]}/{DAILY_QUOTA} usadas</div>', unsafe_allow_html=True)

            if clarity_state.get("cached") and clarity_state.get("rows"):
                devices = ["Todos"] + sorted({r["device"] for r in clarity_state["rows"]})
                with col_device:
                    sel_device = st.selectbox("Dispositivo", devices, key="dcore_clarity_device", label_visibility="collapsed")
                with col_info:
                    st.markdown(f'<div style="color:#5a6080;font-size:11.5px;padding-top:8px">Última instantánea: {clarity_state["fetched_at"]} · últimos {clarity_state["num_days"]} días (sin rango histórico ni por período elegible — limitación de Clarity)</div>', unsafe_allow_html=True)
                pivoted = pivot_clarity_by_landing(clarity_state["rows"], sel_device)
                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                render_clarity_scorecard(pivoted)
                render_csv_download(pivoted, f"dcore_clarity_{time.strftime('%Y%m%d')}.csv", "⬇️ Descargar CSV", "dcore_clarity_csv")
            else:
                with col_info:
                    st.markdown('<div style="color:#5a6080;font-size:11.5px;padding-top:8px">Sin instantánea todavía — pulsa "Actualizar Clarity".</div>', unsafe_allow_html=True)

    with tab_quality:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        if not leads_res.get("configured"):
            st.markdown(
                '<p style="color:#5a6080;font-size:13px">📋 Sheet de leads con código postal aún no configurado. '
                'En cuanto Jordi confirme el ID del Sheet, se añade a <code>.env</code> como '
                '<code>GOOGLE_SHEET_ID_DCORE_LEADS</code> y este bloque se activa automáticamente '
                '(estructura de columnas esperada en <code>tools/sheets_tools.py::fetch_dcore_leads</code>).</p>',
                unsafe_allow_html=True)
        elif leads_res.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:13px">⚠ {leads_res["error"]}</p>', unsafe_allow_html=True)
        else:
            leads = leads_res.get("leads", [])
            cp_counts: dict[str, int] = {}
            for lead in leads:
                cp_counts[lead["cp"]] = cp_counts.get(lead["cp"], 0) + 1
            leads_by_cp = [{"cp": cp, "count": n, "zona": classify_postal_code(cp)}
                           for cp, n in sorted(cp_counts.items(), key=lambda kv: kv[1], reverse=True)]

            zone_totals: dict[str, int] = {}
            for row in leads_by_cp:
                zone_totals[row["zona"]] = zone_totals.get(row["zona"], 0) + row["count"]
            total_leads_cp = sum(zone_totals.values())

            zc1, zc2, zc3 = st.columns(3)
            m30_n = zone_totals.get("Dentro M-30", 0)
            cm_n = zone_totals.get("Fuera M-30 (Madrid/CM)", 0)
            fuera_n = zone_totals.get("Fuera de la Comunidad de Madrid", 0)
            m30_pct = f"{m30_n/total_leads_cp*100:.0f}% del total" if total_leads_cp else "—"
            cm_pct = f"{cm_n/total_leads_cp*100:.0f}% del total" if total_leads_cp else "—"
            fuera_pct = f"{fuera_n/total_leads_cp*100:.0f}% del total" if total_leads_cp else "—"
            zc1.markdown(kpi_card("Dentro M-30", fmt_num(m30_n), "🟢", sub=m30_pct, accent="#4fc870"), unsafe_allow_html=True)
            zc2.markdown(kpi_card("Fuera M-30 (Madrid/CM)", fmt_num(cm_n), "🟡", sub=cm_pct, accent="#fbbf24"), unsafe_allow_html=True)
            zc3.markdown(kpi_card("Fuera de la Comunidad de Madrid", fmt_num(fuera_n), "🔴", sub=fuera_pct, accent="#f87171"), unsafe_allow_html=True)

            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            col_map, col_table = st.columns([3, 2], gap="medium")
            with col_map:
                chart_label("Mapa de leads por código postal (centroide aproximado)")
                st.plotly_chart(chart_leads_map(leads_by_cp), use_container_width=True, config=_NO_INTERACT)
            with col_table:
                chart_label("Leads por código postal")
                render_leads_zone_table(leads_by_cp)


if __name__ == "__main__":
    main()
