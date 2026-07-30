"""
Parseo de nomenclatura de campañas (Meta Ads y Google Ads).

Fuente única de verdad compartida entre dashboard_becier.py y la skill
/reporte-meta, para que ambos clasifiquen vertical/objetivo igual.

Formato Meta (Becier):  AND_PROS_[VERTICAL]_[NOMBRE ESPECIAL opcional]_[OBJETIVO]
  Ej: AND_PROS_VEHICLES_RENAULT-DAYS_LEAD AD
Formato Google:         [TIPO]_[OBJETIVO]_[VERTICAL]_[NOMBRE]
"""

import re

VERTICAL_MAP = {
    "VEHICLES":            "Vehicles",
    "VO":                  "Vehicles",
    "VEHICLES-PLA-ENGEGA": "Vehicles",
    "VEHICLES-LEAD":       "Vehicles",
    "BECAR":               "Becar",
    "AVIS":                "Becar",
    "AVIS-BECAR":          "Becar",
    "BECSER":              "Becser",
    "GRUP":                "Grup Becier",
    "GRUP-BECIER":         "Grup Becier",
    "BECIER":              "Grup Becier",
    "OKSIO":               "Vehicles",
}

OBJETIVO_MAP = {
    "LEAD AD":    "Lead Ad",
    "LEAD":       "Lead Ad",
    "LE":         "Landing",
    "TRAFIC WEB": "Landing",
    "TRAFIC":     "Landing",
    "TRAFFIC":    "Landing",
    "ALCANCE":    "Impresiones",
    "REACH":      "Impresiones",
    "FOLLOWERS":  "Seguidores",
}

GOOGLE_CAMPAIGN_TYPES = {"SEARCH", "DISPLAY", "SHOPPING", "PMAX", "VIDEO",
                         "DSA", "PERFORMANCE", "SMART", "DISCOVERY"}

# Objetivo (ya normalizado por OBJETIVO_MAP) -> action_type(s) a leer del dict `actions`
# de las insights de Meta para contar "resultados". Es una lista porque Meta reporta
# el mismo evento bajo distintas claves según cómo esté montado el anuncio (ej. un Lead Ad
# con formulario instantáneo nativo puede salir como "lead" o como
# "onsite_conversion.lead_grouped"). Probar en orden y quedarse con la primera que exista
# evita reportar "0 resultados" por una clave equivocada en vez de por rendimiento real.
OBJETIVO_ACTION_TYPE = {
    "Lead Ad":     ["lead", "onsite_conversion.lead_grouped", "onsite_conversion.lead"],
    "Landing":     ["landing_page_view", "link_click"],
    "Impresiones": [],  # objetivo de alcance/impresiones no tiene action_type de resultado
    "Seguidores":  [],  # captación de seguidores no tiene action_type de resultado comparable
}


def pick_result_count(actions: dict, objetivo: str) -> int:
    """Devuelve el recuento de 'resultados' de una campaña probando, en orden, los
    action_type candidatos del objetivo detectado. 0 si ninguno aparece en `actions`."""
    for action_type in OBJETIVO_ACTION_TYPE.get(objetivo, []):
        if action_type in actions:
            return actions[action_type]
    return 0


def parse_campaign_parts(name: str) -> dict:
    """Extrae Vertical y Objetivo según el formato del nombre de campaña.
    Meta:   AND_PROS_[VERTICAL]_[OBJETIVO]   -> vertical en pos 2, objetivo en pos 3+
    Google: [TIPO]_[OBJETIVO]_[VERTICAL]_... -> vertical en pos 2, objetivo en pos 1
    """
    parts = [p.strip() for p in name.split("_")]
    vertical = "Otros"
    objetivo = "—"

    if not parts:
        return {"vertical": vertical, "objetivo": objetivo}

    is_google_format = parts[0].upper() in GOOGLE_CAMPAIGN_TYPES

    if is_google_format:
        if len(parts) >= 2:
            objetivo = OBJETIVO_MAP.get(parts[1].upper(), parts[1].title())
        if len(parts) >= 3:
            vertical = VERTICAL_MAP.get(parts[2].upper(), parts[2].title())
    else:
        if len(parts) >= 3:
            v = parts[2].upper()
            vertical = VERTICAL_MAP.get(v, "Otros")
            if vertical == "Otros":
                for part in parts:
                    mapped = VERTICAL_MAP.get(part.upper()) or VERTICAL_MAP.get(part.upper().split("-")[0])
                    if mapped:
                        vertical = mapped
                        break

        if len(parts) >= 4:
            # El objetivo va al final del nombre, pero puede haber un nombre especial
            # de por medio (ej. VEHICLES_RENAULT-DAYS_LEAD_AD) que desplaza dónde empieza.
            # Por eso se prueba el sufijo completo desde cada posición posible (de más
            # larga a más corta) en vez de asumir que el objetivo empieza justo en pos 3.
            objetivo = None
            for start in range(3, len(parts)):
                suffix_parts = list(parts[start:])
                # Sufijos tipo "-2"/"-3" al final (ej. LEAD_AD-2) son variantes de
                # numeración de campaña, no parte del objetivo — se descartan antes
                # de intentar el match para que "LEAD AD-2" siga resolviendo a "Lead Ad".
                suffix_parts[-1] = re.sub(r"-\d+$", "", suffix_parts[-1])
                candidate = " ".join(suffix_parts).upper()
                candidate = OBJETIVO_MAP.get(candidate) or OBJETIVO_MAP.get(candidate.replace("-", " "))
                if candidate:
                    objetivo = candidate
                    break
            if objetivo is None:
                objetivo = parts[-1].title()

    return {"vertical": vertical, "objetivo": objetivo}
