import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from tools.ads_tools import get_campaigns_stats, set_campaign_status, create_campaign, delete_campaign

mcp = FastMCP("Google Ads")


@mcp.tool()
def ads_get_campaigns_stats(date_range: str = "LAST_30_DAYS", account: str = "becier") -> str:
    """Obtiene estadísticas de campañas de Google Ads: impresiones, clics, coste, conversiones, CTR y CPC.
    date_range: LAST_7_DAYS | LAST_14_DAYS | LAST_30_DAYS | THIS_MONTH | LAST_MONTH | THIS_YEAR
    account: 'becier' para Grup Becier, 'diagonal' para Benítez Gomà / Diagonal CQ
    """
    return str(get_campaigns_stats(date_range=date_range, account=account))


@mcp.tool()
def ads_set_campaign_status(campaign_id: str, action: str, account: str = "becier") -> str:
    """Activa o pausa una campaña de Google Ads.
    action: 'ENABLED' para activar, 'PAUSED' para pausar.
    account: 'becier' o 'diagonal'
    """
    return str(set_campaign_status(campaign_id=campaign_id, action=action, account=account))


@mcp.tool()
def ads_create_campaign(name: str, daily_budget_eur: float, account: str = "becier", start_date: str = "", end_date: str = "") -> str:
    """Crea una nueva campaña de búsqueda en Google Ads en estado PAUSED.
    account: 'becier' o 'diagonal'
    start_date y end_date en formato YYYYMMDD (opcional).
    """
    kwargs = {"name": name, "daily_budget_eur": daily_budget_eur, "account": account}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return str(create_campaign(**kwargs))


@mcp.tool()
def ads_delete_campaign(campaign_id: str, account: str = "becier") -> str:
    """Elimina permanentemente una campaña de Google Ads. Acción irreversible.
    account: 'becier' o 'diagonal'
    """
    return str(delete_campaign(campaign_id=campaign_id, account=account))


if __name__ == "__main__":
    mcp.run()
