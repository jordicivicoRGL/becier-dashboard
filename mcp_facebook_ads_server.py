import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from tools.facebook_ads_tools import (
    get_campaigns,
    get_campaign_insights,
    get_account_insights,
    set_campaign_status,
    get_adsets,
    get_ads,
)

mcp = FastMCP("Facebook Ads")


@mcp.tool()
def fb_get_campaigns(account: str = "default", status_filter: str = "all") -> str:
    """Lista las campañas de Facebook/Instagram Ads con estado y presupuesto.
    status_filter: 'all' | 'active' | 'paused' | 'archived'
    account: 'default' usa META_AD_ACCOUNT_ID del .env
    """
    return str(get_campaigns(account=account, status_filter=status_filter))


@mcp.tool()
def fb_get_account_insights(account: str = "default", date_preset: str = "last_30d") -> str:
    """Métricas globales de la cuenta: gasto total, impresiones, clics, CPM, CPC, CTR, alcance.
    date_preset: today | yesterday | last_7d | last_14d | last_28d | last_30d | last_month | this_month | this_year
    """
    return str(get_account_insights(account=account, date_preset=date_preset))


@mcp.tool()
def fb_get_campaign_insights(campaign_id: str, date_preset: str = "last_30d") -> str:
    """Métricas de una campaña: impresiones, clics, gasto, alcance, CPM, CPC, CTR, conversiones.
    date_preset: today | yesterday | last_7d | last_14d | last_28d | last_30d | last_month | this_month | this_year
    """
    return str(get_campaign_insights(campaign_id=campaign_id, date_preset=date_preset))


@mcp.tool()
def fb_set_campaign_status(campaign_id: str, action: str) -> str:
    """Activa o pausa una campaña de Facebook/Instagram Ads.
    action: 'ACTIVE' para activar, 'PAUSED' para pausar.
    """
    return str(set_campaign_status(campaign_id=campaign_id, action=action))


@mcp.tool()
def fb_get_adsets(campaign_id: str) -> str:
    """Lista los conjuntos de anuncios (ad sets) de una campaña con presupuesto, estado y objetivo."""
    return str(get_adsets(campaign_id=campaign_id))


@mcp.tool()
def fb_get_ads(adset_id: str) -> str:
    """Lista los anuncios individuales de un ad set con estado y datos del creativo."""
    return str(get_ads(adset_id=adset_id))


if __name__ == "__main__":
    mcp.run()
