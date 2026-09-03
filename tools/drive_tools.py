# -*- coding: utf-8 -*-
"""
Lectura de Google Drive (solo lectura) para enlazar los vídeos originales de las
creatividades de Meta Ads con su fila correspondiente en el dashboard de DCORE.

Requiere el scope 'drive.readonly' en el token OAuth compartido (credentials/token.json)
— añadido el 2026-08-31 junto con 'analytics.readonly'.
"""
import os
import re
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CREDENTIALS_DIR = os.path.join(os.path.dirname(__file__), "..", "credentials")
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, "token.json")
CLIENT_SECRET_PATH = os.path.join(CREDENTIALS_DIR, "client_secret.json")

DCORE_CREATIVES_FOLDER_ID = "1TvX09fRTOIev69PVSi1lVMc2AZgzZlmh"

VIDEO_MIME_PREFIXES = ("video/",)


def _get_drive_credentials() -> Credentials:
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


def _normalize(name: str) -> str:
    """Sube a mayúsculas y colapsa cualquier separador (espacio, guion, guion bajo,
    punto) a nada, para poder comparar 'COCINA GRATIS REBE .mov' con el nombre de
    anuncio de Meta que suele llevar guiones en vez de espacios."""
    base = re.sub(r"\.[a-zA-Z0-9]{2,4}$", "", name)  # quita extensión
    return re.sub(r"[\s\-_\.]+", "", base).upper()


def fetch_dcore_creative_videos() -> dict:
    """Lista (recursiva, incluye subcarpetas) todos los vídeos de la carpeta de
    creatividades de DCORE en Drive. Devuelve {'videos': [...]} o {'error': str}."""
    try:
        from googleapiclient.discovery import build
        creds = _get_drive_credentials()
        service = build("drive", "v3", credentials=creds)
    except Exception as e:
        return {"error": str(e)}

    videos = []
    try:
        folder_ids = [DCORE_CREATIVES_FOLDER_ID]
        seen_folders = set()
        while folder_ids:
            fid = folder_ids.pop()
            if fid in seen_folders:
                continue
            seen_folders.add(fid)
            page_token = None
            while True:
                resp = service.files().list(
                    q=f"'{fid}' in parents and trashed = false",
                    fields="nextPageToken, files(id, name, mimeType, webViewLink)",
                    pageSize=200, pageToken=page_token,
                ).execute()
                for f in resp.get("files", []):
                    if f["mimeType"] == "application/vnd.google-apps.folder":
                        folder_ids.append(f["id"])
                    elif f["mimeType"].startswith(VIDEO_MIME_PREFIXES):
                        videos.append({
                            "id": f["id"], "name": f["name"],
                            "url": f.get("webViewLink") or f"https://drive.google.com/file/d/{f['id']}/view",
                            "_norm": _normalize(f["name"]),
                        })
                page_token = resp.get("nextPageToken")
                if not page_token:
                    break
    except Exception as e:
        return {"error": str(e), "videos": videos}

    return {"videos": videos}


def match_video_link(ad_name: str, videos: list) -> str | None:
    """Empareja el nombre de un anuncio de Meta con un vídeo de Drive por coincidencia
    de nombre de archivo dentro del nombre del anuncio (Meta suele conservar el nombre
    de archivo original cuando el anuncio no sigue la convención de naming). Exige un
    mínimo de 8 caracteres normalizados para evitar falsos positivos con nombres cortos."""
    if not ad_name:
        return None
    norm_ad = _normalize(ad_name)
    best = None
    best_len = 0
    for v in videos:
        norm_v = v["_norm"]
        if len(norm_v) >= 8 and norm_v in norm_ad and len(norm_v) > best_len:
            best = v["url"]
            best_len = len(norm_v)
    return best
