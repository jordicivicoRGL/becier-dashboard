"""
Gestión automática del token de acceso de Meta Ads.

Uso:
  python tools/meta_token_manager.py            # comprueba y renueva si procede
  python tools/meta_token_manager.py --force    # fuerza el intercambio aunque no haya caducado
  python tools/meta_token_manager.py --check    # solo muestra info del token, sin renovar

Requisitos en .env:
  META_ACCESS_TOKEN   token actual
  META_APP_ID         ID de la app en developers.facebook.com
  META_APP_SECRET     secreto de la app
"""

import os
import sys
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)

API_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{API_VERSION}"
DAYS_BEFORE_RENEW = 10  # renueva si quedan menos de 10 días


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require(var: str) -> str:
    val = os.environ.get(var, "").strip()
    if not val:
        print(f"[ERROR] {var} no está configurado en .env")
        sys.exit(1)
    return val


def _update_env(new_token: str) -> None:
    """Reemplaza META_ACCESS_TOKEN en el archivo .env en disco."""
    text = ENV_PATH.read_text(encoding="utf-8")
    pattern = r"^META_ACCESS_TOKEN=.*$"
    replacement = f"META_ACCESS_TOKEN={new_token}"
    new_text, n = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if n == 0:
        new_text += f"\nMETA_ACCESS_TOKEN={new_token}\n"
    ENV_PATH.write_text(new_text, encoding="utf-8")
    os.environ["META_ACCESS_TOKEN"] = new_token


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def check_token(token: str, app_id: str, app_secret: str) -> dict:
    """Devuelve info del token via debug_token."""
    resp = requests.get(
        f"{GRAPH_BASE}/debug_token",
        params={
            "input_token": token,
            "access_token": f"{app_id}|{app_secret}",
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    if "error" in resp.json():
        raise RuntimeError(resp.json()["error"]["message"])
    return data


def exchange_token(current_token: str, app_id: str, app_secret: str) -> str:
    """Intercambia el token actual por un token de larga duración (60 días)."""
    resp = requests.get(
        f"{GRAPH_BASE}/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": current_token,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"]["message"])
    return data["access_token"]


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def run(force: bool = False, check_only: bool = False) -> None:
    token = _require("META_ACCESS_TOKEN")
    app_id = _require("META_APP_ID")
    app_secret = _require("META_APP_SECRET")

    print("Comprobando token actual...")
    info = check_token(token, app_id, app_secret)

    is_valid = info.get("is_valid", False)
    expires_at = info.get("expires_at", 0)  # timestamp Unix; 0 = no caduca
    scopes = info.get("scopes", [])

    if not is_valid:
        print("[AVISO] El token actual NO es válido o ya ha caducado.")
    else:
        print("[OK] Token válido.")

    if expires_at:
        exp_dt = datetime.fromtimestamp(expires_at, tz=timezone.utc)
        days_left = (exp_dt - datetime.now(tz=timezone.utc)).days
        print(f"  Caduca: {exp_dt.strftime('%Y-%m-%d %H:%M UTC')}  ({days_left} días restantes)")
    else:
        days_left = 9999
        print("  Caduca: nunca (token de sistema o larga duración sin expiración)")

    print(f"  Permisos: {', '.join(scopes)}")

    if check_only:
        return

    needs_renewal = force or not is_valid or days_left < DAYS_BEFORE_RENEW

    if not needs_renewal:
        print(f"\nNo es necesario renovar (quedan {days_left} días). Usa --force para forzarlo.")
        return

    print("\nRenovando token...")
    try:
        new_token = exchange_token(token, app_id, app_secret)
        _update_env(new_token)
        print("[OK] Token renovado y guardado en .env correctamente.")

        # Verifica el nuevo token
        new_info = check_token(new_token, app_id, app_secret)
        new_exp = new_info.get("expires_at", 0)
        if new_exp:
            new_dt = datetime.fromtimestamp(new_exp, tz=timezone.utc)
            print(f"     Nuevo token caduca: {new_dt.strftime('%Y-%m-%d %H:%M UTC')}")
    except Exception as e:
        print(f"[ERROR] No se pudo renovar el token: {e}")
        print("        Necesitas obtener un nuevo token manualmente en el Graph API Explorer.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gestor de token Meta Ads")
    parser.add_argument("--force", action="store_true", help="Fuerza la renovación aunque no haya caducado")
    parser.add_argument("--check", action="store_true", help="Solo muestra info del token, sin renovar")
    args = parser.parse_args()
    run(force=args.force, check_only=args.check)
