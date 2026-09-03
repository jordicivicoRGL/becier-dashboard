# -*- coding: utf-8 -*-
"""
Lectura de Google Analytics 4 (Data API) para el bloque de landings de DCORE.

Requiere:
  1. Scope 'analytics.readonly' en el token OAuth compartido (credentials/token.json) —
     ya añadido en tools/calendar_tools.py::SCOPES el 2026-08-31.
  2. Las APIs "Google Analytics Admin API" y "Google Analytics Data API" habilitadas
     en el proyecto de Google Cloud del client_secret.json (pendiente, Jordi tiene que
     habilitarlas desde Cloud Console — ver clients/dcore.md para los links directos).
  3. GA4_PROPERTY_ID_DCORE en .env (ID numérico de la propiedad, no el measurement ID
     G-LKG6KEHBKP). Si no está, se intenta autodetectar vía accountSummaries y cachear.
"""
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CREDENTIALS_DIR = os.path.join(os.path.dirname(__file__), "..", "credentials")
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, "token.json")
CLIENT_SECRET_PATH = os.path.join(CREDENTIALS_DIR, "client_secret.json")


def _get_ga4_credentials() -> Credentials:
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    with open(CLIENT_SECRET_PATH) as f:
        secret_data = json.load(f)
    web = secret_data.get("web") or secret_data.get("installed")
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web["client_id"],
        client_secret=web["client_secret"],
        scopes=token_data.get("scopes"),
    )
    creds.refresh(Request())
    return creds


def discover_ga4_property_id(domain_hint: str = "dcore.es") -> dict:
    """Busca la propiedad GA4 cuyo nombre/URL contenga domain_hint, vía Admin API.
    Devuelve {'property_id': str} o {'error': str} si la Admin API no está habilitada
    o no se encuentra ninguna propiedad que matchee."""
    import requests
    try:
        creds = _get_ga4_credentials()
    except Exception as e:
        return {"error": f"No se pudo cargar credenciales: {e}"}

    try:
        r = requests.get(
            "https://analyticsadmin.googleapis.com/v1beta/accountSummaries",
            headers={"Authorization": f"Bearer {creds.token}"}, timeout=15,
        )
        data = r.json()
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}
    except Exception as e:
        return {"error": str(e)}

    for account in data.get("accountSummaries", []):
        for prop in account.get("propertySummaries", []):
            display_name = prop.get("displayName", "").lower()
            if domain_hint.lower() in display_name:
                prop_id = prop.get("property", "").replace("properties/", "")
                return {"property_id": prop_id, "display_name": prop.get("displayName")}

    return {"error": f"No se encontró ninguna propiedad GA4 con '{domain_hint}' en el nombre. "
                      f"Propiedades disponibles: "
                      + ", ".join(p.get("displayName", "") for a in data.get("accountSummaries", [])
                                  for p in a.get("propertySummaries", []))}


