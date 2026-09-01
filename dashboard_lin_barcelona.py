# -*- coding: utf-8 -*-
"""
Dashboard de Seguiment de Projecte — Lin Barcelona (metodologia Lean)
Cas de demostració: circuit de trasplantament renal de donant viu (HUMS).

A diferència de dashboard_becier.py / dashboard_dcore.py (Meta/Google Ads), aquí la
font no són plataformes de publicitat sinó un Google Sheet de seguiment de projecte
(cronograma d'accions Lean + indicadors amb punt de partida i objectiu). L'estructura
del Sheet reprodueix la plantilla original (fulls "Cronograma" i "Indicadors") perquè
Lin Barcelona pugui seguir editant-la sense tocar el codi.
"""
import os
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ─── CONFIG DEL PROJECTE ──────────────────────────────────────────────────────
SHEET_ID = "1-8CarQuUiUSsb0JU1n9NXVThCaERngfTCEhBxqtrWBc"
GOOGLE_EPOCH = date(1899, 12, 30)

STATUS_ORDER = ["Pendent", "En procés", "Fet"]
STATUS_COLOR = {"Pendent": "#6b7280", "En procés": "#f59e0b", "Fet": "#14b8a6"}
STATUS_LABEL = {"Pendent": "Pendent", "En procés": "En procés", "Fet": "Fet"}

ACCENT = "#14b8a6"      # teal — accent neutre (salut/Lean)
ACCENT_SOFT = "rgba(20,184,166,0.12)"
GOOD = "#22c55e"
BAD = "#ef4444"
WARN = "#f59e0b"
NEUTRAL_TXT = "#8894c0"

# Indicadors de balanç: no busquen "millorar" un valor sinó comprovar que una
# millora d'un altre indicador no perjudiqui la qualitat/seguretat. Es tracten amb
# una etiqueta i una lògica de semàfor diferents de la resta (veure indicador_on_track).
BALANCING_INDICATORS = {"Taxa de complicacions post-trasplantament del donant (%)"}

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lin Barcelona · Seguiment de Projecte",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── CREDENCIALS (compatibilitat local + Streamlit Cloud) ────────────────────
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


# ─── SHEETS SERVICE ────────────────────────────────────────────────────────────
def _get_sheets_service():
    std_token = Path(__file__).parent / "credentials" / "token.json"
    std_secret = Path(__file__).parent / "credentials" / "client_secret.json"
    token_path = std_token if std_token.exists() else Path("/tmp/token.json")
    secret_path = std_secret if std_secret.exists() else Path("/tmp/client_secret.json")

    with open(token_path) as f:
        token_data = json.load(f)
    with open(secret_path) as f:
        secret_data = json.load(f)
    web_or_installed = secret_data.get("web") or secret_data.get("installed")

    credentials = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web_or_installed["client_id"],
        client_secret=web_or_installed["client_secret"],
        scopes=token_data.get("scopes"),
    )
    credentials.refresh(Request())
    return build("sheets", "v4", credentials=credentials)


def _serial_to_date(serial):
    if serial is None or serial == "":
        return None
    try:
        return GOOGLE_EPOCH + timedelta(days=float(serial))
    except (TypeError, ValueError):
        return None


def _status_from_progress(p) -> str:
    if p is None:
        return "Pendent"
    p = float(p)
    if p >= 1:
        return "Fet"
    if p > 0:
        return "En procés"
    return "Pendent"


def is_overdue(t: dict, today: date) -> bool:
    return t["estat"] != "Fet" and t["fi"] is not None and t["fi"] < today


