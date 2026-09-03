# -*- coding: utf-8 -*-
"""
Clasificación aproximada de códigos postales de Madrid para el dashboard DCORE.

Objetivo del cliente: los leads de reforma solo son útiles dentro de Madrid capital
(idealmente dentro de la M-30) o, como segunda opción, en el resto de la Comunidad
de Madrid. Fuera de la Comunidad de Madrid no hay operativa (ver clients/dcore.md).

IMPORTANTE — esto es una aproximación, no una geometría real:
- La M-30 es un anillo viario, no coincide con los límites de ningún código postal.
- M30_POSTAL_CODES es una lista curada a mano de los CP de Madrid capital que quedan
  mayoritariamente DENTRO del anillo (barrios centrales). Un CP fronterizo puede tener
  parte de su superficie fuera. Ajustar esta lista si el negocio lo requiere.
- Las coordenadas son centroides aproximados del distrito postal (no la dirección
  exacta del lead), solo para poder pintar un punto en el mapa.
"""

# CP de Madrid capital considerados mayoritariamente dentro de la M-30.
M30_POSTAL_CODES = {
    "28001", "28002", "28003", "28004", "28005", "28006", "28007", "28008",
    "28009", "28010", "28012", "28013", "28014", "28015", "28016", "28019",
    "28020", "28028", "28029", "28033", "28036", "28039", "28045", "28046",
}

# Centroides aproximados (lat, lon) de códigos postales de Madrid capital y
# algunos municipios frecuentes de la Comunidad de Madrid (zona de operación DCORE).
POSTAL_CENTROIDS = {
    "28001": (40.4256, -3.6836), "28002": (40.4478, -3.6763),
    "28003": (40.4462, -3.7038), "28004": (40.4230, -3.6997),
    "28005": (40.4093, -3.7132), "28006": (40.4340, -3.6822),
    "28007": (40.4083, -3.6763), "28008": (40.4265, -3.7159),
    "28009": (40.4136, -3.6763), "28010": (40.4340, -3.6950),
    "28011": (40.4136, -3.7413), "28012": (40.4095, -3.7025),
    "28013": (40.4190, -3.7100), "28014": (40.4145, -3.6970),
    "28015": (40.4370, -3.7057), "28016": (40.4550, -3.6790),
    "28017": (40.4420, -3.6480), "28018": (40.4020, -3.6000),
    "28019": (40.3850, -3.7280), "28020": (40.4530, -3.7010),
    "28023": (40.4550, -3.7710), "28024": (40.3820, -3.7420),
    "28025": (40.3630, -3.7130), "28026": (40.3880, -3.6960),
    "28027": (40.4370, -3.6300), "28028": (40.4290, -3.6690),
    "28029": (40.4680, -3.6980), "28030": (40.4070, -3.6470),
    "28031": (40.3820, -3.6270), "28032": (40.4290, -3.6050),
    "28033": (40.4670, -3.6510), "28034": (40.4820, -3.7060),
    "28035": (40.4790, -3.7280), "28036": (40.4460, -3.6790),
    "28037": (40.4290, -3.6570), "28038": (40.3940, -3.6570),
    "28039": (40.4610, -3.7080), "28040": (40.4560, -3.7100),
    "28041": (40.3510, -3.6990), "28042": (40.4720, -3.5810),
    "28043": (40.4410, -3.6480), "28044": (40.3480, -3.6850),
    "28045": (40.3960, -3.6960), "28046": (40.4610, -3.6830),
    "28047": (40.3910, -3.7150), "28050": (40.4980, -3.6600),
    "28051": (40.3630, -3.6180), "28052": (40.4010, -3.5820),
    "28053": (40.4310, -3.5920),
    # Municipios de la Comunidad de Madrid frecuentes en la zona operativa DCORE
    "28223": (40.4320, -3.8140),  # Pozuelo de Alarcón
    "28224": (40.4460, -3.7930),  # Pozuelo (Húmera)
    "28230": (40.4820, -3.8730),  # Las Rozas
    "28231": (40.4920, -3.8850),  # Las Rozas (Molino de la Hoz)
    "28109": (40.5320, -3.6350),  # Alcobendas
    "28791": (40.5900, -3.6180),  # Soto del Real (sierra)
    "28760": (40.7700, -3.8630),  # Tres Cantos
    "28925": (40.3230, -3.7660),  # Alcorcón
    "28931": (40.3220, -3.8650),  # Móstoles
    "28660": (40.4010, -3.8570),  # Boadilla del Monte
    "28680": (40.2830, -4.0130),  # San Martín de Valdeiglesias (sierra oeste)
    "28801": (40.4820, -3.3640),  # Alcalá de Henares
}


def classify_postal_code(cp: str) -> str:
    """Clasifica un CP en 'Dentro M-30' / 'Fuera M-30 (Madrid/CM)' / 'Fuera de la Comunidad de Madrid' / 'CP inválido'."""
    cp = (cp or "").strip()[:5]
    if len(cp) != 5 or not cp.isdigit():
        return "CP inválido"
    if not cp.startswith("28"):
        return "Fuera de la Comunidad de Madrid"
    if cp in M30_POSTAL_CODES:
        return "Dentro M-30"
    return "Fuera M-30 (Madrid/CM)"


def postal_coords(cp: str):
    """Devuelve (lat, lon) aproximados del CP, o None si no está en la tabla."""
    cp = (cp or "").strip()[:5]
    return POSTAL_CENTROIDS.get(cp)


ZONE_COLOR = {
    "Dentro M-30": "#4fc870",
    "Fuera M-30 (Madrid/CM)": "#fbbf24",
    "Fuera de la Comunidad de Madrid": "#f87171",
    "CP inválido": "#5a6080",
}
