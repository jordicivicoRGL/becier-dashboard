"""
Dashboard de Rendimiento — Becier Group
Meta Ads + Google Ads | Streamlit
"""
import os
import sys
import json
from datetime import date, timedelta
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Becier · Dashboard",
    page_icon="🚗",
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
        creds_dir = Path(__file__).parent / "credentials"
        creds_dir.mkdir(exist_ok=True)
        if "GOOGLE_TOKEN_JSON" in secrets:
            (creds_dir / "token.json").write_text(secrets["GOOGLE_TOKEN_JSON"])
        if "GOOGLE_CLIENT_SECRET_JSON" in secrets:
            (creds_dir / "client_secret.json").write_text(secrets["GOOGLE_CLIENT_SECRET_JSON"])
    except Exception:
        pass

_setup_credentials()
sys.path.insert(0, str(Path(__file__).parent))

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Base */
[data-testid="stAppViewContainer"] { background-color: #0d0f18; }
[data-testid="stHeader"] { background-color: #0d0f18; border-bottom: 1px solid #1a1e35; }
section[data-testid="stSidebar"] { background-color: #0b0d16; border-right: 1px solid #1a1e35; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

/* ── KPI cards ────────────────────────────────────────────────────────────── */
.kpi-card {
    background: #12152a;
    border: 1px solid #1e2440;
    border-radius: 10px;
    padding: 16px 18px 14px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2e3560; }
.kpi-icon { font-size: 16px; margin-bottom: 6px; display: block; }
.kpi-label {
    color: #5a6080;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    margin-bottom: 6px;
}
.kpi-value {
    color: #eef0ff;
    font-size: 24px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.5px;
}
.kpi-sub { color: #444c70; font-size: 10.5px; margin-top: 5px; }

/* ── Platform containers ──────────────────────────────────────────────────── */
.platform-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 14px;
}
.ph-meta { background: rgba(74,127,255,0.08); border: 1px solid rgba(74,127,255,0.2); }
.ph-google { background: rgba(52,168,83,0.08); border: 1px solid rgba(52,168,83,0.2); }
.ph-combined { background: rgba(168,85,247,0.08); border: 1px solid rgba(168,85,247,0.2); }
.ph-icon { font-size: 18px; }
.ph-title { font-size: 13px; font-weight: 700; letter-spacing: 0.3px; }
.ph-meta .ph-title { color: #6a9fff; }
.ph-google .ph-title { color: #4fc870; }
.ph-combined .ph-title { color: #c084fc; }
.ph-sub { font-size: 11px; color: #444c70; margin-left: auto; }

/* ── Alerts ───────────────────────────────────────────────────────────────── */
.alert-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0 20px;
}
.alert-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
}
.alert-warn { background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.3); color: #fbbf24; }
.alert-danger { background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.3); color: #f87171; }
.alert-ok { background: rgba(52,168,83,0.12); border: 1px solid rgba(52,168,83,0.3); color: #4fc870; }

/* ── Header principal ─────────────────────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, #12152a 0%, #0d0f18 100%);
    border: 1px solid #1e2440;
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}
.dash-logo { font-size: 28px; font-weight: 900; letter-spacing: -1px; color: #eef0ff; }
.dash-logo span { color: #4a7fff; }
.dash-subtitle { color: #444c70; font-size: 12px; margin-top: 3px; }
.dash-right { display: flex; align-items: center; gap: 20px; }
.dash-total-label { color: #444c70; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; }
.dash-total-value { color: #eef0ff; font-size: 36px; font-weight: 800; letter-spacing: -1px; line-height: 1; }
.dash-total-sub { color: #4a7fff; font-size: 12px; margin-top: 4px; }
.dash-period {
    background: #1a1e35;
    border: 1px solid #252a48;
    border-radius: 8px;
    padding: 12px 20px;
    color: #6a7aaa;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
}

/* ── Divider ──────────────────────────────────────────────────────────────── */
.divider { border: none; border-top: 1px solid #1a1e35; margin: 22px 0; }

/* ── Tables ───────────────────────────────────────────────────────────────── */
.styled-table-wrap { overflow-x: auto; border-radius: 8px; border: 1px solid #1e2440; }
table.styled-table { width: 100%; border-collapse: collapse; font-size: 12.5px; color: #b0b8d8; }
table.styled-table th {
    background: #0f1220;
    color: #444c70;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    padding: 11px 14px;
    text-align: left;
    border-bottom: 1px solid #1e2440;
    white-space: nowrap;
}
table.styled-table td { padding: 10px 14px; border-bottom: 1px solid #161930; }
table.styled-table tr:last-child td { border-bottom: none; }
table.styled-table tr:hover td { background: #12152a; }
table.styled-table .num { text-align: right; font-variant-numeric: tabular-nums; }
.ctr-low { color: #f87171; font-weight: 600; }
.ctr-high { color: #4fc870; font-weight: 600; }
.freq-high { color: #fbbf24; font-weight: 600; }
.tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.4px;
    white-space: nowrap;
}
.tag-vehicles { background: rgba(234,179,8,0.15);   color: #f0c030; }
.tag-becar    { background: rgba(239,68,68,0.15);   color: #f87171; }
.tag-becser   { background: rgba(34,197,94,0.15);   color: #22c55e; }
.tag-grup     { background: rgba(249,115,22,0.15);  color: #f97316; }
.tag-other    { background: rgba(100,100,100,0.15); color: #888; }
.tag-lead     { background: rgba(52,168,83,0.15);  color: #4fc870; }
.tag-landing  { background: rgba(168,85,247,0.15); color: #c084fc; }
.tag-reach    { background: rgba(251,191,36,0.15); color: #fbbf24; }

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
.sidebar-kpi { margin-bottom: 14px; }
.sidebar-kpi-label { color: #444c70; font-size: 10px; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 700; }
.sidebar-kpi-value { color: #eef0ff; font-size: 20px; font-weight: 800; margin-top: 2px; }
.sidebar-platform-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1e2440; gap: 0; }
[data-baseweb="tab"] { color: #444c70 !important; font-weight: 600 !important; font-size: 13px !important; padding: 10px 20px !important; }
[aria-selected="true"] { color: #eef0ff !important; border-bottom: 2px solid #4a7fff !important; }
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

def month_label(since: str) -> str:
    months_es = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    d = date.fromisoformat(since)
    return f"{months_es[d.month]} {d.year}"


# ─── PARSEO DE NOMBRE DE CAMPAÑA ─────────────────────────────────────────────
# Formato: AND_PROS_[VERTICAL]_[OBJETIVO]
_VERTICAL_MAP = {
    "VEHICLES": "Vehicles",
    "VO":       "Vehicles",   # Vehicles-Pla-Engega → amarillo
    "BECAR":    "Becar",
    "AVIS":     "Becar",      # AVIS-BECAR → turquesa
    "BECSER":   "Becser",
    "GRUP":     "Grup Becier",
    "BECIER":   "Grup Becier",
    "OKSIO":    "Oksio",
}
_OBJETIVO_MAP = {
    "LEAD AD":   "Lead Ad",
    "LEAD":      "Lead Ad",
    "LE":        "Landing",
    "TRAFIC WEB":"Landing",
    "TRAFIC":    "Landing",
    "TRAFFIC":   "Landing",
    "ALCANCE":   "Impresiones",
    "REACH":     "Impresiones",
}

def parse_campaign_parts(name: str) -> dict:
    """Extrae Vertical y Objetivo del nombre AND_PROS_[VERTICAL]_[OBJETIVO]."""
    parts = [p.strip() for p in name.split("_")]
    vertical = "Otros"
    objetivo = "—"
    if len(parts) >= 3:
        v = parts[2].upper()
        vertical = _VERTICAL_MAP.get(v, parts[2].title())
    if len(parts) >= 4:
        objetivo = None
        for end in range(len(parts), 3, -1):
            candidate = " ".join(parts[3:end]).upper()
            if candidate in _OBJETIVO_MAP:
                objetivo = _OBJETIVO_MAP[candidate]
                break
        if objetivo is None:
            objetivo = parts[3].title()
    return {"vertical": vertical, "objetivo": objetivo}

VERTICAL_STYLES = {
    "Vehicles":    "tag-vehicles",
    "Becar":       "tag-becar",
    "Becser":      "tag-becser",
    "Oksio":       "tag-grup",
    "Grup Becier": "tag-grup",
    "Otros":       "tag-other",
}
OBJETIVO_STYLES = {
    "Lead Ad":     "tag-lead",
    "Landing":     "tag-landing",
    "Impresiones": "tag-reach",
}


# ─── META ADS FETCH ───────────────────────────────────────────────────────────
META_BASE = "https://graph.facebook.com/v21.0"

def _meta_account_id() -> str:
    aid = os.environ.get("META_AD_ACCOUNT_ID_BECIER", "act_353629399")
    return aid if aid.startswith("act_") else f"act_{aid}"

def _meta_token() -> str:
    return os.environ.get("META_ACCESS_TOKEN", "")

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_summary(since: str, until: str) -> dict:
    params = {
        "access_token": _meta_token(),
        "fields": "spend,impressions,reach,clicks,cpm,cpc,ctr,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "account",
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}
        rows = data.get("data", [])
        if not rows:
            return {"error": "Sin datos para el período"}
        i = rows[0]
        actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
        result_types = [
            ("lead", "Leads"),
            ("offsite_conversion.fb_pixel_lead", "Leads (pixel)"),
            ("link_click", "Clics enlace"),
            ("landing_page_view", "Visitas landing"),
        ]
        results, result_label = 0, "Resultados"
        for rt, label in result_types:
            if actions.get(rt, 0) > 0:
                results = actions[rt]
                result_label = label
                break
        spend = float(i.get("spend", 0))
        return {
            "spend_eur": spend,
            "impressions": int(i.get("impressions", 0)),
            "reach": int(i.get("reach", 0)),
            "clicks": int(i.get("clicks", 0)),
            "cpm": float(i.get("cpm", 0)),
            "cpc": float(i.get("cpc", 0)),
            "ctr_pct": float(i.get("ctr", 0)),
            "frequency": float(i.get("frequency", 0)),
            "results": int(results),
            "result_label": result_label,
            "cost_per_result": round(spend / results, 2) if results > 0 else None,
        }
    except Exception as e:
        return {"error": str(e)}

_OPT_GOAL_TO_ACTION = {
    "LINK_CLICKS":           "link_click",
    "CLICKS":                "link_click",
    "LANDING_PAGE_VIEWS":    "landing_page_view",
    "CONTENT_VIEWS":         "offsite_conversion.fb_pixel_view_content",
    "LEAD_GENERATION":       "lead",
    "QUALITY_LEAD":          "lead",
    "REACH":                 None,
    "IMPRESSIONS":           None,
    "AD_RECALL_LIFT":        None,
    "VIDEO_VIEWS":           "video_view",
    "THRUPLAY":              "video_view",
    "POST_ENGAGEMENT":       "post_engagement",
    "PAGE_LIKES":            "like",
    "CONVERSATIONS":         "onsite_conversion.messaging_conversation_started_7d",
    "OFFSITE_CONVERSIONS":   "__pixel__",
    "PROFILE_VISIT":         None,
    "VISIT_INSTAGRAM_PROFILE": None,
    "NONE":                  None,
}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_adset_goals() -> dict:
    """Devuelve {campaign_id: {"goal": str, "event": str}} con optimization_goal y promoted_object."""
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
            aid = adset.get("id")
            cid = adset.get("campaign_id")
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
    "CONTENT_VIEW":          "offsite_conversion.fb_pixel_view_content",
    "VIEW_CONTENT":          "offsite_conversion.fb_pixel_view_content",
    "LEAD":                  "offsite_conversion.fb_pixel_lead",
    "PURCHASE":              "offsite_conversion.fb_pixel_purchase",
    "COMPLETE_REGISTRATION": "offsite_conversion.fb_pixel_complete_registration",
    "ADD_TO_CART":           "offsite_conversion.fb_pixel_add_to_cart",
    "SEARCH":                "offsite_conversion.fb_pixel_search",
    "INITIATED_CHECKOUT":    "offsite_conversion.fb_pixel_initiate_checkout",
}

_ACTION_LABELS = {
    "link_click":                                    "Clics enlace",
    "landing_page_view":                             "Visitas landing",
    "offsite_conversion.fb_pixel_view_content":      "Vis. contenido",
    "offsite_conversion.fb_pixel_lead":              "Leads",
    "offsite_conversion.fb_pixel_purchase":          "Compras",
    "offsite_conversion.fb_pixel_complete_registration": "Registros",
    "lead":                                          "Leads",
    "video_view":                                    "Reprod. vídeo",
    "post_engagement":                               "Interacciones",
}

def _result_from_actions(actions: dict, goal_info: dict,
                         reach: int, impressions: int) -> tuple[int, str]:
    """Devuelve (valor, label) usando optimization_goal + promoted_object del adset."""
    goal  = goal_info.get("goal", "")
    event = goal_info.get("event", "")

    if goal == "REACH":       return reach, "Alcance"
    if goal == "IMPRESSIONS": return impressions, "Impresiones"

    if goal == "OFFSITE_CONVERSIONS":
        # Usar el evento pixel exacto del promoted_object
        action_key = _EVENT_TO_ACTION.get(event)
        if action_key:
            return int(actions.get(action_key, 0)), _ACTION_LABELS.get(action_key, "Conversión")
        # Fallback: pixel event con mayor valor
        pixel = {k: v for k, v in actions.items()
                 if k.startswith("offsite_conversion.fb_pixel") and v > 0}
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
        "fields": "campaign_id,campaign_name,spend,impressions,reach,cpm,cost_per_inline_link_click,inline_link_click_ctr,inline_link_clicks,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "campaign",
        "limit": 200,
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
            parts = parse_campaign_parts(name)
            objetivo = parts["objetivo"]
            cid = i.get("campaign_id", "")
            goal_info = adset_goals.get(cid, {"goal": "", "event": ""})
            result_val, result_key = _result_from_actions(
                actions, goal_info,
                reach=int(i.get("reach", 0)),
                impressions=int(i.get("impressions", 0)),
            )
            campaigns.append({
                "_campaign_id":    cid,
                "Campaña":         name,
                "Vertical":        parts["vertical"],
                "Objetivo":        objetivo,
                "Gasto (€)":       spend,
                "Impresiones":     int(i.get("impressions", 0)),
                "Alcance":         int(i.get("reach", 0)),
                "CPM":             float(i.get("cpm", 0)),
                "CTR (%)":         float(i.get("inline_link_click_ctr", 0)),
                "Clics enlace":    int(i.get("inline_link_clicks", 0)),
                "CPC":             float(i.get("cost_per_inline_link_click", 0) or 0),
                "Frecuencia":      float(i.get("frequency", 0)),
                "Resultado":       int(result_val),
                "Resultado Key":   result_key,
                "Coste/Resultado": round(spend / result_val, 2) if result_val > 0 else None,
            })
        campaigns.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return campaigns
    except Exception:
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_daily(since: str, until: str) -> list:
    params = {
        "access_token": _meta_token(),
        "fields": "spend,date_start",
        "time_range": json.dumps({"since": since, "until": until}),
        "time_increment": 1,
        "level": "account",
        "limit": 100,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights", params=params, timeout=20)
        data = r.json()
        return [{"date": row["date_start"], "spend": float(row.get("spend", 0))}
                for row in data.get("data", [])]
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_adsets_detail(since: str, until: str) -> list:
    """Insights por adset — mismas métricas que por campaña + nombre del adset."""
    params = {
        "access_token": _meta_token(),
        "fields": "adset_id,adset_name,campaign_id,campaign_name,spend,impressions,reach,"
                  "cpm,cost_per_inline_link_click,inline_link_click_ctr,inline_link_clicks,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "adset",
        "limit": 500,
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
            spend   = float(i.get("spend", 0))
            aid     = i.get("adset_id", "")
            cid     = i.get("campaign_id", "")
            name    = i.get("campaign_name", "")
            parts   = parse_campaign_parts(name)
            goal_info = adset_goals.get(aid) or adset_goals.get(cid, {"goal":"","event":""})
            result_val, _ = _result_from_actions(
                actions, goal_info,
                reach=int(i.get("reach", 0)),
                impressions=int(i.get("impressions", 0)),
            )
            link_clicks = int(i.get("inline_link_clicks", 0))
            rows.append({
                "_adset_id":       i.get("adset_id", ""),
                "Campaña":         name,
                "Adset":           i.get("adset_name", ""),
                "Vertical":        parts["vertical"],
                "Objetivo":        parts["objetivo"],
                "Gasto (€)":       spend,
                "Impresiones":     int(i.get("impressions", 0)),
                "Alcance":         int(i.get("reach", 0)),
                "CPM":             float(i.get("cpm", 0)),
                "CPC":             float(i.get("cost_per_inline_link_click", 0) or 0),
                "CTR (%)":         float(i.get("inline_link_click_ctr", 0)),
                "Clics enlace":    link_clicks,
                "Frecuencia":      float(i.get("frequency", 0)),
                "Resultado":       int(result_val),
                "Coste/Resultado": round(spend / result_val, 2) if result_val > 0 else None,
            })
        rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
        return rows
    except Exception:
        return []

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
                   metrics.conversions, metrics.ctr, metrics.average_cpc,
                   metrics.average_cpm
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
              AND metrics.impressions > 0
            ORDER BY metrics.cost_micros DESC
        """
        response = ga_service.search(customer_id="1632468817", query=query)
        campaigns = []
        for row in response:
            name  = row.campaign.name
            parts = parse_campaign_parts(name)
            cost  = round(row.metrics.cost_micros / 1_000_000, 2)
            conv  = round(row.metrics.conversions, 1)
            campaigns.append({
                "Campaña":      name,
                "Vertical":     parts["vertical"],
                "Objetivo":     parts["objetivo"],
                "Gasto (€)":    cost,
                "Impresiones":  row.metrics.impressions,
                "CPM (€)":      round(row.metrics.average_cpm / 1_000_000, 2),
                "CPC (€)":      round(row.metrics.average_cpc / 1_000_000, 2),
                "Clics":        row.metrics.clicks,
                "CTR (%)":      round(row.metrics.ctr * 100, 2),
                "Conversiones": conv,
                "Coste/conv.":  round(cost / conv, 2) if conv > 0 else None,
            })
        return {"campaigns": campaigns}
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_meta_ads_for_adset(adset_id: str, since: str, until: str) -> list:
    """Insights + creatives a nivel de anuncio para el adset seleccionado."""
    token = _meta_token()

    # 1. Insights por anuncio
    ins_params = {
        "access_token": token,
        "fields": "ad_id,ad_name,spend,impressions,reach,cpm,"
                  "cost_per_inline_link_click,inline_link_click_ctr,"
                  "inline_link_clicks,frequency,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "ad",
        "filtering": json.dumps([{"field":"adset.id","operator":"EQUAL","value": adset_id}]),
        "limit": 200,
    }
    try:
        r = requests.get(f"{META_BASE}/{_meta_account_id()}/insights",
                         params=ins_params, timeout=20)
        insights_raw = r.json().get("data", [])
    except Exception:
        return []

    if not insights_raw:
        return []

    # Mapa ad_id → métricas
    ins_map = {}
    for i in insights_raw:
        actions = {a["action_type"]: float(a["value"]) for a in i.get("actions", [])}
        spend = float(i.get("spend", 0))
        link_clicks = int(i.get("inline_link_clicks", 0))
        ins_map[i["ad_id"]] = {
            "spend": spend,
            "impressions": int(i.get("impressions", 0)),
            "reach": int(i.get("reach", 0)),
            "cpm": float(i.get("cpm", 0)),
            "cpc": float(i.get("cost_per_inline_link_click", 0) or 0),
            "ctr": float(i.get("inline_link_click_ctr", 0)),
            "clics": link_clicks,
            "frequency": float(i.get("frequency", 0)),
            "actions": actions,
        }

    # 2. Creatives de los anuncios del adset
    ads_params = {
        "access_token": token,
        "fields": "id,name,effective_status,creative{id,name,image_url,thumbnail_url,"
                  "video_id,object_type,image_hash}",
        "limit": 200,
    }
    try:
        r2 = requests.get(f"{META_BASE}/{adset_id}/ads", params=ads_params, timeout=20)
        ads_raw = r2.json().get("data", [])
    except Exception:
        ads_raw = []

    adset_goals = fetch_meta_adset_goals()
    goal_info   = adset_goals.get(adset_id, {"goal":"","event":""})

    rows = []
    for ad in ads_raw:
        aid     = ad.get("id","")
        metrics = ins_map.get(aid, {})
        if not metrics:
            continue
        creative  = ad.get("creative") or {}
        img_url   = creative.get("image_url","")
        thumb_url = creative.get("thumbnail_url","")
        obj_type  = creative.get("object_type","")
        is_video  = bool(creative.get("video_id")) or obj_type in ("VIDEO","SHARE")
        preview_url = thumb_url if is_video else img_url

        result_val, _ = _result_from_actions(
            metrics.get("actions",{}), goal_info,
            reach=metrics.get("reach",0),
            impressions=metrics.get("impressions",0),
        )
        spend = metrics.get("spend", 0)
        rows.append({
            "ad_id":           aid,
            "Anuncio":         ad.get("name",""),
            "Estado":          ad.get("effective_status",""),
            "preview_url":     preview_url,
            "is_video":        is_video,
            "Gasto (€)":       spend,
            "Impresiones":     metrics.get("impressions",0),
            "Alcance":         metrics.get("reach",0),
            "CPM":             metrics.get("cpm",0),
            "CPC":             metrics.get("cpc",0),
            "CTR (%)":         metrics.get("ctr",0),
            "Clics":           metrics.get("clics",0),
            "Frecuencia":      metrics.get("frequency",0),
            "Resultado":       int(result_val),
            "CPR":             round(spend / result_val, 2) if result_val > 0 else None,
        })
    rows.sort(key=lambda x: x["Gasto (€)"], reverse=True)
    return rows

_KW_QUALITY = {"ABOVE_AVERAGE":"✅ Por encima","AVERAGE":"🟡 Promedio",
               "BELOW_AVERAGE":"🔴 Por debajo","UNKNOWN":"—"}

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
        response = ga_svc.search(customer_id="1632468817", query=query)
        MATCH = {"EXACT":"[Exacta]","PHRASE":'"Frase"',"BROAD":"Amplia"}

        def pct(v):
            return f"{v*100:.1f}%" if v and v > 0 else "—"

        keywords = []
        for row in response:
            crit  = row.ad_group_criterion
            m     = row.metrics
            cost  = round(m.cost_micros / 1_000_000, 2)
            conv  = round(m.conversions, 1)
            clics = m.clicks
            urls  = list(crit.final_urls) if crit.final_urls else []
            keywords.append({
                "Keyword":          crit.keyword.text,
                "Concordancia":     MATCH.get(crit.keyword.match_type.name, "—"),
                "Campaña":          row.campaign.name,
                "Vertical":         parse_campaign_parts(row.campaign.name)["vertical"],
                "Coste":            cost,
                "CTR (%)":          round(m.ctr * 100, 2),
                "CPC medio":        round(m.average_cpc / 1_000_000, 2),
                "Conversiones":     conv,
                "Coste/conv.":      round(cost / conv, 2) if conv > 0 else None,
                "Tasa conv. (%)":   round(conv / clics * 100, 2) if clics > 0 else 0,
                "Cuota impr. (%)":  pct(m.search_impression_share),
                "Cuota perd. ranking": pct(m.search_rank_lost_impression_share),
                "Cuota clics (%)":  pct(m.search_click_share),
                "Nivel calidad":    crit.quality_info.quality_score or "—",
                "URL final":        urls[0] if urls else "—",
                "CTR esperado":     _KW_QUALITY.get(crit.quality_info.search_predicted_ctr.name, "—"),
                "Exp. landing":     _KW_QUALITY.get(crit.quality_info.post_click_quality_score.name, "—"),
                "Relevancia anuncio": _KW_QUALITY.get(crit.quality_info.creative_quality_score.name, "—"),
            })
        return {"keywords": keywords}
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_daily(since: str, until: str) -> list:
    try:
        from tools.ads_tools import _build_client
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT segments.date, metrics.cost_micros
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
            ORDER BY segments.date
        """
        response = ga_service.search(customer_id="1632468817", query=query)
        daily: dict[str, float] = {}
        for row in response:
            d = row.segments.date
            daily[d] = daily.get(d, 0) + row.metrics.cost_micros / 1_000_000
        return [{"date": k, "spend": round(v, 2)} for k, v in sorted(daily.items())]
    except Exception:
        return []


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


# ─── COMPONENTES UI ───────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, icon: str = "", sub: str = "",
             accent: str = "#1e2440") -> str:
    icon_html = f'<span class="kpi-icon">{icon}</span>' if icon else ""
    sub_html  = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi-card" style="border-top:2px solid {accent}">'
            f'{icon_html}<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{sub_html}</div>')

def platform_header(title: str, subtitle: str, platform: str) -> str:
    icons = {"meta": "📘", "google": "📗", "combined": "📊"}
    cls   = {"meta": "ph-meta", "google": "ph-google", "combined": "ph-combined"}
    i = icons.get(platform, "")
    c = cls.get(platform, "")
    return (f'<div class="platform-header {c}">'
            f'<span class="ph-icon">{i}</span>'
            f'<span class="ph-title">{title}</span>'
            f'<span class="ph-sub">{subtitle}</span></div>')

def render_alerts(meta: dict, google_camps: list):
    alerts = []
    if not meta.get("error"):
        freq = meta.get("frequency", 0)
        ctr  = meta.get("ctr_pct", 99)
        if freq > 3.0:
            alerts.append(("warn", f"⚠️ Frecuencia Meta: {freq:.2f} — riesgo de saturación de audiencia"))
        if ctr < 0.8:
            alerts.append(("danger", f"🔴 CTR Meta: {ctr:.2f}% — bajo umbral mínimo (0,80%)"))
        if ctr >= 2.0:
            alerts.append(("ok", f"✅ CTR Meta: {ctr:.2f}% — buen rendimiento de creatividades"))

    if google_camps:
        total_imp = sum(c["Impresiones"] for c in google_camps)
        total_cli = sum(c["Clics"] for c in google_camps)
        g_ctr = (total_cli / total_imp * 100) if total_imp else 0
        if g_ctr < 1.0:
            alerts.append(("danger", f"🔴 CTR Google: {g_ctr:.2f}% — revisar keywords y anuncios"))
        elif g_ctr > 5.0:
            alerts.append(("ok", f"✅ CTR Google: {g_ctr:.2f}% — excelente rendimiento"))

    if not alerts:
        return

    badges = "".join(f'<span class="alert-badge alert-{level}">{msg}</span>' for level, msg in alerts)
    st.markdown(f'<div class="alert-strip">{badges}</div>', unsafe_allow_html=True)


# ─── GRÁFICOS ─────────────────────────────────────────────────────────────────
_CHART_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="#12152a",
    plot_bgcolor="#12152a",
    font=dict(family="sans-serif", color="#6a7aaa"),
    hoverlabel=dict(bgcolor="#12152a", bordercolor="#2e3560", font_color="#eef0ff"),
)

_NO_INTERACT = {"displayModeBar": False, "scrollZoom": False,
                "doubleClick": False, "showTips": False}
_LEGEND_STATIC = dict(itemclick=False, itemdoubleclick=False,
                      bgcolor="rgba(0,0,0,0)", font=dict(size=12, color="#b0b8d8"))
COLOR_VERT = {"Vehicles":"#f0c030","Becar":"#f87171","Becser":"#22c55e",
              "Oksio":"#f97316","Grup Becier":"#f97316","Otros":"#555"}


def chart_inversion_semanal(meta_daily: list, google_daily: list) -> go.Figure:
    """Barras agrupadas: inversión semanal Meta + Google."""
    def to_weekly(dl, label):
        if not dl:
            return pd.DataFrame(columns=["week","spend"])
        df = pd.DataFrame(dl)
        df["date"] = pd.to_datetime(df["date"])
        df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time.strftime("%d %b"))
        return df.groupby("week")["spend"].sum().reset_index()

    meta_w   = to_weekly(meta_daily, "Meta")
    google_w = to_weekly(google_daily, "Google")
    weeks    = sorted(set(list(meta_w["week"]) + list(google_w["week"])))

    meta_idx   = meta_w.set_index("week")["spend"]
    google_idx = google_w.set_index("week")["spend"]
    meta_vals   = [meta_idx.get(w, 0) for w in weeks]
    google_vals = [google_idx.get(w, 0) for w in weeks]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=weeks, y=meta_vals, name="Meta Ads", marker_color="#4a7fff",
                         hovertemplate="<b>Meta</b>: %{y:,.2f} €<extra></extra>"))
    fig.add_trace(go.Bar(x=weeks, y=google_vals, name="Google Ads", marker_color="#34a853",
                         hovertemplate="<b>Google</b>: %{y:,.2f} €<extra></extra>"))
    fig.update_layout(
        **_CHART_BASE, barmode="group", height=300, margin=dict(l=4,r=4,t=10,b=4),
        hovermode="x unified",
        legend=dict(**_LEGEND_STATIC, orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
        xaxis=dict(gridcolor="#1a1e35", showgrid=False),
        yaxis=dict(gridcolor="#1a1e35", ticksuffix=" €", showgrid=True),
        bargap=0.25, bargroupgap=0.08,
    )
    return fig


def chart_desglose_vertical(meta_camps: list, google_camps: list) -> go.Figure:
    """Dona: presupuesto total por vertical (Meta + Google combinados)."""
    spend: dict[str, float] = {}
    for c in meta_camps:
        v = c.get("Vertical","Otros")
        spend[v] = spend.get(v, 0) + c.get("Gasto (€)", 0)
    for c in google_camps:
        v = c.get("Vertical","Otros")
        spend[v] = spend.get(v, 0) + c.get("Gasto (€)", 0)

    labels = [v for v, s in spend.items() if s > 0]
    values = [spend[v] for v in labels]
    colors = [COLOR_VERT.get(v, "#555") for v in labels]
    total  = sum(values)

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color="#12152a", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color="#eef0ff"),
        hovertemplate="<b>%{label}</b><br>%{value:,.2f} €  (%{percent})<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{fmt_eur(total)}</b><br>Total",
                       x=0.5, y=0.5, showarrow=False,
                       font=dict(size=13, color="#eef0ff"), xanchor="center", align="center")
    fig.update_layout(
        **_CHART_BASE, height=300, margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
    )
    return fig


def chart_cpr_por_vertical_canal(meta_camps: list, google_camps: list) -> go.Figure:
    """Barras agrupadas: CPL/CPR por vertical y canal (Meta vs Google)."""
    # Meta: agrupar Lead Ad + Landing por vertical
    meta_v: dict[str, dict] = {}
    for c in meta_camps:
        v   = c.get("Vertical", "Otros")
        obj = c.get("Objetivo", "")
        if obj not in ("Lead Ad", "Landing"):
            continue
        if v not in meta_v:
            meta_v[v] = {"spend": 0, "results": 0}
        meta_v[v]["spend"]   += c.get("Gasto (€)", 0)
        meta_v[v]["results"] += c.get("Resultado", 0)

    # Google: coste/conversión por vertical
    google_v: dict[str, dict] = {}
    for c in google_camps:
        v = c.get("Vertical", "Otros")
        if v not in google_v:
            google_v[v] = {"spend": 0, "conversions": 0}
        google_v[v]["spend"]       += c.get("Gasto (€)", 0)
        google_v[v]["conversions"] += c.get("Conversiones", 0)

    # Unir verticales y calcular CPR/CPL
    all_verts = sorted(set(list(meta_v.keys()) + list(google_v.keys())))
    meta_cpls  = []
    google_cpcs = []
    valid_verts = []

    for v in all_verts:
        m = meta_v.get(v, {"spend":0,"results":0})
        g = google_v.get(v, {"spend":0,"conversions":0})
        meta_cpl    = round(m["spend"] / m["results"], 2)     if m["results"] > 0    else None
        google_cpc  = round(g["spend"] / g["conversions"], 2) if g["conversions"] > 0 else None
        if meta_cpl is None and google_cpc is None:
            continue
        valid_verts.append(v)
        meta_cpls.append(meta_cpl)
        google_cpcs.append(google_cpc)

    if not valid_verts:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Meta Ads", y=valid_verts,
        x=[v if v is not None else 0 for v in meta_cpls],
        orientation="h", marker_color="#4a7fff",
        text=[fmt_eur(v) if v is not None else "—" for v in meta_cpls],
        textposition="outside", textfont=dict(size=11, color="#8898cc"),
        hovertemplate="<b>Meta · %{y}</b>: %{x:,.2f} €<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Google Ads", y=valid_verts,
        x=[v if v is not None else 0 for v in google_cpcs],
        orientation="h", marker_color="#34a853",
        text=[fmt_eur(v) if v is not None else "—" for v in google_cpcs],
        textposition="outside", textfont=dict(size=11, color="#8898cc"),
        hovertemplate="<b>Google · %{y}</b>: %{x:,.2f} €<extra></extra>",
    ))
    fig.update_layout(
        **_CHART_BASE, barmode="group", height=300, margin=dict(l=4,r=90,t=10,b=4),
        legend=dict(**_LEGEND_STATIC, orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
        xaxis=dict(gridcolor="#1a1e35", ticksuffix=" €", showgrid=True,
                   title=dict(text="Coste por resultado", font=dict(size=11, color="#5a6080"))),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    return fig


META_TIPS = {
    "Importe gastado": "Importe total invertido en el período",
    "Impresiones":     "Número total de veces que se mostró el anuncio",
    "Alcance":         "Personas únicas que vieron el anuncio al menos una vez",
    "CPM":             "Coste por cada 1.000 impresiones",
    "CPC":             "Coste medio por clic en el enlace del anuncio",
    "CTR":             "% de personas que hicieron clic tras ver el anuncio",
    "Clics":           "Clics en el enlace del anuncio (inline link clicks)",
    "Resultados":      "Resultado principal según el objetivo de la campaña",
    "CPR":             "Coste medio por resultado conseguido",
    "Frecuencia":      "Número medio de veces que cada persona vio el anuncio. >3 indica riesgo de saturación",
}

# ─── TABLA SORTABLE (iframe con JS) ──────────────────────────────────────────
_TABLE_CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0f18;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:2px 0;overflow-y:hidden;overflow-x:hidden}
.wrap{overflow-x:auto;border-radius:8px;border:1px solid #1e2440}
table{width:100%;border-collapse:collapse;font-size:12.5px;color:#b0b8d8}
td{white-space:nowrap}
.num{white-space:nowrap}
thead{position:sticky;top:0;z-index:1}
th{background:#0f1220;color:#444c70;font-size:10.5px;font-weight:700;text-transform:uppercase;
   letter-spacing:.7px;padding:11px 14px;text-align:center;border-bottom:1px solid #1e2440;
   white-space:nowrap;cursor:pointer;user-select:none;transition:color .15s}
th:hover{color:#8898cc}
th.asc::after{content:" ▲";color:#4a7fff;font-size:9px}
th.desc::after{content:" ▼";color:#4a7fff;font-size:9px}
th.num-h{text-align:center}
td{padding:10px 14px;border-bottom:1px solid #161930;text-align:center}
tr:last-child td{border-bottom:none}
tr:hover td{background:#12152a}
.num{text-align:center;font-variant-numeric:tabular-nums}
.tag{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;letter-spacing:.4px;white-space:nowrap}
.tv{background:rgba(234,179,8,.15);  color:#f0c030}
.tb{background:rgba(239,68,68,.15);  color:#f87171}
.ts{background:rgba(34,197,94,.15);  color:#22c55e}
.tg{background:rgba(249,115,22,.15); color:#f97316}
.to{background:rgba(100,100,100,.15);color:#888}
.tl{background:rgba(52,168,83,.15);color:#4fc870}
.tp{background:rgba(168,85,247,.15);color:#c084fc}
.tr{background:rgba(251,191,36,.15);color:#fbbf24}
.ctr-low{color:#f87171;font-weight:600}
.ctr-hi{color:#4fc870;font-weight:600}
.freq-hi{color:#fbbf24;font-weight:600}
tr.sec-hdr td{background:#161d32;color:#5a6898;font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:.8px;padding:12px 14px 8px;
  border-top:2px solid #1e2440;border-bottom:1px solid #1e2440;
  text-align:left !important}
tr.sec-hdr:first-child td{border-top:none}
tr.total-row td{background:#0f1628;color:#eef0ff;font-weight:700;font-size:12.5px;
  border-top:2px solid #2e3560;white-space:nowrap}
th{position:relative}
th[data-tip]:hover::after{content:attr(data-tip);position:absolute;top:calc(100% + 6px);
  left:50%;transform:translateX(-50%);background:#1c2040;color:#c8d0f0;
  padding:7px 12px;border-radius:7px;font-size:11px;font-weight:400;
  text-transform:none;letter-spacing:0;white-space:normal;max-width:220px;
  z-index:999;border:1px solid #2e3a60;pointer-events:none;
  box-shadow:0 6px 16px rgba(0,0,0,.5);line-height:1.5;text-align:left}
</style>"""

_TABLE_JS = """
<script>
function sortTable(idx,th){
  const tb=document.querySelector('tbody');
  if(!tb) return;
  const allRows=Array.from(tb.children);
  const asc=th.classList.contains('asc');
  document.querySelectorAll('th').forEach(h=>h.classList.remove('asc','desc'));

  const cmp=(a,b)=>{
    const ac=a.cells[idx]; const bc=b.cells[idx];
    if(!ac||!bc) return 0;
    const av=ac.dataset.v!==undefined?ac.dataset.v:ac.textContent.trim();
    const bv=bc.dataset.v!==undefined?bc.dataset.v:bc.textContent.trim();
    const an=parseFloat(String(av).replace(/[^\d.-]/g,''));
    const bn=parseFloat(String(bv).replace(/[^\d.-]/g,''));
    if(!isNaN(an)&&!isNaN(bn)) return asc?bn-an:an-bn;
    return asc?String(bv).localeCompare(String(av),'es'):String(av).localeCompare(String(bv),'es');
  };

  const hasSec=allRows.some(r=>r.dataset.sec);
  if(!hasSec){
    allRows.sort(cmp);
    allRows.forEach(r=>tb.appendChild(r));
  } else {
    const secs=[];
    let cur={hdr:null,rows:[]};
    allRows.forEach(r=>{
      if(r.dataset.sec){secs.push(cur);cur={hdr:r,rows:[]};}
      else cur.rows.push(r);
    });
    secs.push(cur);
    secs.forEach(s=>{
      s.rows.sort(cmp);
      if(s.hdr) tb.appendChild(s.hdr);
      s.rows.forEach(r=>tb.appendChild(r));
    });
  }
  th.classList.add(asc?'desc':'asc');
}
</script>"""

def _th(label: str, idx: int, num: bool = False, tip: str = "") -> str:
    cls  = "num-h" if num else ""
    dtip = f' data-tip="{tip}"' if tip else ""
    return f'<th class="{cls}" onclick="sortTable({idx},this)"{dtip}>{label}</th>'

def _tag_cell(text: str, css: str, raw: str = "") -> str:
    v = raw or text
    return f'<td data-v="{v}"><span class="tag {css}">{text}</span></td>'

def _num_td(display: str, raw) -> str:
    return f'<td class="num" data-v="{raw}">{display}</td>'

def _ctr_cell(val: float) -> str:
    return fmt_pct(val)

def _freq_cell(val: float) -> str:
    s = f"{val:.2f}"
    return f'<span class="freq-hi">{s}</span>' if val > 3.0 else s

_VCSS = {"Vehicles":"tv","Becar":"tb","Becser":"ts","Oksio":"tg","Grup Becier":"tg","Otros":"to"}
# tv=amarillo  tb=turquesa  ts=verde  tg=naranja  to=gris
_OCSS = {"Lead Ad":"tl","Landing":"tp","Impresiones":"tr"}

def render_meta_table(campaigns: list):
    if not campaigns:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de campañas.</p>',
                    unsafe_allow_html=True)
        return

    import streamlit.components.v1 as components

    COLS = [
        {"key":"Campaña",         "label":"Campaña"},
        {"key":"Vertical",        "label":"Vertical"},
        {"key":"Gasto (€)",       "label":"Importe gastado",    "num":True,"eur":True},
        {"key":"Impresiones",     "label":"Impresiones",         "num":True},
        {"key":"Alcance",         "label":"Alcance",             "num":True},
        {"key":"CPM",             "label":"CPM",                 "num":True,"eur":True},
        {"key":"CPC",             "label":"CPC",                 "num":True,"eur":True},
        {"key":"CTR (%)",         "label":"CTR",                 "num":True},
        {"key":"Clics enlace",    "label":"Clics",               "num":True},
        {"key":"Resultado",       "label":"Resultados",          "num":True},
        {"key":"Coste/Resultado", "label":"CPR",                 "num":True,"eur":True},
    ]
    ncols = len(COLS)

    def make_row(c):
        name = c["Campaña"]
        vert = c.get("Vertical","—")
        cells = ""
        for col in COLS:
            key = col["key"]
            if key == "Campaña":
                cells += f'<td data-v="{name}">{name}</td>'
            elif key == "Vertical":
                cells += _tag_cell(vert, _VCSS.get(vert,"to"))
            elif key == "CTR (%)":
                cells += f'<td class="num" data-v="{c.get(key,0)}">{_ctr_cell(c.get(key,0))}</td>'
            elif key == "Frecuencia":
                cells += f'<td class="num" data-v="{c.get(key,0)}">{_freq_cell(c.get(key,0))}</td>'
            elif col.get("eur"):
                cells += _num_td(fmt_eur(c.get(key)), c.get(key) or 0)
            elif col.get("num"):
                cells += _num_td(fmt_num(c.get(key)), c.get(key) or 0)
            else:
                cells += f'<td>{c.get(key,"—")}</td>'
        return f"<tr>{cells}</tr>"

    by_obj: dict[str, list] = {}
    for c in campaigns:
        by_obj.setdefault(c.get("Objetivo","—"), []).append(c)

    ORDER = [("Lead Ad","🎯  Lead Ad"),
             ("Landing","🌐  Tráfico / Landing"),
             ("Impresiones","📣  Alcance / Impresiones")]
    known = {o for o,_ in ORDER}

    heads = "".join(_th(c["label"], i, c.get("num", False), META_TIPS.get(c["label"],"")) for i, c in enumerate(COLS))
    tbody = ""
    sections_shown = 0
    for obj_key, title in ORDER:
        camps = by_obj.get(obj_key, [])
        if not camps:
            continue
        tbody += f'<tr class="sec-hdr" data-sec="1"><td colspan="{ncols}">{title}</td></tr>'
        tbody += "".join(make_row(c) for c in camps)
        sections_shown += 1
    for obj_key, camps in by_obj.items():
        if obj_key not in known and camps:
            tbody += f'<tr class="sec-hdr" data-sec="1"><td colspan="{ncols}">📌  Otros — {obj_key}</td></tr>'
            tbody += "".join(make_row(c) for c in camps)
            sections_shown += 1

    # Fila TOTAL Meta
    t_spend = sum(c["Gasto (€)"] for c in campaigns)
    t_imp   = sum(c["Impresiones"] for c in campaigns)
    t_alc   = sum(c["Alcance"] for c in campaigns)
    t_cli   = sum(c.get("Clics enlace", 0) for c in campaigns)
    t_res   = sum(c.get("Resultado", 0) for c in campaigns)
    t_cpm   = round(t_spend / t_imp * 1000, 2) if t_imp else 0
    t_cpc   = round(t_spend / t_cli, 2)         if t_cli  else 0
    t_ctr   = round(t_cli / t_imp * 100, 2)     if t_imp  else 0
    t_cpr   = round(t_spend / t_res, 2)          if t_res  else None
    total_row = (f'<tr class="total-row"><td>TOTAL</td><td></td>'
                 + _num_td(fmt_eur(t_spend), t_spend)
                 + _num_td(fmt_num(t_imp),   t_imp)
                 + _num_td(fmt_num(t_alc),   t_alc)
                 + _num_td(fmt_eur(t_cpm),   t_cpm)
                 + _num_td(fmt_eur(t_cpc),   t_cpc)
                 + f'<td class="num">{fmt_pct(t_ctr)}</td>'
                 + _num_td(fmt_num(t_cli),   t_cli)
                 + _num_td(fmt_num(t_res),   t_res)
                 + _num_td(fmt_eur(t_cpr),   t_cpr or 0)
                 + '</tr>')

    height = len(campaigns) * 42 + sections_shown * 44 + 56 + 44
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table>'
                    f'<thead><tr>{heads}</tr></thead><tbody>{tbody}{total_row}</tbody></table></div>',
                    height=height, scrolling=True)

def render_meta_adsets_table(adsets: list):
    if not adsets:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de adsets.</p>',
                    unsafe_allow_html=True)
        return

    import streamlit.components.v1 as components

    COLS = [
        {"key":"Campaña",         "label":"Campaña"},
        {"key":"Adset",           "label":"Adset"},
        {"key":"Vertical",        "label":"Vertical"},
        {"key":"Gasto (€)",       "label":"Importe gastado",    "num":True,"eur":True},
        {"key":"Impresiones",     "label":"Impresiones",         "num":True},
        {"key":"Alcance",         "label":"Alcance",             "num":True},
        {"key":"CPM",             "label":"CPM",                 "num":True,"eur":True},
        {"key":"CPC",             "label":"CPC",                 "num":True,"eur":True},
        {"key":"CTR (%)",         "label":"CTR",                 "num":True},
        {"key":"Clics enlace",    "label":"Clics",               "num":True},
        {"key":"Resultado",       "label":"Resultados",          "num":True},
        {"key":"Coste/Resultado", "label":"CPR",                 "num":True,"eur":True},
    ]

    heads = "".join(_th(c["label"], i, c.get("num", False), META_TIPS.get(c["label"],"")) for i, c in enumerate(COLS))
    rows = ""
    for c in adsets:
        name  = c["Campaña"];  sname  = (name[:30]+"…")  if len(name)>32  else name
        adset = c["Adset"];    sadset = (adset[:30]+"…") if len(adset)>32 else adset
        vert  = c.get("Vertical","—")
        cells = ""
        for col in COLS:
            key = col["key"]
            if key == "Campaña":
                cells += f'<td data-v="{name}">{name}</td>'
            elif key == "Adset":
                cells += f'<td data-v="{adset}">{adset}</td>'
            elif key == "Vertical":
                cells += _tag_cell(vert, _VCSS.get(vert,"to"))
            elif key == "CTR (%)":
                cells += f'<td class="num" data-v="{c.get(key,0)}">{fmt_pct(c.get(key,0))}</td>'
            elif col.get("eur"):
                cells += _num_td(fmt_eur(c.get(key)), c.get(key) or 0)
            elif col.get("num"):
                cells += _num_td(fmt_num(c.get(key)), c.get(key) or 0)
            else:
                cells += f'<td>{c.get(key,"—")}</td>'
        rows += f"<tr>{cells}</tr>"

    height = len(adsets) * 42 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table>'
                    f'<thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


def render_creatives_table(ads: list):
    if not ads:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de anuncios.</p>',
                    unsafe_allow_html=True)
        return

    import streamlit.components.v1 as components

    THUMB_CSS = ("width:80px;height:80px;object-fit:cover;border-radius:6px;"
                 "display:block;background:#1a1e35")
    VIDEO_OVERLAY = ("<div style='position:relative;width:80px;height:80px'>"
                     "<img src='{url}' style='" + THUMB_CSS + "'>"
                     "<div style='position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
                     "background:rgba(0,0,0,0.65);border-radius:50%;width:28px;height:28px;"
                     "display:flex;align-items:center;justify-content:center;"
                     "font-size:12px;color:#fff'>▶</div></div>")
    IMG_HTML    = "<img src='{url}' style='" + THUMB_CSS + "'>"
    NO_IMG      = "<div style='" + THUMB_CSS + ";border:1px dashed #2a3060'></div>"

    heads = ('<th style="cursor:default">Vista previa</th>'
             + _th("Adset", 1) + _th("Anuncio", 2) + _th("Estado", 3)
             + _th("Gasto", 4, True) + _th("Impresiones", 5, True)
             + _th("Alcance", 6, True) + _th("CPM", 7, True)
             + _th("CPC", 8, True) + _th("CTR", 9, True)
             + _th("Clics", 10, True) + _th("Resultados", 11, True)
             + _th("CPR", 12, True))

    STATUS_COLOR = {"ACTIVE":"#22c55e","PAUSED":"#fbbf24","DELETED":"#f87171",
                    "ARCHIVED":"#888","PENDING_REVIEW":"#a855f7"}

    rows = ""
    for a in ads:
        url = a.get("preview_url","")
        if url and a["is_video"]:
            thumb = VIDEO_OVERLAY.format(url=url)
        elif url:
            thumb = IMG_HTML.format(url=url)
        else:
            thumb = NO_IMG

        status = a.get("Estado","")
        sc = STATUS_COLOR.get(status,"#888")
        status_html = f'<span style="color:{sc};font-size:11px;font-weight:600">{status}</span>'

        adset_name = a.get("Adset","—")
        rows += (f'<tr>'
                 f'<td style="padding:8px 14px">{thumb}</td>'
                 f'<td data-v="{adset_name}">{adset_name}</td>'
                 f'<td data-v="{a["Anuncio"]}">{a["Anuncio"]}</td>'
                 f'<td data-v="{status}">{status_html}</td>'
                 + _num_td(fmt_eur(a["Gasto (€)"]),  a["Gasto (€)"])
                 + _num_td(fmt_num(a["Impresiones"]), a["Impresiones"])
                 + _num_td(fmt_num(a["Alcance"]),     a["Alcance"])
                 + _num_td(fmt_eur(a["CPM"]),         a["CPM"])
                 + _num_td(fmt_eur(a["CPC"]),         a["CPC"])
                 + f'<td class="num" data-v="{a["CTR (%)"]}">{fmt_pct(a["CTR (%)"])}</td>'
                 + _num_td(fmt_num(a["Clics"]),       a["Clics"])
                 + _num_td(fmt_num(a["Resultado"]),   a["Resultado"])
                 + _num_td(fmt_eur(a["CPR"]),         a["CPR"] or 0)
                 + '</tr>')

    height = len(ads) * 100 + 56
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table>'
                    f'<thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>',
                    height=height, scrolling=True)


def render_google_table(campaigns: list):
    if not campaigns:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de campañas.</p>',
                    unsafe_allow_html=True)
        return

    import streamlit.components.v1 as components

    VERT_ORDER = ["Vehicles","Becser","Becar","Oksio","Grup Becier","Otros"]
    VERT_ICONS = {"Vehicles":"🟡","Becser":"🟢","Becar":"🔵",
                  "Oksio":"🟠","Grup Becier":"🟠","Otros":"⚪"}
    ncols = 9

    heads = (_th("Campaña",0)
             + _th("Coste",1,True,       "Importe total invertido")
             + _th("Impresiones",2,True, "Veces que apareció el anuncio en búsquedas")
             + _th("CPM medio",3,True,   "Coste por cada 1.000 impresiones")
             + _th("CPC medio",4,True,   "Coste medio por clic")
             + _th("Clics",5,True,       "Clics en el anuncio")
             + _th("CTR",6,True,         "% de clics sobre impresiones")
             + _th("Conv.",7,True,       "Conversiones registradas (formularios, llamadas, etc.)")
             + _th("Coste/conv.",8,True, "Coste medio por conversión conseguida"))

    def make_row(c):
        name = c["Campaña"]
        return (f'<tr><td data-v="{name}">{name}</td>'
                + _num_td(fmt_eur(c["Gasto (€)"]),    c["Gasto (€)"])
                + _num_td(fmt_num(c["Impresiones"]),   c["Impresiones"])
                + _num_td(fmt_eur(c["CPM (€)"]),       c["CPM (€)"])
                + _num_td(fmt_eur(c["CPC (€)"]),       c["CPC (€)"])
                + _num_td(fmt_num(c["Clics"]),         c["Clics"])
                + f'<td class="num" data-v="{c["CTR (%)"]}">{fmt_pct(c["CTR (%)"])}</td>'
                + _num_td(str(int(c["Conversiones"])), c["Conversiones"])
                + _num_td(fmt_eur(c["Coste/conv."]),   c["Coste/conv."] or 0)
                + '</tr>')

    by_vert: dict[str, list] = {}
    for c in campaigns:
        by_vert.setdefault(c.get("Vertical","Otros"), []).append(c)

    tbody = ""
    n_sections = 0
    for vert in VERT_ORDER:
        camps = by_vert.get(vert, [])
        if not camps:
            continue
        icon = VERT_ICONS.get(vert,"⚪")
        tbody += (f'<tr class="sec-hdr" data-sec="1">'
                  f'<td colspan="{ncols}">{icon}  {vert}</td></tr>')
        tbody += "".join(make_row(c) for c in camps)
        n_sections += 1
    for vert, camps in by_vert.items():
        if vert not in VERT_ORDER and camps:
            tbody += (f'<tr class="sec-hdr" data-sec="1">'
                      f'<td colspan="{ncols}">⚪  {vert}</td></tr>')
            tbody += "".join(make_row(c) for c in camps)
            n_sections += 1

    # Fila TOTAL Google
    g_spend = sum(c["Gasto (€)"] for c in campaigns)
    g_imp   = sum(c["Impresiones"] for c in campaigns)
    g_cli   = sum(c["Clics"] for c in campaigns)
    g_conv  = sum(c["Conversiones"] for c in campaigns)
    g_cpm   = round(g_spend / g_imp * 1000, 2) if g_imp  else 0
    g_cpc   = round(g_spend / g_cli, 2)         if g_cli  else 0
    g_ctr   = round(g_cli / g_imp * 100, 2)     if g_imp  else 0
    g_cpa   = round(g_spend / g_conv, 2)         if g_conv else None
    total_row = (f'<tr class="total-row"><td>TOTAL</td>'
                 + _num_td(fmt_eur(g_spend), g_spend)
                 + _num_td(fmt_num(g_imp),   g_imp)
                 + _num_td(fmt_eur(g_cpm),   g_cpm)
                 + _num_td(fmt_eur(g_cpc),   g_cpc)
                 + _num_td(fmt_num(g_cli),   g_cli)
                 + f'<td class="num">{fmt_pct(g_ctr)}</td>'
                 + _num_td(str(int(g_conv)), g_conv)
                 + _num_td(fmt_eur(g_cpa),   g_cpa or 0)
                 + '</tr>')

    height = len(campaigns) * 42 + n_sections * 44 + 56 + 44
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table>'
                    f'<thead><tr>{heads}</tr></thead><tbody>{tbody}{total_row}</tbody></table></div>',
                    height=height, scrolling=True)


def render_google_keywords_table(keywords: list):
    if not keywords:
        st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de keywords.</p>',
                    unsafe_allow_html=True)
        return

    import streamlit.components.v1 as components

    MATCH_CSS = {"[Exacta]": "tl", '"Frase"': "tp", "Amplia": "to"}
    ncols = 18

    heads = (_th("Keyword", 0)
             + _th("Concordancia", 1,  False, "Tipo: [Exacta] busca la kw exacta · 'Frase' incluye variantes · Amplia muestra en búsquedas relacionadas")
             + _th("Vertical", 2)
             + _th("Conversiones", 3,  True,  "Conversiones registradas en el período")
             + _th("Coste/conv.", 4,   True,  "Coste medio por conversión conseguida")
             + _th("Coste", 5,         True,  "Importe total invertido en esta keyword")
             + _th("CTR", 6,           True,  "% de clics sobre el total de impresiones")
             + _th("CPC medio", 7,     True,  "Coste medio por clic en esta keyword")
             + _th("Tasa conv.", 8,    True,  "% de clics que generaron una conversión")
             + _th("Cuota impr.", 9,   True,  "% de impresiones obtenidas vs. total posible en búsquedas")
             + _th("Cuota perd. ranking", 10, True, "% de impresiones perdidas por baja posición del anuncio. Mejorar puja o Quality Score")
             + _th("Cuota clics", 11,  True,  "% de clics obtenidos del total disponible")
             + _th("Nivel calidad", 12,True,  "Puntuación de Google (1-10). Influye en el CPC real y la posición del anuncio")
             + _th("URL final", 13,    False, "Página de destino a la que va el usuario al hacer clic")
             + _th("CTR esperado", 14, False, "Predicción de Google sobre si esta keyword generará clics. Por encima/Promedio/Por debajo del promedio")
             + _th("Exp. landing", 15, False, "Valoración de Google sobre la relevancia de la página de destino para esta keyword")
             + _th("Relevancia anuncio", 16, False, "Grado de coincidencia entre el texto del anuncio y la intención de búsqueda del usuario"))

    # Agrupar por vertical
    by_vert: dict[str, list] = {}
    for k in keywords:
        by_vert.setdefault(k["Vertical"], []).append(k)

    VERT_ORDER  = ["Vehicles","Becser","Becar","Oksio","Grup Becier","Otros"]
    VERT_ICONS  = {"Vehicles":"🟡","Becser":"🟢","Becar":"🔴","Oksio":"🟠","Grup Becier":"🟠","Otros":"⚪"}

    tbody = ""
    n_sec = 0
    for vert in VERT_ORDER:
        kws = by_vert.get(vert, [])
        if not kws:
            continue
        tbody += (f'<tr class="sec-hdr" data-sec="1">'
                  f'<td colspan="{ncols}">{VERT_ICONS.get(vert,"⚪")}  {vert}</td></tr>')
        for k in kws:
            m_cls = MATCH_CSS.get(k["Concordancia"], "to")
            url   = k["URL final"]
            url_display = url[:35]+"…" if len(url) > 37 else url
            tbody += (f'<tr><td data-v="{k["Keyword"]}">{k["Keyword"]}</td>'
                      + _tag_cell(k["Concordancia"], m_cls)
                      + _tag_cell(k["Vertical"], _VCSS.get(k["Vertical"],"to"))
                      + _num_td(str(int(k["Conversiones"])),  k["Conversiones"])
                      + _num_td(fmt_eur(k["Coste/conv."]),    k["Coste/conv."] or 0)
                      + _num_td(fmt_eur(k["Coste"]),          k["Coste"])
                      + f'<td class="num" data-v="{k["CTR (%)"]}">{fmt_pct(k["CTR (%)"])}</td>'
                      + _num_td(fmt_eur(k["CPC medio"]),      k["CPC medio"])
                      + f'<td class="num" data-v="{k["Tasa conv. (%)"]}">{fmt_pct(k["Tasa conv. (%)"])}</td>'
                      + f'<td class="num" data-v="{k["Cuota impr. (%)"]}">{k["Cuota impr. (%)"]}</td>'
                      + f'<td class="num" data-v="{k["Cuota perd. ranking"]}">{k["Cuota perd. ranking"]}</td>'
                      + f'<td class="num" data-v="{k["Cuota clics (%)"]}">{k["Cuota clics (%)"]}</td>'
                      + f'<td class="num" data-v="{k["Nivel calidad"]}">{k["Nivel calidad"]}</td>'
                      + f'<td title="{url}" data-v="{url}" style="text-align:left">{url_display}</td>'
                      + f'<td data-v="{k["CTR esperado"]}">{k["CTR esperado"]}</td>'
                      + f'<td data-v="{k["Exp. landing"]}">{k["Exp. landing"]}</td>'
                      + f'<td data-v="{k["Relevancia anuncio"]}">{k["Relevancia anuncio"]}</td>'
                      + '</tr>')
        n_sec += 1

    # Total
    t_sp   = sum(k["Coste"] for k in keywords)
    t_conv = sum(k["Conversiones"] for k in keywords)
    t_cpa  = round(t_sp / t_conv, 2) if t_conv else None
    empty  = '<td></td>'
    tbody += (f'<tr class="total-row"><td>TOTAL</td><td></td><td></td>'
              + _num_td(str(int(t_conv)), t_conv)
              + _num_td(fmt_eur(t_cpa), t_cpa or 0)
              + _num_td(fmt_eur(t_sp), t_sp)
              + empty * 11 + '</tr>')

    height = len(keywords) * 42 + n_sec * 44 + 56 + 44
    components.html(f'{_TABLE_CSS}{_TABLE_JS}<div class="wrap"><table>'
                    f'<thead><tr>{heads}</tr></thead><tbody>{tbody}</tbody></table></div>',
                    height=height, scrolling=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    default_since, default_until = get_prev_month_range()

    period_options = {
        "Mes anterior":     _period_last_month(),
        "Este mes":         _period_this_month(),
        "Últimos 7 días":   _period_last_n(7),
        "Últimos 30 días":  _period_last_n(30),
        "Últimos 90 días":  _period_last_n(90),
        "Rango personalizado": None,
    }

    # ── Sidebar ────────────────────────────────────────────────────────────
    # ── Sidebar: solo Vista toggle ─────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div style="padding:16px 0 20px"><img src="https://www.becier.ad/wp-content/uploads/logo_gb_text_white_m.png" style="height:34px;object-fit:contain"><div style="font-size:11px;color:#3a4060;margin-top:6px">Performance Dashboard</div></div>',
                    unsafe_allow_html=True)

        vista = st.radio("Vista", ["📊 Período", "📅 Anual 2026"],
                         key="vista_toggle", label_visibility="collapsed")
        st.markdown('<hr style="border-color:#1a1e35;margin:16px 0">', unsafe_allow_html=True)

        if vista == "📅 Anual 2026":
            st.markdown('<div style="color:#6a7aaa;font-size:12px">Datos del año 2026<br>1 ene → hoy</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#6a7aaa;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px">Período</div>',
                        unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        if st.button("🔄  Refrescar datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        st.markdown('<div style="color:#2a3050;font-size:10px;margin-top:8px">Caché: 30 min</div>',
                    unsafe_allow_html=True)

    # ── Selector de período (arriba, antes del header) ─────────────────────
    if vista == "📅 Anual 2026":
        since = "2026-01-01"
        until = str(date.today())
        period_label = "Anual 2026"
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    else:
        col_sel, col_pad = st.columns([2, 4])
        with col_sel:
            selected = st.selectbox("📅 Período", list(period_options.keys()), index=0,
                                    key="period_sel")
            if selected == "Rango personalizado":
                c_d1, c_d2 = st.columns(2)
                since = str(c_d1.date_input("Desde", value=date.fromisoformat(default_since)))
                until = str(c_d2.date_input("Hasta", value=date.fromisoformat(default_until)))
            else:
                since, until = period_options[selected]
        period_label = selected if selected != "Rango personalizado" else f"{since} – {until}"

    # ── Fetch ──────────────────────────────────────────────────────────────
    with st.spinner("Cargando datos…"):
        meta_sum     = fetch_meta_summary(since, until)
        meta_camps   = fetch_meta_campaigns(since, until)
        meta_adsets  = fetch_meta_adsets_detail(since, until)
        meta_daily   = fetch_meta_daily(since, until)
        google_res   = fetch_google_campaigns(since, until)
        google_daily = fetch_google_daily(since, until)
        google_kw_res = fetch_google_keywords(since, until)

    google_camps = google_res.get("campaigns", [])
    google_error = google_res.get("error")

    # Totales combinados para el header
    meta_spend   = meta_sum.get("spend_eur", 0) if not meta_sum.get("error") else 0
    google_spend = sum(c["Gasto (€)"] for c in google_camps) if google_camps else 0
    total_spend  = meta_spend + google_spend

    # ── Header principal ─────────────────────────────────────────────────────
    st.markdown(
        f'<div class="dash-header">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<img src="https://www.becier.ad/wp-content/uploads/logo_gb_text_white_m.png" '
        f'style="height:26px;object-fit:contain" alt="Grup Becier">'
        f'</div>'
        f'<div class="dash-right">'
        f'<div style="text-align:right">'
        f'<div style="color:#444c70;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.8px">Inversión total del período</div>'
        f'<div style="color:#eef0ff;font-size:38px;font-weight:800;letter-spacing:-1px;line-height:1.1">{fmt_eur(total_spend)}</div>'
        f'</div>'
        f'<div style="background:#1a1e35;border:1px solid #252a48;border-radius:10px;padding:14px 22px;color:#6a7aaa;font-size:15px;font-weight:600;white-space:nowrap;line-height:1.6">'
        f'📅 {period_label}<br><span style="font-size:12px;color:#3a4060">{since} – {until}</span></div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True)


    # ── KPIs: dos columnas por plataforma ───────────────────────────────────
    col_meta, col_google = st.columns(2, gap="large")

    META_COLOR  = "#4a7fff"
    GOOGLE_COLOR = "#34a853"

    with col_meta:
        st.markdown(platform_header("Meta Ads", f"Cuenta Becier · {_meta_account_id()}", "meta"),
                    unsafe_allow_html=True)
        if meta_sum.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:13px">⚠ {meta_sum["error"]}</p>',
                        unsafe_allow_html=True)
        else:
            ms = meta_sum
            c1, c2, c3 = st.columns(3)
            c1.markdown(kpi_card("Gasto total", fmt_eur(ms["spend_eur"]), "💰", accent=META_COLOR), unsafe_allow_html=True)
            c2.markdown(kpi_card("Alcance", fmt_num(ms["reach"]), "👁️", accent=META_COLOR), unsafe_allow_html=True)
            c3.markdown(kpi_card("Impresiones", fmt_num(ms["impressions"]), "📊", accent=META_COLOR), unsafe_allow_html=True)

            total_clics_meta = sum(c.get("Clics enlace", 0) for c in meta_camps)
            cpc_meta = round(ms["spend_eur"] / total_clics_meta, 2) if total_clics_meta > 0 else 0

            c4, c5, c6 = st.columns(3)
            c4.markdown(kpi_card("CPM", fmt_eur(ms["cpm"]), "📈", accent=META_COLOR), unsafe_allow_html=True)
            c5.markdown(kpi_card("CTR", fmt_pct(ms["ctr_pct"]), "🖱️", accent=META_COLOR), unsafe_allow_html=True)
            c6.markdown(kpi_card("CPC", fmt_eur(cpc_meta), "💶", accent=META_COLOR), unsafe_allow_html=True)

            # Resultados desglosados por objetivo (usando datos por campaña)
            by_obj: dict[str, dict] = {}
            for c in meta_camps:
                obj = c.get("Objetivo", "—")
                if obj not in by_obj:
                    by_obj[obj] = {"spend": 0, "results": 0}
                by_obj[obj]["spend"]   += c.get("Gasto (€)", 0)
                by_obj[obj]["results"] += c.get("Resultado", 0)

            # Fila 3: Leads | CPL | Result. landing | CPR — 4 columnas
            d_lead   = by_obj.get("Lead Ad", {"spend":0,"results":0})
            d_land   = by_obj.get("Landing",  {"spend":0,"results":0})
            cpl  = round(d_lead["spend"] / d_lead["results"], 2) if d_lead["results"] > 0 else None
            cpr  = round(d_land["spend"] / d_land["results"], 2) if d_land["results"] > 0 else None

            r3a, r3b, r3c, r3d = st.columns(4)
            r3a.markdown(kpi_card("Leads",            fmt_num(d_lead["results"]), "🎯", accent=META_COLOR), unsafe_allow_html=True)
            r3b.markdown(kpi_card("CPL",              fmt_eur(cpl),              "💡", accent=META_COLOR), unsafe_allow_html=True)
            r3c.markdown(kpi_card("Result. landing",  fmt_num(d_land["results"]), "🌐", accent=META_COLOR), unsafe_allow_html=True)
            r3d.markdown(kpi_card("CPR landing",      fmt_eur(cpr),              "💡", accent=META_COLOR), unsafe_allow_html=True)

    with col_google:
        st.markdown(platform_header("Google Ads", "Cuenta Becier · 1632468817", "google"),
                    unsafe_allow_html=True)
        if google_error:
            st.markdown(f'<p style="color:#f87171;font-size:13px">⚠ {google_error}</p>',
                        unsafe_allow_html=True)
        elif google_camps:
            total_imp  = sum(c["Impresiones"] for c in google_camps)
            total_cli  = sum(c["Clics"] for c in google_camps)
            total_conv = sum(c["Conversiones"] for c in google_camps)
            avg_ctr    = (total_cli / total_imp * 100) if total_imp else 0
            avg_cpc    = (google_spend / total_cli) if total_cli else 0
            avg_cpm    = (google_spend / total_imp * 1000) if total_imp else 0
            cost_conv  = (google_spend / total_conv) if total_conv else None

            c1, c2, c3 = st.columns(3)
            c1.markdown(kpi_card("Gasto total", fmt_eur(google_spend), "💰", accent=GOOGLE_COLOR), unsafe_allow_html=True)
            c2.markdown(kpi_card("Clics", fmt_num(total_cli), "🖱️", accent=GOOGLE_COLOR), unsafe_allow_html=True)
            c3.markdown(kpi_card("Impresiones", fmt_num(total_imp), "📊", accent=GOOGLE_COLOR), unsafe_allow_html=True)

            c4, c5, c6 = st.columns(3)
            c4.markdown(kpi_card("CTR medio", fmt_pct(avg_ctr), "📈", accent=GOOGLE_COLOR), unsafe_allow_html=True)
            c5.markdown(kpi_card("CPC medio", fmt_eur(avg_cpc), "💶", accent=GOOGLE_COLOR), unsafe_allow_html=True)
            c6.markdown(kpi_card("Conversiones", f"{total_conv:.0f}", "✅", accent=GOOGLE_COLOR), unsafe_allow_html=True)

            c7, _, _ = st.columns(3)
            c7.markdown(kpi_card("Coste / conv.", fmt_eur(cost_conv), "💡", accent=GOOGLE_COLOR), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de Google Ads para el período.</p>',
                        unsafe_allow_html=True)

    # ── Gráficos ────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(platform_header("Análisis visual", f"{since} – {until}", "combined"),
                unsafe_allow_html=True)

    col_evo, col_donut, col_cpl = st.columns([5, 3, 3], gap="medium")

    def chart_label(text):
        st.markdown(f'<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">{text}</div>', unsafe_allow_html=True)

    with col_evo:
        chart_label("Inversión semanal — Meta vs Google")
        if meta_daily or google_daily:
            st.plotly_chart(chart_inversion_semanal(meta_daily, google_daily),
                            use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos diarios.</p>', unsafe_allow_html=True)

    with col_donut:
        chart_label("Presupuesto por vertical")
        if meta_camps or google_camps:
            st.plotly_chart(chart_desglose_vertical(meta_camps, google_camps),
                            use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos.</p>', unsafe_allow_html=True)

    with col_cpl:
        chart_label("CPL / CPR por vertical y canal")
        fig_cpr = chart_cpr_por_vertical_canal(meta_camps, google_camps)
        if fig_cpr.data:
            st.plotly_chart(fig_cpr, use_container_width=True, config=_NO_INTERACT)
        else:
            st.markdown('<p style="color:#5a6080;font-size:13px">Sin datos de resultados.</p>', unsafe_allow_html=True)

    # ── Tablas ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    tab_meta, tab_google = st.tabs([
        "📘  Meta Ads",
        "📗  Google Ads",
    ])

    with tab_meta:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        # Filtro por vertical con emojis de color
        VERT_EMOJI = {"Vehicles":"🟡","Becser":"🟢","Becar":"🔴","Oksio":"🟠","Grup Becier":"🟠","Otros":"⚪"}
        all_verts_meta = sorted({c.get("Vertical","Otros") for c in meta_camps if c.get("Vertical")})
        vert_labels    = {f'{VERT_EMOJI.get(v,"⚪")} {v}': v for v in all_verts_meta}
        vert_options   = ["🔘 Todos"] + list(vert_labels.keys())
        col_filt, _ = st.columns([1, 3])
        with col_filt:
            sel_vert_label = st.selectbox("Filtrar por vertical", vert_options, key="meta_vert_filter")

        sel_vert = None if sel_vert_label == "🔘 Todos" else vert_labels.get(sel_vert_label)
        filtered_camps  = meta_camps  if not sel_vert else [c for c in meta_camps  if c.get("Vertical") == sel_vert]
        filtered_adsets = meta_adsets if not sel_vert else [a for a in meta_adsets if a.get("Vertical") == sel_vert]

        render_meta_table(filtered_camps)
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px">Por conjunto de anuncios (Adset)</div>', unsafe_allow_html=True)
        render_meta_adsets_table(filtered_adsets)

        # ── Creatividades ──────────────────────────────────────────────────
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px">Creatividades</div>', unsafe_allow_html=True)

        if meta_adsets:
            camp_names = sorted({a["Campaña"] for a in meta_adsets})
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                sel_camp = st.selectbox("Campaña", camp_names, key="cr_camp")

            # Adsets únicos de la campaña seleccionada
            seen_ids: set = set()
            all_camp_adsets: list[tuple[str,str]] = []
            for a in meta_adsets:
                if a["Campaña"] == sel_camp:
                    aid = a.get("_adset_id","")
                    if aid and aid not in seen_ids:
                        seen_ids.add(aid)
                        all_camp_adsets.append((aid, a["Adset"]))

            with col_s2:
                adset_options = ["Todos"] + [name for _, name in all_camp_adsets]
                sel_adset_filter = st.selectbox("Adset", adset_options, key="cr_adset")

            if sel_adset_filter == "Todos":
                camp_adsets = all_camp_adsets
            else:
                camp_adsets = [(aid, name) for aid, name in all_camp_adsets
                               if name == sel_adset_filter]

            if camp_adsets:
                with st.spinner("Cargando creatividades…"):
                    all_ads: list = []
                    for adset_id, adset_name in camp_adsets:
                        ads = fetch_meta_ads_for_adset(adset_id, since, until)
                        for ad in ads:
                            ad["Adset"] = adset_name
                        all_ads.extend(ads)
                    all_ads.sort(key=lambda x: x["Gasto (€)"], reverse=True)

                if all_ads:
                    st.markdown(
                        f'<div style="color:#5a6080;font-size:11px;margin-bottom:8px">'
                        f'{len(all_ads)} anuncio{"s" if len(all_ads)!=1 else ""} · '
                        f'{len(camp_adsets)} adset{"s" if len(camp_adsets)!=1 else ""}</div>',
                        unsafe_allow_html=True)
                    render_creatives_table(all_ads)
                else:
                    st.markdown('<p style="color:#5a6080;font-size:13px">Sin anuncios con datos para este período.</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#f87171;font-size:13px">No se encontraron adsets. Refresca los datos.</p>', unsafe_allow_html=True)

    with tab_google:
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        all_verts_google = sorted({c.get("Vertical","Otros") for c in google_camps if c.get("Vertical")})
        vert_labels_g    = {f'{VERT_EMOJI.get(v,"⚪")} {v}': v for v in all_verts_google}
        col_fg, _ = st.columns([1, 3])
        with col_fg:
            sel_vert_g_label = st.selectbox("Filtrar por vertical", ["🔘 Todos"] + list(vert_labels_g.keys()), key="google_vert_filter")

        sel_vert_g      = None if sel_vert_g_label == "🔘 Todos" else vert_labels_g.get(sel_vert_g_label)
        filtered_google = google_camps if not sel_vert_g else [c for c in google_camps if c.get("Vertical") == sel_vert_g]
        render_google_table(filtered_google)

        # ── Keywords ──────────────────────────────────────────────────────
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#5a6080;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px">Keywords</div>', unsafe_allow_html=True)
        if google_kw_res.get("error"):
            st.markdown(f'<p style="color:#f87171;font-size:13px">⚠ {google_kw_res["error"]}</p>', unsafe_allow_html=True)
        else:
            kws = google_kw_res.get("keywords", [])
            all_verts_kw = sorted({k.get("Vertical","Otros") for k in kws if k.get("Vertical")})
            vert_labels_kw = {f'{VERT_EMOJI.get(v,"⚪")} {v}': v for v in all_verts_kw}
            col_fkw, _ = st.columns([1, 3])
            with col_fkw:
                sel_kw_label = st.selectbox("Filtrar por vertical", ["🔘 Todos"] + list(vert_labels_kw.keys()), key="kw_vert_filter")
            sel_kw = None if sel_kw_label == "🔘 Todos" else vert_labels_kw.get(sel_kw_label)
            filtered_kws = kws if not sel_kw else [k for k in kws if k.get("Vertical") == sel_kw]
            render_google_keywords_table(filtered_kws)

    # ── Footer ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;color:#1e2440;font-size:11px;margin-top:48px;padding:16px 0;border-top:1px solid #1a1e35">
        Grup Becier · Dashboard generado con Claude Code
    </div>""", unsafe_allow_html=True)


if __name__ == "__main__" or True:
    main()
