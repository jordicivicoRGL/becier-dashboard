import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

DEVELOPER_TOKEN = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
CUSTOMER_ID = os.environ.get("GOOGLE_ADS_CUSTOMER_ID")

ACCOUNTS = {
    "becier": "1632468817",       # Grup Becier Bona
    "diagonal": "1708585653",     # BENITEZ GOMA (Diagonal CQ)
    "dcore": "1829150362",        # Dcore Group
    "properfy": "3929043521",     # Properfy
    "tago": "2976338027",         # Client - Tago
    "bloome": "4199711613",       # Bloome
    "egos": "1547712696",         # Clínica EGOS 2024
}


def _build_client() -> GoogleAdsClient:
    import json
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    std_token = os.path.join(os.path.dirname(__file__), "..", "credentials", "token.json")
    std_secret = os.path.join(os.path.dirname(__file__), "..", "credentials", "client_secret.json")
    token_path = std_token if os.path.exists(std_token) else "/tmp/token.json"
    client_secret_path = std_secret if os.path.exists(std_secret) else "/tmp/client_secret.json"

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


def get_account_summary(date_range: str = "LAST_30_DAYS", account: str = "becier") -> dict:
    """Resumen a nivel de cuenta: totales, nº de campañas activas, conversiones y coste por conversión."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = f"""
            SELECT
                customer.descriptive_name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.ctr
            FROM campaign
            WHERE segments.date DURING {date_range}
        """
        response = ga_service.search(customer_id=customer_id, query=query)

        totals = {"impressions": 0, "clicks": 0, "cost_micros": 0, "conversions": 0.0, "conversions_value": 0.0}
        active_campaigns = set()
        account_name = None
        for row in response:
            account_name = row.customer.descriptive_name
            if row.campaign.status.name == "ENABLED":
                active_campaigns.add(row.campaign.id)
            totals["impressions"] += row.metrics.impressions
            totals["clicks"] += row.metrics.clicks
            totals["cost_micros"] += row.metrics.cost_micros
            totals["conversions"] += row.metrics.conversions
            totals["conversions_value"] += row.metrics.conversions_value

        cost_eur = round(totals["cost_micros"] / 1_000_000, 2)
        conversions = round(totals["conversions"], 2)

        return {
            "account_name": account_name,
            "period": date_range,
            "active_campaigns": len(active_campaigns),
            "impressions": totals["impressions"],
            "clicks": totals["clicks"],
            "cost_eur": cost_eur,
            "ctr_pct": round((totals["clicks"] / totals["impressions"] * 100), 2) if totals["impressions"] else 0,
            "conversions": conversions,
            "conversions_value": round(totals["conversions_value"], 2),
            "cost_per_conversion_eur": round(cost_eur / conversions, 2) if conversions else None,
        }

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_ad_groups_stats(date_range: str = "LAST_30_DAYS", account: str = "becier", campaign_id: str = None) -> dict:
    """Estadísticas por grupo de anuncios: impresiones, clics, coste, conversiones, CTR, CPC medio."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        where_extra = f" AND campaign.id = {campaign_id}" if campaign_id else ""
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM ad_group
            WHERE segments.date DURING {date_range}{where_extra}
            ORDER BY metrics.cost_micros DESC
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        ad_groups = []
        for row in response:
            ad_groups.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "ad_group_id": row.ad_group.id,
                "ad_group_name": row.ad_group.name,
                "status": row.ad_group.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(row.metrics.conversions, 2),
                "ctr_pct": round(row.metrics.ctr * 100, 2),
                "avg_cpc_eur": round(row.metrics.average_cpc / 1_000_000, 2),
            })
        return {"ad_groups": ad_groups, "total": len(ad_groups), "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_keywords_stats(date_range: str = "LAST_30_DAYS", account: str = "becier", campaign_id: str = None) -> dict:
    """Palabras clave con métricas y Quality Score (score, CTR esperado, relevancia del anuncio, experiencia de landing)."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        where_extra = f" AND campaign.id = {campaign_id}" if campaign_id else ""
        query = f"""
            SELECT
                campaign.name,
                ad_group.name,
                ad_group_criterion.criterion_id,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group_criterion.status,
                ad_group_criterion.quality_info.quality_score,
                ad_group_criterion.quality_info.creative_quality_score,
                ad_group_criterion.quality_info.post_click_quality_score,
                ad_group_criterion.quality_info.search_predicted_ctr,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM keyword_view
            WHERE segments.date DURING {date_range}{where_extra}
            ORDER BY metrics.cost_micros DESC
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        keywords = []
        for row in response:
            qi = row.ad_group_criterion.quality_info
            keywords.append({
                "campaign_name": row.campaign.name,
                "ad_group_name": row.ad_group.name,
                "keyword": row.ad_group_criterion.keyword.text,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "status": row.ad_group_criterion.status.name,
                "quality_score": qi.quality_score if qi.quality_score else None,
                "creative_quality": qi.creative_quality_score.name if qi.creative_quality_score else None,
                "landing_page_experience": qi.post_click_quality_score.name if qi.post_click_quality_score else None,
                "expected_ctr": qi.search_predicted_ctr.name if qi.search_predicted_ctr else None,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(row.metrics.conversions, 2),
                "ctr_pct": round(row.metrics.ctr * 100, 2),
                "avg_cpc_eur": round(row.metrics.average_cpc / 1_000_000, 2),
            })
        return {"keywords": keywords, "total": len(keywords), "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_search_terms_report(date_range: str = "LAST_30_DAYS", account: str = "becier", campaign_id: str = None) -> dict:
    """Términos de búsqueda reales que activaron anuncios, con coste y conversiones — clave para detectar gasto desperdiciado y negativas nuevas."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        where_extra = f" AND campaign.id = {campaign_id}" if campaign_id else ""
        query = f"""
            SELECT
                campaign.name,
                ad_group.name,
                search_term_view.search_term,
                search_term_view.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM search_term_view
            WHERE segments.date DURING {date_range}{where_extra}
            ORDER BY metrics.cost_micros DESC
            LIMIT 200
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        search_terms = []
        for row in response:
            search_terms.append({
                "campaign_name": row.campaign.name,
                "ad_group_name": row.ad_group.name,
                "search_term": row.search_term_view.search_term,
                "status": row.search_term_view.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(row.metrics.conversions, 2),
                "ctr_pct": round(row.metrics.ctr * 100, 2),
            })
        return {"search_terms": search_terms, "total": len(search_terms), "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_ads_performance(date_range: str = "LAST_30_DAYS", account: str = "becier", campaign_id: str = None) -> dict:
    """Anuncios RSA con Ad Strength, nº de títulos/descripciones activos y métricas de rendimiento."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        where_extra = f" AND campaign.id = {campaign_id}" if campaign_id else ""
        query = f"""
            SELECT
                campaign.name,
                ad_group.name,
                ad_group_ad.ad.id,
                ad_group_ad.ad.responsive_search_ad.headlines,
                ad_group_ad.ad.responsive_search_ad.descriptions,
                ad_group_ad.ad_strength,
                ad_group_ad.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM ad_group_ad
            WHERE segments.date DURING {date_range}
                AND ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD{where_extra}
            ORDER BY metrics.cost_micros DESC
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        ads = []
        for row in response:
            rsa = row.ad_group_ad.ad.responsive_search_ad
            ads.append({
                "campaign_name": row.campaign.name,
                "ad_group_name": row.ad_group.name,
                "ad_id": row.ad_group_ad.ad.id,
                "ad_strength": row.ad_group_ad.ad_strength.name if row.ad_group_ad.ad_strength else None,
                "status": row.ad_group_ad.status.name,
                "num_headlines": len(rsa.headlines),
                "num_descriptions": len(rsa.descriptions),
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost_eur": round(row.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(row.metrics.conversions, 2),
                "ctr_pct": round(row.metrics.ctr * 100, 2),
            })
        return {"ads": ads, "total": len(ads), "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_extensions_coverage(account: str = "becier") -> dict:
    """Cobertura de extensiones (assets) activas a nivel de cuenta y campaña: sitelinks, callouts, structured snippets, llamada, ubicación, etc."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = """
            SELECT
                campaign.name,
                asset.type,
                campaign_asset.status
            FROM campaign_asset
            WHERE campaign_asset.status = 'ENABLED'
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        coverage = {}
        for row in response:
            campaign_name = row.campaign.name
            asset_type = row.asset.type_.name
            coverage.setdefault(campaign_name, {})
            coverage[campaign_name][asset_type] = coverage[campaign_name].get(asset_type, 0) + 1

        return {"coverage_by_campaign": coverage}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_device_performance(date_range: str = "LAST_30_DAYS", account: str = "becier") -> dict:
    """Rendimiento segmentado por dispositivo (móvil, ordenador, tablet)."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = f"""
            SELECT
                segments.device,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE segments.date DURING {date_range}
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        devices = {}
        for row in response:
            device = row.segments.device.name
            d = devices.setdefault(device, {"impressions": 0, "clicks": 0, "cost_micros": 0, "conversions": 0.0})
            d["impressions"] += row.metrics.impressions
            d["clicks"] += row.metrics.clicks
            d["cost_micros"] += row.metrics.cost_micros
            d["conversions"] += row.metrics.conversions

        result = {}
        for device, d in devices.items():
            result[device] = {
                "impressions": d["impressions"],
                "clicks": d["clicks"],
                "cost_eur": round(d["cost_micros"] / 1_000_000, 2),
                "conversions": round(d["conversions"], 2),
                "ctr_pct": round((d["clicks"] / d["impressions"] * 100), 2) if d["impressions"] else 0,
            }
        return {"by_device": result, "period": date_range}

    except GoogleAdsException as ex:
        errors = [e.message for e in ex.failure.errors]
        return {"error": f"Google Ads API error: {errors}"}
    except Exception as e:
        return {"error": str(e)}


def get_recommendations(account: str = "becier") -> dict:
    """Recomendaciones activas que Google Ads sugiere para la cuenta (tipo e impacto estimado)."""
    try:
        client = _build_client()
        ga_service = client.get_service("GoogleAdsService")
        customer_id = ACCOUNTS.get(account.lower(), CUSTOMER_ID)

        query = """
            SELECT
                recommendation.type,
                recommendation.campaign,
                recommendation.dismissed
            FROM recommendation
            WHERE recommendation.dismissed = FALSE
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        recommendations = []
        for row in response:
            recommendations.append({
                "type": row.recommendation.type_.name,
                "campaign": row.recommendation.campaign,
            })
        return {"recommendations": recommendations, "total": len(recommendations)}

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