def fetch_ga4_landing_metrics(property_id: str, since: str, until: str) -> dict:
    """Sesiones y conversiones por página (pagePath), desglosadas por canal
    (sessionDefaultChannelGroup) para no mezclar tráfico de Google Ads con el de
    Meta/orgánico en la misma cifra — ver conversación 2026-08-31: Jordi pidió separar
    el tráfico porque una landing puede recibir sesiones de ambas plataformas a la vez.

    Aviso real (ver clients/dcore.md): Meta Ads no tiene UTMs consistentes en todos los
    adsets, así que parte de su tráfico cae en 'Organic Social' en vez de 'Paid Social' —
    la cifra de 'Google Ads' (Paid Search) es fiable, la de 'Meta/Otros' es una
    aproximación por debajo de la realidad hasta que se etiquete bien.
    """
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Dimension, Metric,
        )
    except ImportError:
        return {"error": "Paquete google-analytics-data no instalado."}

    try:
        creds = _get_ga4_credentials()
        client = BetaAnalyticsDataClient(credentials=creds)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath"), Dimension(name="sessionDefaultChannelGroup")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="engagedSessions"),
                Metric(name="conversions"),
            ],
            date_ranges=[DateRange(start_date=since, end_date=until)],
        )
        response = client.run_report(request)
    except Exception as e:
        return {"error": str(e)}

    by_path: dict[str, dict] = {}
    for row in response.rows:
        path = row.dimension_values[0].value
        channel = row.dimension_values[1].value
        sessions = int(float(row.metric_values[0].value))
        engaged = int(float(row.metric_values[1].value))
        conv = float(row.metric_values[2].value)

        entry = by_path.setdefault(path, {
            "path": path, "sesiones": 0, "sesiones_engaged": 0,
            "sesiones_google_ads": 0, "sesiones_meta": 0, "sesiones_otros": 0,
            "conversiones_ga4": 0.0,
        })
        entry["sesiones"] += sessions
        entry["sesiones_engaged"] += engaged
        entry["conversiones_ga4"] += conv
        if channel == "Paid Search":
            entry["sesiones_google_ads"] += sessions
        elif channel in ("Paid Social", "Organic Social"):
            entry["sesiones_meta"] += sessions
        else:
            entry["sesiones_otros"] += sessions

    rows = []
    for entry in by_path.values():
        entry["tasa_interaccion"] = round(entry["sesiones_engaged"] / entry["sesiones"] * 100, 2) if entry["sesiones"] else 0
        entry["conversiones_ga4"] = round(entry["conversiones_ga4"], 1)
        del entry["sesiones_engaged"]
        rows.append(entry)
    return {"rows": rows}


# Los 3 eventos de formulario en juego (ver conversación 2026-08-31): son etapas
# SECUENCIALES del mismo embudo (empiezas a rellenar → le das a enviar → pasa la
# validación), no conversiones independientes — form_start siempre será ≥ Form Send
# ≥ form_submit. Se muestran los 3 en vez de elegir uno solo, mientras Jordi decide con
# Javier cuál usar como conversión "oficial" de Google Ads.
FORM_FUNNEL_EVENTS = ["form_start", "Form Send", "form_submit"]


def fetch_ga4_form_funnel(property_id: str, since: str, until: str, channel: str = "Paid Search") -> dict:
    """Cuenta de los 3 eventos de formulario en GA4, filtrados al canal indicado
    (por defecto 'Paid Search' = tráfico de Google Ads, para que encaje con el resto
    de KPIs de la pestaña Google Ads del dashboard)."""
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Dimension, Metric,
            FilterExpression, FilterExpressionList, Filter,
        )
    except ImportError:
        return {"error": "Paquete google-analytics-data no instalado."}

    try:
        creds = _get_ga4_credentials()
        client = BetaAnalyticsDataClient(credentials=creds)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="eventName")],
            metrics=[Metric(name="eventCount")],
            date_ranges=[DateRange(start_date=since, end_date=until)],
            dimension_filter=FilterExpression(
                and_group=FilterExpressionList(expressions=[
                    FilterExpression(filter=Filter(
                        field_name="eventName",
                        in_list_filter=Filter.InListFilter(values=FORM_FUNNEL_EVENTS),
                    )),
                    FilterExpression(filter=Filter(
                        field_name="sessionDefaultChannelGroup",
                        string_filter=Filter.StringFilter(value=channel),
                    )),
                ])
            ),
        )
        response = client.run_report(request)
    except Exception as e:
        return {"error": str(e)}

    counts = {name: 0 for name in FORM_FUNNEL_EVENTS}
    for row in response.rows:
        name = row.dimension_values[0].value
        if name in counts:
            counts[name] = int(float(row.metric_values[0].value))
    return {
        "form_start": counts["form_start"],
        "form_send": counts["Form Send"],
        "form_submit": counts["form_submit"],
        "channel": channel,
    }
