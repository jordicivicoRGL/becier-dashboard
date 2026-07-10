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
