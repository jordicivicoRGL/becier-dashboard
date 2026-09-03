# -*- coding: utf-8 -*-
"""
Integración con la Data Export API de Microsoft Clarity para DCORE.

Limitaciones reales de la API (no son un bug nuestro, son del producto):
  - Solo agrega los últimos 1, 2 o 3 días — sin rango histórico ni período elegible.
  - Límite de 10 peticiones/día por proyecto de Clarity.

Por eso NUNCA se llama en directo desde el dashboard (@st.cache_data no basta: se
resetea en cada redeploy/reinicio y volvería a gastar la cuota). Se cachea en disco
(outputs/dcore/clarity_cache.json) y solo se refresca cuando alguien pulsa el botón
"Actualizar Clarity" en el dashboard — nunca automáticamente.

Configuración pendiente (Jordi): CLARITY_API_TOKEN_DCORE y CLARITY_PROJECT_ID_DCORE en .env
(Clarity → proyecto dcore.es → Settings → Data Export → Generate new API token).
"""
import os
import json
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

CACHE_PATH = Path(__file__).parent.parent / "outputs" / "dcore" / "clarity_cache.json"
QUOTA_PATH = Path(__file__).parent.parent / "outputs" / "dcore" / "clarity_quota.json"
CLARITY_API_URL = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
DAILY_QUOTA = 10

# Métricas priorizadas para "salud de landing" (ver conversación 2026-08-31):
# Rage Clicks y Quickback Clicks son las de mayor valor accionable, Scroll Depth y
# Dead Clicks las siguientes. El resto de métricas que devuelve Clarity no se muestran
# porque no aportan una decisión clara para DCORE.
# Cada métrica guarda su valor en un campo distinto dentro de "information" (confirmado
# inspeccionando la respuesta real de la API el 2026-08-31, la documentación no lo detalla
# con precisión): los "*ClickCount"/"QuickbackClick" usan "subTotal" (recuento de sesiones
# con ese evento), ScrollDepth usa "averageScrollDepth" (% medio).
_METRIC_CONFIG = {
    "RageClickCount": {"label": "Rage clicks", "value_field": "subTotal"},
    "QuickbackClick": {"label": "Quickback clicks", "value_field": "subTotal"},
    "ScrollDepth":    {"label": "Scroll depth medio", "value_field": "averageScrollDepth"},
    "DeadClickCount": {"label": "Dead clicks", "value_field": "subTotal"},
}


def is_configured() -> bool:
    return bool(os.environ.get("CLARITY_API_TOKEN_DCORE") and os.environ.get("CLARITY_PROJECT_ID_DCORE"))


def _read_cache() -> dict | None:
    if not CACHE_PATH.exists():
        return None
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_cache(data: dict):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_quota_status() -> dict:
    """Peticiones ya gastadas hoy, contadas localmente (Clarity no expone la cuota
    restante en la respuesta de la API, así que la llevamos nosotros). Se resetea solo
    por cambio de fecha, no hace falta ninguna acción manual."""
    today = time.strftime("%Y-%m-%d")
    if not QUOTA_PATH.exists():
        return {"date": today, "used": 0, "remaining": DAILY_QUOTA}
    try:
        with open(QUOTA_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"date": today, "used": 0, "remaining": DAILY_QUOTA}
    if data.get("date") != today:
        return {"date": today, "used": 0, "remaining": DAILY_QUOTA}
    used = data.get("used", 0)
    return {"date": today, "used": used, "remaining": max(DAILY_QUOTA - used, 0)}


def _record_quota_use():
    status = get_quota_status()
    QUOTA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(QUOTA_PATH, "w", encoding="utf-8") as f:
        json.dump({"date": status["date"], "used": status["used"] + 1}, f)


def get_cached_snapshot() -> dict:
    """Devuelve la última instantánea guardada en disco, o {'configured': False} /
    {'cached': False} si no hay ninguna todavía. Nunca llama a la API de Clarity."""
    if not is_configured():
        return {"configured": False}
    cache = _read_cache()
    if not cache:
        return {"configured": True, "cached": False}
    return {"configured": True, "cached": True, **cache}


def refresh_snapshot(num_days: int = 3) -> dict:
    """Llama a la API de Clarity (gasta 1 de las 10 peticiones/día) y sobrescribe la
    caché en disco. Solo debe invocarse desde una acción explícita del usuario
    (botón 'Actualizar Clarity'), nunca en un rerun automático del dashboard."""
    token = os.environ.get("CLARITY_API_TOKEN_DCORE", "")
    project_id = os.environ.get("CLARITY_PROJECT_ID_DCORE", "")
    if not token or not project_id:
        return {"error": "Clarity no configurado (falta CLARITY_API_TOKEN_DCORE o CLARITY_PROJECT_ID_DCORE en .env)."}

    quota = get_quota_status()
    if quota["remaining"] <= 0:
        return {"error": f"Límite de {DAILY_QUOTA} peticiones/día de Clarity ya consumido hoy. Vuelve a intentarlo mañana."}

    try:
        r = requests.get(
            CLARITY_API_URL,
            params={"numOfDays": num_days, "dimension1": "URL", "dimension2": "Device"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        _record_quota_use()  # cuenta el intento aunque falle: la petición ya se envió a Clarity
        if r.status_code == 429:
            return {"error": "Límite de 10 peticiones/día de Clarity alcanzado. Vuelve a intentarlo mañana."}
        r.raise_for_status()
        raw = r.json()
    except Exception as e:
        return {"error": str(e)}

    rows = []
    for entry in raw:
        metric_name = entry.get("metricName", "")
        config = _METRIC_CONFIG.get(metric_name)
        if not config:
            continue
        for info in entry.get("information", []):
            raw_url = info.get("Url", "—")
            path = urlparse(raw_url).path or "/" if raw_url != "—" else "—"
            rows.append({
                "metrica": config["label"],
                "url": path,
                "device": info.get("Device", "—"),
                "valor": info.get(config["value_field"], "—"),
            })

    # Agregar por (métrica, url, device): la API devuelve una fila por sesión/click
    # individual, no un total ya sumado — sin esto Rage/Dead clicks aparecen como
    # decenas de filas con valor 0 o 1 en vez de un total legible por landing.
    aggregated: dict[tuple, float] = {}
    for row in rows:
        key = (row["metrica"], row["url"], row["device"])
        try:
            val = float(row["valor"])
        except (TypeError, ValueError):
            continue
        if row["metrica"] == "Scroll depth medio":
            # Promedio, no suma: nos quedamos con el último valor visto para esta clave
            aggregated[key] = val
        else:
            aggregated[key] = aggregated.get(key, 0) + val
    rows = [{"metrica": m, "url": u, "device": d, "valor": round(v, 1)}
            for (m, u, d), v in sorted(aggregated.items(), key=lambda kv: (-kv[1], kv[0]))]

    snapshot = {"fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"), "num_days": num_days, "rows": rows}
    _write_cache(snapshot)
    return {"configured": True, "cached": True, **snapshot}
