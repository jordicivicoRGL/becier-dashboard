import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

DEVELOPER_TOKEN = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
CUSTOMER_ID = os.environ.get("GOOGLE_ADS_CUSTOMER_ID")

ACCOUNTS = {
    "becier": "1632468817",
    "diagonal": "1708585653",
}


def _build_client() -> GoogleAdsClient:
    import json
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    token_path = os.path.join(os.path.dirname(__file__), "..", "credentials", "token.json")
    client_secret_path = os.path.join(os.path.dirname(__file__), "..", "credentials", "client_secret.json")

    with open(token_path) as f:
        token_data = json.load(f)
    with open(client_secret_path) as f:
        secret_data = json.load(f)

    web_or_installed = secret_data.get("web") or secret_data.get("installed")

    credentials = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=web_or_installed["client_id"],
        client_secret=web_or_installed["client_secret"],
        scopes=token_data.get("scopes"),
    )

    # Siempre refrescar para garantizar token válido en ejecuciones automáticas
    credentials.refresh(Request())
    token_data["token"] = credentials.token
    token_data["expiry"] = credentials.expiry.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(token_path, "w") as f:
        json.dump(token_data, f)

    return GoogleAdsClient(
        credentials=credentials,
        developer_token=DEVELOPER_TOKEN,
        login_customer_id=LOGIN_CUSTOMER_ID,
        use_proto_plus=True,
    )


def get_campaigns_stats(date_range: str = "LAST_30_DAYS", account: str = "becier") -> dict:
    """Obtiene estadísticas de campañas: impresiones, clics, coste, conversiones."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE segments.date DURING {date_range}
            ORDER BY metrics.cost_micros DESC
        """

        response = ga_service.search(customer_id=customer_id, query=query)
        campaigns = []
        for row in response:
            campaigns.append({
                "id": row.campaign.id,
                "name": row.campaign.name,
                "status": row.campaign.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": row.metrics.conversions,
                "ctr_pct": round(row.metrics.ctr * 100, 2),
                "avg_cpc_eur": round(row.metrics.average_cpc / 1_000_000, 2),
            })

        return {"campaigns": campaigns, "total": len(campaigns), "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_campaigns_stats_range(since: str, until: str, account: str = "becier") -> dict:
    """Estadísticas de campañas en un rango de fechas personalizado. Fechas en formato YYYY-MM-DD."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE segments.date BETWEEN '{since}' AND '{until}'
            ORDER BY metrics.cost_micros DESC
        """

        response = ga_service.search(customer_id=customer_id, query=query)
        campaigns = []
        for row in response:
            campaigns.append({
                "id": row.campaign.id,
                "name": row.campaign.name,
                "status": row.campaign.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": row.metrics.conversions,
                "ctr_pct": round(row.metrics.ctr * 100, 2),
                "avg_cpc_eur": round(row.metrics.average_cpc / 1_000_000, 2),
            })

        return {"campaigns": campaigns, "total": len(campaigns), "period": f"{since}/{until}"}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def set_campaign_status(campaign_id: str, action: str, account: str = "becier") -> dict:
    """Activa o pausa una campaña. action: 'ENABLED' | 'PAUSED'"""
    try:
        client = _build_client()
        campaign_service = client.get_service("CampaignService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.update
        campaign.resource_name = campaign_service.campaign_path(customer_id, campaign_id)

        status_enum = client.enums.CampaignStatusEnum
        campaign.status = status_enum.ENABLED if action.upper() == "ENABLED" else status_enum.PAUSED

        from google.protobuf import field_mask_pb2
        campaign_operation.update_mask.CopyFrom(
            field_mask_pb2.FieldMask(paths=["status"])
        )

        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )
        result = response.results[0]
        return {
            "success": True,
            "campaign_resource": result.resource_name,
            "new_status": action.upper()
        }

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def create_campaign(name: str, daily_budget_eur: float, start_date: str = None, end_date: str = None, account: str = "becier") -> dict:
    """Crea una campaña de búsqueda con presupuesto diario. Fechas en formato YYYYMMDD."""
    try:
        client = _build_client()
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_service = client.get_service("CampaignService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        budget_operation = client.get_type("CampaignBudgetOperation")
        budget = budget_operation.create
        budget.name = f"Presupuesto {name}"
        budget.amount_micros = int(daily_budget_eur * 1_000_000)
        budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

        budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[budget_operation]
        )
        budget_resource = budget_response.results[0].resource_name

        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.create
        campaign.name = name
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
        campaign.campaign_budget = budget_resource
        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = True

        if start_date:
            campaign.start_date = start_date
        if end_date:
            campaign.end_date = end_date

        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
        result = campaign_response.results[0]
        return {
            "success": True,
            "campaign_resource": result.resource_name,
            "name": name,
            "daily_budget_eur": daily_budget_eur,
            "status": "PAUSED"
        }

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def delete_campaign(campaign_id: str, account: str = "becier") -> dict:
    """Elimina (remueve) una campaña permanentemente."""
    try:
        client = _build_client()
        campaign_service = client.get_service("CampaignService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        campaign_operation = client.get_type("CampaignOperation")
        resource_name = campaign_service.campaign_path(customer_id, campaign_id)
        campaign_operation.remove = resource_name

        response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
        return {
            "success": True,
            "removed_campaign": response.results[0].resource_name
        }

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}
