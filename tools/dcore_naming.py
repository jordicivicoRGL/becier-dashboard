# -*- coding: utf-8 -*-
"""
Clasificación de campañas y creatividades de Meta Ads para DCORE.

A diferencia de Becier, DCORE no tiene sub-marcas/verticales: es un único negocio
(reformas de lujo). Aquí "Tema" cumple el papel que "Vertical" cumple en Becier,
agrupando campañas por temática/ángulo comercial a partir de palabras clave
detectadas en el nombre real de campaña (ver scratch_dcore_campaigns.txt, extraído
de la cuenta el 2026-08-31).

Para creatividades: DCORE aún no tiene convención de nombres (los .mov/.MOV actuales
son nombres de archivo sueltos). parse_creative_name() implementa la convención
propuesta a Vero (ver clients/dcore.md y clients/_referencias/dcore_taxonomia_naming_creatividades.xlsx):
[ANGULO]_[LANDING]_[OBJETIVO]_[HOOK]_[FECHA]_[FORMATO] — FORMATO añadido el 2026-08-31
(dimensiones del creativo, ej. 1080X1080). Se acepta también el formato sin FORMATO
(5 campos) durante la transición mientras Vero termina de adoptar la convención nueva.
Si el nombre no encaja (todo lo histórico), devuelve "—" en los campos que no puede
extraer en vez de fallar.
"""

import re

# Las 5 "verticales del negocio" confirmadas por Jordi (2026-08-31): prácticamente toda
# campaña real de la cuenta contiene una de estas palabras. No debe existir bucket
# "Otros" — toda campaña no-boost cae en una de estas 5, usando "Reformas B2C" como
# vertical por defecto para cualquier campaña histórica/pausada que no matchee ninguna
# palabra clave específica (Healthy House, Real Estate, Interiorismo, Inversores,
# WhatsApp, Black Friday, Zonas Prime, etc. — ver clients/dcore.md).
# Orden importa: los más específicos primero (B2B antes que nada que pueda confundirse).
TEMA_KEYWORDS = [
    ("B2B",                "B2B"),
    ("COCINAS",            "Cocinas"),
    ("EVO",                "Evo"),
    ("LIVING",             "Living"),
]
TEMA_DEFAULT = "Reformas B2C"

# Landings activas confirmadas por Jordi (2026-08-31) — reciben tráfico sobre todo de
# Meta, por eso no siempre aparecen en el informe de landing_page_view de Google Ads
# (que solo reporta tráfico de Google Ads). Se usan como fila fija en la pestaña
# Landings del dashboard para que una landing real no "desaparezca" solo porque no tuvo
# gasto de Google Ads ese período — se muestra igualmente con sus datos en 0/—.
# Actualizar esta lista cuando se lance o retire una landing.
# Tercer campo = Tema al que pertenece (para que el filtro de Vertical del sidebar
# también filtre esta tabla) — es una asignación estática de referencia; si la landing
# SÍ tuvo tráfico real de Google Ads ese período, se usa el Tema de la campaña real en
# su lugar (más preciso), este valor es solo el fallback para cuando no hay datos.
KNOWN_LANDINGS = [
    ("/landing-sobrecostes/", "Sobrecostes", "Reformas B2C"),
    ("/reformas-chalets-premium/", "Chalets Premium", "Reformas B2C"),
    ("/landing-reformas-chalets/", "Reformas Chalets", "Reformas B2C"),
    ("/landing-evo/", "Evo", "Evo"),
    ("/landing-chalets-tier1/", "Chalets Tier 1", "Reformas B2C"),
    ("/landing-chalets-tier2/", "Chalets Tier 2", "Reformas B2C"),
]

# Campañas de impulso de publicaciones de Instagram (objetivo LINK_CLICKS boosteando
# un post orgánico): no siguen ninguna convención de nombre y son ruido para la toma
# de decisiones de campaña. Se agregan en un único bucket en vez de listarlas una a una.
_BOOST_PREFIXES = ("PUBLICACIÓN DE INSTAGRAM", "PUBLICACION DE INSTAGRAM",
                   "INSTAGRAM POST", "PUBLICATION INSTAGRAM")


def is_post_boost(campaign_name: str) -> bool:
    name = (campaign_name or "").strip().upper()
    return name.startswith(_BOOST_PREFIXES)


def classify_tema(campaign_name: str) -> str:
    """Detecta el tema/ángulo de una campaña DCORE a partir de palabras clave en su nombre.
    Nunca devuelve 'Otros': lo que no matchea una palabra clave específica cae en
    TEMA_DEFAULT (Reformas B2C, la vertical general del negocio)."""
    name = (campaign_name or "").upper()
    for keyword, label in TEMA_KEYWORDS:
        if keyword in name:
            return label
    return TEMA_DEFAULT


TEMA_STYLES = {
    "B2B":            "tag-b2b",
    "Cocinas":        "tag-cocinas",
    "Evo":            "tag-evo",
    "Living":         "tag-living",
    "Reformas B2C":   "tag-reformas",
}


def parse_creative_name(ad_name: str) -> dict:
    """Intenta parsear la convención [ANGULO]_[LANDING]_[OBJETIVO]_[HOOK]_[FECHA].
    Devuelve '—' en los campos que no pueda extraer (todo el histórico actual, con
    nombres de archivo .mov sueltos, cae aquí hasta que se adopte la convención)."""
    name = (ad_name or "").strip()
    # Quita extensión de vídeo si la lleva pegada al final
    name_no_ext = re.sub(r"\.(mov|mp4|MOV|MP4)$", "", name)
    parts = [p.strip() for p in name_no_ext.split("_") if p.strip()]
    if len(parts) < 5:
        return {"angulo": "—", "landing": "—", "objetivo": "—", "hook": "—", "fecha": "—", "formato": "—", "parseado": False}
    angulo, landing, objetivo, hook = parts[0], parts[1], parts[2], parts[3]
    fecha = parts[4] if re.fullmatch(r"\d{8}", parts[4]) else "—"
    # FORMATO (6º campo, ej. 1080X1080) es opcional durante la transición: nombres
    # antiguos de 5 campos siguen parseando bien, solo sin dimensiones.
    formato = "—"
    if len(parts) >= 6 and re.fullmatch(r"\d{3,4}X\d{3,4}", parts[5].upper()):
        formato = parts[5].upper()
    return {
        "angulo": angulo.replace("-", " ").title(),
        "landing": landing.replace("-", " ").title(),
        "objetivo": objetivo.title(),
        "hook": hook.replace("-", " ").title(),
        "fecha": fecha,
        "formato": formato,
        "parseado": True,
    }
