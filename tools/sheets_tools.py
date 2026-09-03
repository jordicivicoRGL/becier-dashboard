# -*- coding: utf-8 -*-
"""
Lectura del Sheet de negociaciones/ventas del CRM de Grup Becier.
Fuente: exportación del CRM, convertida a Google Sheets nativo.
"""
import os
import json
from datetime import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

DEALS_SHEET_ID = "1ceahGbhnyQ99J_6RdWD5g-66KWiHsc5bWUHxr8GlYLo"

# "Creatividades Dcore" — hoja que ya mantienen Jordi/Vero con el estado real de cada
# landing (URL de test en Vercel, URL activa en dcore.es, si Vero la ha revisado, si
# está activa en Meta/Google). Es la fuente de verdad para KNOWN_LANDINGS del dashboard
# — así Jordi/Vero pueden añadir/editar landings sin tocar código nunca más.
DCORE_LANDINGS_SHEET_ID = "1BTah3mnvvJo3lIgM9Ca73rF-_8nfz5HMXjrqDRXQy6k"
DCORE_LANDINGS_TAB = "LANDINGS"

ETAPAS_VENTA = {"Venut", "Vehicle per entregar"}
ETAPA_NEGOCIACION = "En negociació"
# "Website" se incluye porque las campañas de Meta/Google Ads derivan a landing pages
# y el CRM las registra como Website en vez de PAID MEDIA cuando el lead entra por ahí.
# "Instagram Direct" son leads que escriben por DM desde un anuncio de Meta.
ORIGENES_PAID_MEDIA = {"PAID MEDIA", "WEBSITE", "INSTAGRAM DIRECT"}


def _get_sheets_service():
    std_token = os.path.join(os.path.dirname(__file__), "..", "credentials", "token.json")
    std_secret = os.path.join(os.path.dirname(__file__), "..", "credentials", "client_secret.json")
    token_path = std_token if os.path.exists(std_token) else "/tmp/token.json"
    client_secret_path = std_secret if os.path.exists(std_secret) else "/tmp/client_secret.json"

    with open(token_path) as f:
        token_data = json.load(f)
    with open(client_secret_path) as f:
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


def fetch_becier_deals() -> list[dict]:
    """Lee todas las negociaciones del CRM Becier.

    Devuelve una lista de dicts: id, etapa, origen, creado (datetime).
    Filas sin fecha de creación parseable se descartan.
    """
    service = _get_sheets_service()

    meta = service.spreadsheets().get(spreadsheetId=DEALS_SHEET_ID).execute()
    tab_title = meta["sheets"][0]["properties"]["title"]

    result = service.spreadsheets().values().get(
        spreadsheetId=DEALS_SHEET_ID,
        range=f"'{tab_title}'!A2:J",
    ).execute()
    rows = result.get("values", [])

    deals = []
    for r in rows:
        if len(r) < 10:
            continue
        etapa = (r[1] or "").strip()
        origen = (r[6] or "").strip()
        creado_raw = (r[9] or "").strip()
        try:
            creado = datetime.strptime(creado_raw, "%d.%m.%Y %H:%M:%S")
        except ValueError:
            continue
        deals.append({"id": r[0], "etapa": etapa, "origen": origen, "creado": creado})
    return deals


# DCORE — Sheet de leads con código postal y presupuesto (formulario Lead Ads Meta).
# PENDIENTE (2026-08-31): Jordi tiene que confirmar el ID real del Sheet y sus columnas
# (ver clients/dcore.md). Mientras GOOGLE_SHEET_ID_DCORE_LEADS no esté en .env, esta
# función devuelve "configured": False y el dashboard muestra un aviso en vez de datos.
# Estructura de columnas esperada (ajustar rango/índices en cuanto se confirme el Sheet):
#   A: Fecha | B: Nombre | C: Teléfono | D: Código Postal | E: Presupuesto | F: Campaña/Adset
def fetch_dcore_leads() -> dict:
    """Lee el Sheet de leads de DCORE (código postal + presupuesto) si está configurado."""
    sheet_id = os.environ.get("GOOGLE_SHEET_ID_DCORE_LEADS", "").strip()
    if not sheet_id:
        return {"configured": False, "leads": []}

    try:
        service = _get_sheets_service()
        meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        tab_title = meta["sheets"][0]["properties"]["title"]
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=f"'{tab_title}'!A2:F",
        ).execute()
        rows = result.get("values", [])
    except Exception as e:
        return {"configured": True, "error": str(e), "leads": []}

    leads = []
    for r in rows:
        r = r + [""] * (6 - len(r))
        fecha, nombre, telefono, cp, presupuesto, campana = r[:6]
        cp = (cp or "").strip()
        if not cp:
            continue
        leads.append({
            "fecha": (fecha or "").strip(),
            "nombre": (nombre or "").strip(),
            "telefono": (telefono or "").strip(),
            "cp": cp,
            "presupuesto": (presupuesto or "").strip(),
            "campana": (campana or "").strip(),
        })
    return {"configured": True, "leads": leads}


def summarize_funnel(deals: list[dict], since: str, until: str) -> dict:
    """Filtra por origen Paid Media, creado en 2026 y dentro de [since, until],
    y cuenta el embudo leads > negociaciones > ventas."""
    since_d = datetime.strptime(since, "%Y-%m-%d").date()
    until_d = datetime.strptime(until, "%Y-%m-%d").date()

    filtered = [
        d for d in deals
        if d["origen"].upper() in ORIGENES_PAID_MEDIA
        and d["creado"].year == 2026
        and since_d <= d["creado"].date() <= until_d
    ]

    leads = len(filtered)
    negociaciones = sum(1 for d in filtered if d["etapa"] == ETAPA_NEGOCIACION)
    ventas = sum(1 for d in filtered if d["etapa"] in ETAPAS_VENTA)

    return {"leads": leads, "negociaciones": negociaciones, "ventas": ventas}


def fetch_dcore_known_landings() -> dict:
    """Lee la pestaña LANDINGS de 'Creatividades Dcore' (mantenida por Jordi/Vero) y
    devuelve las landings con URL activa en dcore.es como lista de (path, label, tema)
    — mismo formato que tools/dcore_naming.py::KNOWN_LANDINGS, para que el dashboard
    pueda usar esta fuente en vivo y solo caer al fallback hardcodeado si falla.

    Criterio de "activa": columna 'Url activa' rellena. Las columnas 'Activa Meta' /
    'Activa Google' no se usan como filtro porque no están siempre al día (landings ya
    con URL real y revisadas por Vero pero con esas casillas todavía en FALSE)."""
    from urllib.parse import urlparse

    try:
        service = _get_sheets_service()
        result = service.spreadsheets().values().get(
            spreadsheetId=DCORE_LANDINGS_SHEET_ID,
            range=f"'{DCORE_LANDINGS_TAB}'!A2:C200",
        ).execute()
        rows = result.get("values", [])
    except Exception as e:
        return {"error": str(e)}

    landings = []
    for r in rows:
        r = r + [""] * (3 - len(r))
        label, _url_test, url_activa = r[:3]
        label = (label or "").strip()
        url_activa = (url_activa or "").strip()
        if not label or not url_activa:
            continue
        path = urlparse(url_activa if "://" in url_activa else f"https://{url_activa}").path or "/"
        tema = "Evo" if "evo" in label.lower() else "Reformas B2C"
        landings.append((path, label, tema))
    return {"landings": landings}