# ─── FETCH: CRONOGRAMA ─────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_cronograma() -> dict:
    service = _get_sheets_service()

    meta = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Cronograma!B1",
        valueRenderOption="FORMATTED_VALUE",
    ).execute()
    titol = (meta.get("values") or [[""]])[0][0] if meta.get("values") else "Projecte"

    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Cronograma!B11:G30",
        valueRenderOption="UNFORMATTED_VALUE",
        dateTimeRenderOption="SERIAL_NUMBER",
    ).execute()
    rows = result.get("values", [])

    tasques = []
    for r in rows:
        r = r + [None] * (6 - len(r))
        proposta, accio, responsable, progres, inici, fi = r[:6]
        if not proposta and not accio:
            continue
        if not isinstance(progres, (int, float)) and not isinstance(inici, (int, float)):
            # fila d'instruccions de la plantilla (p. ex. "Esta fila indica el final...")
            continue
        progres = float(progres) if isinstance(progres, (int, float)) else 0.0
        inici_d = _serial_to_date(inici)
        fi_d = _serial_to_date(fi)
        tasques.append({
            "proposta": (proposta or "Sense proposta").strip(),
            "accio": (accio or "").strip(),
            "responsable": (responsable or "Sense assignar").strip(),
            "progres": progres,
            "estat": _status_from_progress(progres),
            "inici": inici_d,
            "fi": fi_d,
        })

    return {"titol": titol, "tasques": tasques}


# ─── FETCH: INDICADORS ──────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_indicadors() -> dict:
    service = _get_sheets_service()

    # Dues lectures de la mateixa graella: FORMATTED per a etiquetes/mesos/text
    # (p. ex. "feb-26", "45%") i UNFORMATTED per als valors mensuals numèrics
    # (evita que Sheets els retorni com a serials de data o amb coma decimal).
    fmt = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Indicadors!C3:U30",
        valueRenderOption="FORMATTED_VALUE",
    ).execute().get("values", [])
    raw = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Indicadors!C3:U30",
        valueRenderOption="UNFORMATTED_VALUE",
    ).execute().get("values", [])

    if not fmt:
        return {"actualitzat": None, "months": [], "indicadors": []}

    actualitzat = fmt[0][3] if len(fmt[0]) > 3 else None

    header_row_idx = None
    for i, r in enumerate(fmt):
        if r and str(r[0]).strip().lower() == "indicadors":
            header_row_idx = i
            break

    if header_row_idx is None:
        return {"actualitzat": actualitzat, "months": [], "indicadors": []}

    header = fmt[header_row_idx]
    months = [str(m) for m in header[6:19] if m not in (None, "")]

    indicadors = []
    for i in range(header_row_idx + 1, len(fmt)):
        r = fmt[i]
        if not r or not r[0]:
            continue
        r = r + [None] * (6 + len(months) - len(r))
        nom, punt_partida, objetiu, responsable, font, freq = r[:6]

        rraw = raw[i] if i < len(raw) else []
        rraw = list(rraw) + [None] * (6 + len(months) - len(rraw))
        valors_raw = rraw[6:6 + len(months)]

        valors = {}
        for m, v in zip(months, valors_raw):
            if v not in (None, ""):
                try:
                    valors[m] = float(v)
                except (TypeError, ValueError):
                    pass
        indicadors.append({
            "nom": str(nom).strip(),
            "punt_partida": punt_partida,
            "objetiu": objetiu,
            "responsable": responsable,
            "font": font,
            "frequencia": freq,
            "valors": valors,
        })

    return {"actualitzat": actualitzat, "months": months, "indicadors": indicadors}


# ─── FORMAT ─────────────────────────────────────────────────────────────────────
def fmt_pct(v) -> str:
    if v is None:
        return "—"
    return f"{v:.0f}%"


def fmt_num(v, decimals=0) -> str:
    if v is None:
        return "—"
    return f"{v:,.{decimals}f}".replace(",", ".")


def fmt_date(d) -> str:
    if d is None:
        return "—"
    return d.strftime("%d/%m/%Y")


# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #0d0f18; }
[data-testid="stHeader"] { background-color: #0d0f18; border-bottom: 1px solid #1a1e35; }
section[data-testid="stSidebar"] { background-color: #0b0d16; border-right: 1px solid #1a1e35; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

.dash-header {
    background: linear-gradient(135deg, #101820 0%, #0d0f18 100%);
    border: 1px solid #1c2f2c; border-radius: 14px; padding: 22px 28px; margin-bottom: 18px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;
}
.dash-title { color: #eef0ff; font-size: 20px; font-weight: 800; letter-spacing: -0.3px; }
.dash-subtitle { color: #5a6080; font-size: 12.5px; margin-top: 4px; }
.dash-period { background: #131f1d; border: 1px solid #1c332f; border-radius: 8px; padding: 10px 18px; color: #4fd6bd; font-size: 13px; font-weight: 600; white-space: nowrap; }

.kpi-card {
    background: #12152a; border: 1px solid #1e2440; border-radius: 10px;
    padding: 16px 18px 14px; margin-bottom: 10px; min-height: 104px;
    box-sizing: border-box; transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2e3560; }
.kpi-label { color: #5a6080; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.9px; margin-bottom: 6px; }
.kpi-value { color: #eef0ff; font-size: 24px; font-weight: 800; line-height: 1; letter-spacing: -0.5px; }
.kpi-sub { color: #444c70; font-size: 10.5px; margin-top: 5px; }

.section-title { color: #eef0ff; font-size: 15px; font-weight: 700; margin: 8px 0 12px; display:flex; align-items:center; gap:8px; }
.section-title .dot { width:7px; height:7px; border-radius:50%; background:#14b8a6; display:inline-block; }

.status-badge { display:inline-block; font-size:10.5px; font-weight:700; padding:3px 10px; border-radius:20px; letter-spacing:0.3px; white-space:nowrap; }
.status-pendent  { background: rgba(107,114,128,0.16); color:#9aa1b0; }
.status-en-proces{ background: rgba(245,158,11,0.16);  color:#f5b942; }
.status-fet       { background: rgba(20,184,166,0.16); color:#2dd4bf; }

.styled-table-wrap { overflow-x: auto; border-radius: 8px; border: 1px solid #1e2440; margin-bottom: 18px; }
table.custom { width: 100%; border-collapse: collapse; font-size: 12.5px; }
table.custom th { background:#161a30; color:#5a6080; font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; text-align:left; padding:10px 14px; border-bottom:1px solid #1e2440; }
table.custom td { padding:10px 14px; border-bottom:1px solid #171b30; color:#c8cce0; }
table.custom tr:last-child td { border-bottom:none; }
table.custom tr:hover td { background:#151933; }

.ind-card { background:#12152a; border:1px solid #1e2440; border-radius:10px; padding:16px 18px; margin-bottom:14px; }
.ind-name { color:#eef0ff; font-size:13px; font-weight:700; margin-bottom:10px; }
.ind-row { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px; }
.ind-metric-label { color:#5a6080; font-size:11px; }
.ind-metric-value { font-size:15px; font-weight:800; }
.ind-meta { color:#444c70; font-size:10.5px; margin-top:8px; border-top:1px solid #1a1e35; padding-top:8px; }

.divider { border: none; border-top: 1px solid #1a1e35; margin: 24px 0; }

.summary-banner {
    display:flex; align-items:flex-start; gap:12px; background:#101f24; border:1px solid #1c3a3f;
    border-radius:10px; padding:14px 18px; margin-bottom:18px; color:#c8e6e8; font-size:13px; line-height:1.5;
}
.summary-banner b { color:#4fd6bd; }
.summary-icon { font-size:16px; }

.balanc-badge {
    display:inline-block; font-size:9.5px; font-weight:700; padding:2px 8px; border-radius:10px;
    background: rgba(136,148,192,0.15); color:#a6b0d6; margin-left:8px; letter-spacing:0.3px; vertical-align:middle;
}

.overdue-badge { display:inline-block; font-size:10px; font-weight:700; padding:2px 9px; border-radius:20px; background:rgba(239,68,68,0.15); color:#f87171; white-space:nowrap; }
tr.row-overdue td { background: rgba(239,68,68,0.05); }
tr.row-overdue td:first-child { box-shadow: inset 3px 0 0 #ef4444; }

.disclaimer-strip { display:flex; flex-direction:column; gap:8px; margin: 0 0 20px; }
.disclaimer {
    display:flex; align-items:flex-start; gap:10px; padding: 10px 16px; border-radius: 8px;
    font-size: 12px; line-height:1.5; background: rgba(251,191,36,0.07); border: 1px solid rgba(251,191,36,0.24); color: #d8c483;
}
.disclaimer b { color: #fbbf24; }
.disclaimer.info { background: rgba(20,184,166,0.07); border-color: rgba(20,184,166,0.24); color: #a8d8d0; }
.disclaimer.info b { color: #4fd6bd; }
</style>
""", unsafe_allow_html=True)

_NO_INTERACT = {"displayModeBar": False}


# ─── COMPONENTS ─────────────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, sub: str = "", accent: str = ACCENT) -> str:
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi-card" style="border-top:2px solid {accent}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{sub_html}</div>')


def status_badge(estat: str) -> str:
    cls = {"Pendent": "status-pendent", "En procés": "status-en-proces", "Fet": "status-fet"}[estat]
    return f'<span class="status-badge {cls}">{STATUS_LABEL[estat]}</span>'


def section_title(text: str):
    st.markdown(f'<div class="section-title"><span class="dot"></span>{text}</div>', unsafe_allow_html=True)


def _clicked_categories(event: dict | None) -> list:
    """Extreu les categories (eix Y) clicades d'un esdeveniment on_select de plotly_chart."""
    if not event:
        return []
    points = event.get("selection", {}).get("points", [])
    return sorted({p.get("y") for p in points if p.get("y") is not None})


def sync_chart_click_to_filter(event_key: str, filter_key: str, fp_key: str):
    """Si l'usuari acaba de clicar una barra al gràfic `event_key`, sobreescriu
    l'estat del multiselect `filter_key` amb aquesta selecció, ABANS que es
    dibuixi el widget. Només actua quan la selecció del gràfic ha canviat des de
    l'últim cop (comparant `fp_key`), per no trepitjar una edició manual posterior
    del multiselect feta per l'usuari."""
    event = st.session_state.get(event_key)
    clicked = _clicked_categories(event)
    fingerprint = tuple(clicked)
    if st.session_state.get(fp_key) != fingerprint:
        st.session_state[filter_key] = clicked
        st.session_state[fp_key] = fingerprint


def render_disclaimers():
    st.markdown(
        '<div class="disclaimer-strip">'
        '<div class="disclaimer">⚠️ <div><b>Dades d\'exemple:</b> aquest dashboard mostra un cas de demostració fictici '
        '(HUMS · circuit de trasplantament renal de donant viu) per ensenyar com queda un projecte real connectat. '
        'Ni els noms de l\'equip clínic ni les xifres corresponen a dades reals de cap pacient ni hospital.</div></div>'
        '<div class="disclaimer info">⚖️ <div><b>Què és un "indicador de balanç":</b> a diferència dels altres indicadors '
        '(que busquen millorar un valor), un indicador de balanç comprova que una millora no en perjudiqui una altra '
        '— per exemple, que accelerar el circuit no faci pujar les complicacions. Es marca en verd quan es manté '
        'estable dins el llindar acordat, no quan "millora".</div></div>'
        '</div>', unsafe_allow_html=True,
    )


# ─── CHARTS ─────────────────────────────────────────────────────────────────────
def chart_gantt(tasques: list, today: date) -> go.Figure:
    ordered = sorted(
        [t for t in tasques if t["inici"] and t["fi"]],
        key=lambda t: (t["proposta"], t["inici"]),
    )
    fig = go.Figure()
    labels = [f'{t["proposta"].split(" - ")[0]} · {t["accio"][:42]}{"…" if len(t["accio"]) > 42 else ""}' for t in ordered]
    for t, label in zip(ordered, labels):
        duration_ms = (((t["fi"] - t["inici"]).days + 1) * 24 * 60 * 60 * 1000)
        overdue = is_overdue(t, today)
        marker_line = dict(color=BAD, width=2) if overdue else dict(width=0)
        estat_txt = f'{STATUS_LABEL[t["estat"]]}{" · ENDARRERIDA" if overdue else ""}'
        fig.add_trace(go.Bar(
            x=[duration_ms],
            y=[label],
            base=[t["inici"].isoformat()],
            orientation="h",
            marker=dict(color=STATUS_COLOR[t["estat"]], line=marker_line),
            hovertemplate=(f'<b>{t["accio"]}</b><br>Responsable: {t["responsable"]}'
                            f'<br>{fmt_date(t["inici"])} — {fmt_date(t["fi"])}'
                            f'<br>Estat: {estat_txt}<extra></extra>'),
            showlegend=False,
        ))
    fig.add_vline(x=today.isoformat(), line=dict(color=NEUTRAL_TXT, width=1.5, dash="dot"))
    fig.add_annotation(
        x=today.isoformat(), y=1, yref="paper", yanchor="bottom", showarrow=False,
        text="avui", font=dict(color=NEUTRAL_TXT, size=10.5),
    )
    fig.update_layout(
        barmode="stack",
        height=max(320, 34 * len(ordered) + 60),
        margin=dict(l=10, r=10, t=24, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8cce0", size=11.5),
        xaxis=dict(type="date", gridcolor="#1a1e35", tickfont=dict(color="#5a6080")),
        yaxis=dict(autorange="reversed", gridcolor="#1a1e35"),
    )
    return fig


def chart_per_responsable(tasques: list, highlight: list | None = None) -> go.Figure:
    resp_order = sorted({t["responsable"] for t in tasques})
    highlight = highlight or []
    opacity = [1.0 if (not highlight or r in highlight) else 0.3 for r in resp_order]
    fig = go.Figure()
    for estat in STATUS_ORDER:
        counts = [sum(1 for t in tasques if t["responsable"] == r and t["estat"] == estat) for r in resp_order]
        fig.add_trace(go.Bar(
            y=resp_order, x=counts, orientation="h", name=STATUS_LABEL[estat],
            marker=dict(color=STATUS_COLOR[estat], opacity=opacity),
        ))
    fig.update_layout(
        barmode="stack",
        height=max(240, 46 * len(resp_order) + 60),
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8cce0", size=11.5),
        xaxis=dict(gridcolor="#1a1e35", tickfont=dict(color="#5a6080"), dtick=1),
        yaxis=dict(gridcolor="#1a1e35"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
    )
    return fig


def chart_per_proposta(tasques: list, highlight: list | None = None) -> go.Figure:
    props = sorted({t["proposta"] for t in tasques})
    highlight = highlight or []
    avg = [sum(t["progres"] for t in tasques if t["proposta"] == p) / max(1, sum(1 for t in tasques if t["proposta"] == p)) * 100 for p in props]
    colors = [GOOD if a >= 100 else (STATUS_COLOR["En procés"] if a > 0 else STATUS_COLOR["Pendent"]) for a in avg]
    opacity = [1.0 if (not highlight or p in highlight) else 0.3 for p in props]
    # Nota: NO es pot fer servir `text`/`textfont` en aquesta traça (bar amb on_select
    # actiu) — Streamlit intenta llegir `trace.textfont` en aplicar l'estil de selecció
    # i falla si la traça no en té un de complet, cosa que bloqueja per complet el clic.
    # Les etiquetes de percentatge es dibuixen com a annotations (figura), no com a text
    # de la traça, per evitar aquest camí de codi.
    fig = go.Figure(go.Bar(
        x=avg, y=props, orientation="h",
        marker=dict(color=colors, opacity=opacity),
        hovertemplate="%{y}<br>Progrés mitjà: %{x:.0f}%<extra></extra>",
    ))
    for p, a in zip(props, avg):
        fig.add_annotation(
            x=a, y=p, text=f"{a:.0f}%", showarrow=False,
            xanchor="left", xshift=6, font=dict(color="#c8cce0", size=11),
        )
    fig.update_layout(
        height=max(240, 50 * len(props) + 60),
        margin=dict(l=10, r=30, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8cce0", size=11.5),
        xaxis=dict(range=[0, 115], gridcolor="#1a1e35", tickfont=dict(color="#5a6080"), ticksuffix="%"),
        yaxis=dict(gridcolor="#1a1e35"),
    )
    return fig


def chart_indicador(ind: dict, months: list) -> go.Figure:
    x = [m for m in months if m in ind["valors"]]
    y = [ind["valors"][m] for m in x]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", line=dict(color=ACCENT, width=2.5),
        marker=dict(size=7, color=ACCENT), name="Valor",
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))
    target = _parse_numeric(ind.get("objetiu"))
    if target is not None and x:
        fig.add_trace(go.Scatter(
            x=x, y=[target] * len(x), mode="lines", line=dict(color=NEUTRAL_TXT, width=1.5, dash="dash"),
            name="Objectiu", hoverinfo="skip",
        ))
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8cce0", size=10.5),
        xaxis=dict(gridcolor="#1a1e35", tickfont=dict(color="#5a6080")),
        yaxis=dict(gridcolor="#1a1e35"),
        showlegend=False,
    )
    return fig


def _parse_numeric(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", ".")
    num = ""
    for ch in s:
        if ch.isdigit() or ch in ".-":
            num += ch
        elif num:
            break
    try:
        return float(num) if num else None
    except ValueError:
        return None


def indicador_on_track(ind: dict, months: list):
    """Retorna (on_track: bool|None, latest, delta_mes_anterior) per a un indicador.

    Els indicadors de balanç (BALANCING_INDICATORS) es consideren "on track" quan
    es mantenen per sota/igual de l'objectiu, independentment de si l'objectiu és
    igual al punt de partida (no busquen millorar, busquen no empitjorar)."""
    x = [m for m in months if m in ind["valors"]]
    latest = ind["valors"][x[-1]] if x else None
    previous = ind["valors"][x[-2]] if len(x) >= 2 else None
    delta = (latest - previous) if (latest is not None and previous is not None) else None

    target = _parse_numeric(ind.get("objetiu"))
    baseline = _parse_numeric(ind.get("punt_partida"))
    if latest is None or target is None:
        return None, latest, delta

    if ind["nom"] in BALANCING_INDICATORS:
        return latest <= target, latest, delta

    if baseline is None:
        return None, latest, delta
    improving_up = target >= baseline
    on_track = (latest >= target) if improving_up else (latest <= target)
    return on_track, latest, delta


def indicador_card_html(ind: dict, months: list) -> str:
    x = [m for m in months if m in ind["valors"]]
    on_track, latest, delta = indicador_on_track(ind, months)
    color = GOOD if on_track is True else (BAD if on_track is False else ACCENT)

    latest_str = fmt_num(latest, 1) if latest is not None else "—"
    delta_html = ""
    if delta is not None:
        arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "▬")
        delta_html = f'<span style="font-size:10.5px;color:#5a6080;margin-left:6px;">{arrow} {abs(delta):.1f} vs mes anterior</span>'

    balanc_badge = ""
    if ind["nom"] in BALANCING_INDICATORS:
        balanc_badge = '<span class="balanc-badge" title="Indicador de balanç: comprova que una millora no en perjudiqui una altra">⚖ Indicador de balanç</span>'

    return (
        f'<div class="ind-card">'
        f'<div class="ind-name">{ind["nom"]}{balanc_badge}</div>'
        f'<div class="ind-row"><span class="ind-metric-label">Valor actual ({x[-1] if x else "—"})</span>'
        f'<span class="ind-metric-value" style="color:{color}">{latest_str}{delta_html}</span></div>'
        f'<div class="ind-row"><span class="ind-metric-label">Punt de partida</span>'
        f'<span class="ind-metric-value" style="font-size:12px;color:#8894c0">{ind["punt_partida"] or "—"}</span></div>'
        f'<div class="ind-row"><span class="ind-metric-label">Objectiu</span>'
        f'<span class="ind-metric-value" style="font-size:12px;color:#8894c0">{ind["objetiu"] or "—"}</span></div>'
        f'<div class="ind-meta">Responsable: {ind["responsable"] or "—"} · Font: {ind["font"] or "—"} · {ind["frequencia"] or "—"}</div>'
        f'</div>'
    )


# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🩺 Lin Barcelona")
    st.caption("Panell de seguiment Lean")
    if st.button("🔄 Refrescar dades", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")

cronograma = fetch_cronograma()
indicadors_data = fetch_indicadors()
tasques = cronograma["tasques"]

# Si l'últim clic de l'usuari va ser sobre una barra dels gràfics de desglossament
# (més avall a la pàgina), això actualitza el filtre corresponent ABANS de dibuixar
# els widgets del sidebar — així els gràfics fan també de selector interactiu.
st.session_state.setdefault("filt_resp", [])
st.session_state.setdefault("filt_prop", [])
sync_chart_click_to_filter("chart_responsable", "filt_resp", "_fp_resp")
sync_chart_click_to_filter("chart_proposta", "filt_prop", "_fp_prop")

def _netejar_filtres():
    # Un widget amb key= no es pot reassignar via session_state un cop ja instanciat
    # en aquesta mateixa execució (StreamlitWidgetAlreadyInstantiatedError). Un callback
    # on_click s'executa ABANS que el script es torni a dibuixar, així que aquí sí
    # és segur mutar l'estat: el multiselect encara no s'ha instanciat en aquesta execució.
    st.session_state["filt_resp"] = []
    st.session_state["filt_prop"] = []
    st.session_state["_fp_resp"] = ()
    st.session_state["_fp_prop"] = ()


with st.sidebar:
    responsables = sorted({t["responsable"] for t in tasques})
    propostes = sorted({t["proposta"] for t in tasques})
    filt_resp = st.multiselect(
        "Responsable", responsables, key="filt_resp",
        placeholder="Tots els responsables",
    )
    filt_prop = st.multiselect(
        "Proposta de millora", propostes, key="filt_prop",
        placeholder="Totes les propostes",
    )
    st.caption("💡 També pots fer clic a una barra dels gràfics de desglossament per filtrar.")
    st.button("✖ Netejar filtres", use_container_width=True, on_click=_netejar_filtres)

# Cap selecció = sense filtre (mostra tot); és el comportament "Tots" per defecte.
actius_resp = filt_resp or responsables
actius_prop = filt_prop or propostes
tasques_filtrades = [t for t in tasques if t["responsable"] in actius_resp and t["proposta"] in actius_prop]

# ─── HEADER ─────────────────────────────────────────────────────────────────────
TODAY = date.today()

total_accions = len(tasques)
completades = sum(1 for t in tasques if t["estat"] == "Fet")
en_curs = sum(1 for t in tasques if t["estat"] == "En procés")
pendents = sum(1 for t in tasques if t["estat"] == "Pendent")
endarrerides = sum(1 for t in tasques if is_overdue(t, TODAY))
progres_global = (sum(t["progres"] for t in tasques) / total_accions * 100) if total_accions else 0

months_all = indicadors_data["months"]
indicadors_all = indicadors_data["indicadors"]
on_track_flags = [indicador_on_track(ind, months_all)[0] for ind in indicadors_all]
indicadors_ok = sum(1 for f in on_track_flags if f is True)
n_indicadors = len(indicadors_all)

st.markdown(
    f'<div class="dash-header">'
    f'<div><div class="dash-title">{cronograma["titol"]}</div>'
    f'<div class="dash-subtitle">Lin Barcelona · Metodologia Lean aplicada a salut</div></div>'
    f'<div class="dash-period">Progrés global · {progres_global:.0f}%</div>'
    f'</div>', unsafe_allow_html=True,
)

render_disclaimers()

# ─── RESUM EXECUTIU ─────────────────────────────────────────────────────────────
if endarrerides == 0:
    endarrerides_txt = "cap acció està endarrerida"
elif endarrerides == 1:
    endarrerides_txt = "hi ha <b>1 acció endarrerida</b> que cal revisar"
else:
    endarrerides_txt = f"hi ha <b>{endarrerides} accions endarrerides</b> que cal revisar"

st.markdown(
    f'<div class="summary-banner"><span class="summary-icon">📋</span>'
    f'<div>El projecte avança al <b>{progres_global:.0f}%</b> ({completades} de {total_accions} accions fetes): '
    f'<b>{indicadors_ok} de {n_indicadors} indicadors</b> ja han assolit el seu objectiu, i {endarrerides_txt}.</div></div>',
    unsafe_allow_html=True,
)

# ─── KPI ROW ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown(kpi_card("Accions totals", str(total_accions), "en el cronograma"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("Fetes", str(completades), f"{completades/total_accions*100:.0f}% del total" if total_accions else "—", accent=STATUS_COLOR["Fet"]), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("En procés", str(en_curs), f"{en_curs/total_accions*100:.0f}% del total" if total_accions else "—", accent=STATUS_COLOR["En procés"]), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card("Pendents", str(pendents), f"{pendents/total_accions*100:.0f}% del total" if total_accions else "—", accent=STATUS_COLOR["Pendent"]), unsafe_allow_html=True)
with c5:
    st.markdown(kpi_card("Endarrerides", str(endarrerides), "respecte la data de fi prevista", accent=BAD if endarrerides else GOOD), unsafe_allow_html=True)
with c6:
    st.markdown(kpi_card("Indicadors monitoritzats", str(n_indicadors), f"{indicadors_ok} ja a l'objectiu"), unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── GANTT ──────────────────────────────────────────────────────────────────────
section_title("Cronograma d'accions")
st.plotly_chart(chart_gantt(tasques_filtrades, TODAY), use_container_width=True, config=_NO_INTERACT)

# ─── TAULA D'ACCIONS ────────────────────────────────────────────────────────────
rows_html = ""
for t in sorted(tasques_filtrades, key=lambda t: (t["inici"] or date.max)):
    overdue = is_overdue(t, TODAY)
    row_cls = ' class="row-overdue"' if overdue else ""
    alerta = '<span class="overdue-badge">⚠ Endarrerida</span>' if overdue else "—"
    rows_html += (
        f'<tr{row_cls}><td>{t["proposta"]}</td><td>{t["accio"]}</td><td>{t["responsable"]}</td>'
        f'<td>{status_badge(t["estat"])}</td><td>{fmt_date(t["inici"])}</td><td>{fmt_date(t["fi"])}</td><td>{alerta}</td></tr>'
    )
st.markdown(
    '<div class="styled-table-wrap"><table class="custom">'
    '<tr><th>Proposta de millora</th><th>Acció</th><th>Responsable</th><th>Estat</th><th>Inici</th><th>Fi</th><th>Alerta</th></tr>'
    f'{rows_html}</table></div>', unsafe_allow_html=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── DESGLOSSAMENT ──────────────────────────────────────────────────────────────
# Aquests dos gràfics mostren sempre TOTES les accions (no només les filtrades) perquè
# fan també de selector interactiu: clicar una barra filtra el Gantt i la taula de dalt.
col_resp, col_prop = st.columns(2, gap="large")
with col_resp:
    section_title("Desglossament per responsable · clica una barra per filtrar")
    st.plotly_chart(
        chart_per_responsable(tasques, highlight=filt_resp), use_container_width=True,
        config=_NO_INTERACT, on_select="rerun", selection_mode="points", key="chart_responsable",
    )
with col_prop:
    section_title("Progrés per proposta de millora · clica una barra per filtrar")
    st.plotly_chart(
        chart_per_proposta(tasques, highlight=filt_prop), use_container_width=True,
        config=_NO_INTERACT, on_select="rerun", selection_mode="points", key="chart_proposta",
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── INDICADORS ─────────────────────────────────────────────────────────────────
section_title("Indicadors del projecte")
if indicadors_data["actualitzat"]:
    st.caption(f'Última actualització de dades: {indicadors_data["actualitzat"]}')

months = indicadors_data["months"]
indicadors = indicadors_data["indicadors"]

for i in range(0, len(indicadors), 2):
    cols = st.columns(2, gap="large")
    for col, ind in zip(cols, indicadors[i:i + 2]):
        with col:
            st.markdown(indicador_card_html(ind, months), unsafe_allow_html=True)
            st.plotly_chart(chart_indicador(ind, months), use_container_width=True, config=_NO_INTERACT)
