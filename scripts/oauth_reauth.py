# -*- coding: utf-8 -*-
"""Reautentica y guarda el token con los scopes actuales, sin abrir navegador automáticamente."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from google_auth_oauthlib.flow import InstalledAppFlow
from tools.calendar_tools import SCOPES, CLIENT_SECRET_PATH, TOKEN_PATH

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
creds = flow.run_local_server(port=0, open_browser=False)

TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(TOKEN_PATH, "w") as f:
    f.write(creds.to_json())

print("TOKEN_OK")
