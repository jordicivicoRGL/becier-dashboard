import os
import json
import requests

META_API_VERSION = "v21.0"
META_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"


def _get_token() -> str:
    token = os.environ.get("META_ACCESS_TOKEN")
    if not token:
        raise ValueError("META_ACCESS_TOKEN no está configurado en .env")
    return token


def _get_account_id(account: str = "default") -> str:
    mapping = {
        "default": os.environ.get("META_AD_ACCOUNT_ID", ""),
        "becier": os.environ.get("META_AD_ACCOUNT_ID_BECIER", ""),
        "tago": os.environ.get("META_AD_ACCOUNT_ID_TAGO", ""),
        "skillgap": os.environ.get("META_AD_ACCOUNT_ID_SKILLGAP", ""),
        "diagonal": os.environ.get("META_AD_ACCOUNT_ID_DIAGONAL", ""),
    }
    aid = mapping.get(account.lower(), mapping["default"])
    if not aid:
        raise ValueError(f"No hay account ID configurado para '{account}'. Revisa el .env.")
    return aid if aid.startswith("act_") else f"act_{aid}"


def _appsecret_proof(token: str) -> str:
    import hmac, hashlib
    secret = os.environ.get("META_APP_SECRET", "")
    if not secret:
        return ""
    return hmac.new(secret.encode(), token.encode(), hashlib.sha256).hexdigest()

def _get(path: str, params: dict) -> dict:
    token = _get_token()
    params["access_token"] = token
    proof = _appsecret_proof(token)
    if proof:
        params["appsecret_proof"] = proof
    resp = requests.get(f"{META_BASE_URL}{path}", params=params, timeout=15)
    return resp.json()


def _post(path: str, data: dict) -> dict:
    data["access_token"] = _get_token()
    resp = requests.post(f"{META_BASE_URL}{path}", data=data, timeout=15)
    return resp.json()


def get_campaigns(account: str = "default", status_filter: str = "all") -> dict:
    """Lista campañas con estado y presupuesto."""
    try:
        account_id = _get_account_id(account)
        params = {
            "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,start_time,stop_time",
            "limit": 50,
        }
        if status_filter.lower() != "all":
            status_map = {"active": "ACTIVE", "paused": "PAUSED", "archived": "ARCHIVED"}
            status = status_map.get(status_filter.lower(), status_filter.upper())
            params["filtering"] = json.dumps([{"field": "effective_status", "operator": "IN", "value": [status]}])

        data = _get(f"/{account_id}/campaigns", params)
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        campaigns = []
        for c in data.get("data", []):
            campaigns.append({
                "id": c.get("id"),
                "name": c.get("name"),
                "status": c.get("status"),
                "effective_status": c.get("effective_status"),
                "objective": c.get("objective"),
                "daily_budget_eur": round(int(c["daily_budget"]) / 100, 2) if c.get("daily_budget") else None,
                "lifetime_budget_eur": round(int(c["lifetime_budget"]) / 100, 2) if c.get("lifetime_budget") else None,
                "start_time": c.get("start_time"),
                "stop_time": c.get("stop_time"),
            })
        return {"campaigns": campaigns, "total": len(campaigns), "account": account_id}

    except Exception as e:
        return {"error": str(e)}


def get_campaign_insights(campaign_id: str, date_preset: str = "last_30d") -> dict:
    """Métricas de una campaña: impresiones, clics, gasto, alcance, CPM, CPC, CTR."""
    try:
        params = {
            "fields": "campaign_name,impressions,clicks,spend,reach,cpm,cpc,ctr,frequency,actions",
            "date_preset": date_preset,
            "level": "campaign",
        }
        data = _get(f"/{campaign_id}/insights", params)
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        insights = data.get("data", [])
        if not insights:
            return {"message": "Sin datos para el período", "campaign_id": campaign_id, "period": date_preset}

        i = insights[0]
        actions = {a["action_type"]: int(a["value"]) for a in i.get("actions", [])}
        return {
            "campaign_id": campaign_id,
            "campaign_name": i.get("campaign_name"),
            "period": date_preset,
            "impressions": int(i.get("impressions", 0)),
            "clicks": int(i.get("clicks", 0)),
            "spend_eur": float(i.get("spend", 0)),
            "reach": int(i.get("reach", 0)),
            "cpm": float(i.get("cpm", 0)),
            "cpc": float(i.get("cpc", 0)),
            "ctr_pct": float(i.get("ctr", 0)),
            "frequency": float(i.get("frequency", 0)),
            "actions": actions,
        }

    except Exception as e:
        return {"error": str(e)}


def get_account_insights(account: str = "default", date_preset: str = "last_30d") -> dict:
    """Métricas globales de la cuenta: gasto total, impresiones, clics, CPM, CPC, CTR."""
    try:
        account_id = _get_account_id(account)
        params = {
            "fields": "impressions,clicks,spend,reach,cpm,cpc,ctr,frequency",
            "date_preset": date_preset,
            "level": "account",
        }
        data = _get(f"/{account_id}/insights", params)
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        insights = data.get("data", [])
        if not insights:
            return {"message": "Sin datos para el período", "account": account_id, "period": date_preset}

        i = insights[0]
        return {
            "account": account_id,
            "period": date_preset,
            "impressions": int(i.get("impressions", 0)),
            "clicks": int(i.get("clicks", 0)),
            "spend_eur": float(i.get("spend", 0)),
            "reach": int(i.get("reach", 0)),
            "cpm": float(i.get("cpm", 0)),
            "cpc": float(i.get("cpc", 0)),
            "ctr_pct": float(i.get("ctr", 0)),
            "frequency": float(i.get("frequency", 0)),
        }

    except Exception as e:
        return {"error": str(e)}


def set_campaign_status(campaign_id: str, action: str) -> dict:
    """Activa o pausa una campaña. action: 'ACTIVE' | 'PAUSED'"""
    try:
        status = action.upper()
        if status not in ("ACTIVE", "PAUSED"):
            return {"error": "action debe ser 'ACTIVE' o 'PAUSED'"}

        data = _post(f"/{campaign_id}", {"status": status})
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        return {"success": True, "campaign_id": campaign_id, "new_status": status}

    except Exception as e:
        return {"error": str(e)}


def get_adsets(campaign_id: str) -> dict:
    """Lista los ad sets de una campaña con presupuesto y estado."""
    try:
        params = {
            "fields": "id,name,status,effective_status,daily_budget,lifetime_budget,optimization_goal,billing_event,bid_amount",
        }
        data = _get(f"/{campaign_id}/adsets", params)
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        adsets = []
        for a in data.get("data", []):
            adsets.append({
                "id": a.get("id"),
                "name": a.get("name"),
                "status": a.get("status"),
                "effective_status": a.get("effective_status"),
                "daily_budget_eur": round(int(a["daily_budget"]) / 100, 2) if a.get("daily_budget") else None,
                "lifetime_budget_eur": round(int(a["lifetime_budget"]) / 100, 2) if a.get("lifetime_budget") else None,
                "optimization_goal": a.get("optimization_goal"),
                "billing_event": a.get("billing_event"),
            })
        return {"adsets": adsets, "total": len(adsets), "campaign_id": campaign_id}

    except Exception as e:
        return {"error": str(e)}


def get_campaigns_insights_range(account: str = "becier", since: str = None, until: str = None) -> dict:
    """
    Insights de todas las campañas en un rango de fechas personalizado.
    since/until en formato 'YYYY-MM-DD'.
    """
    try:
        account_id = _get_account_id(account)
        params = {
            "fields": "campaign_id,campaign_name,impressions,inline_link_clicks,spend,reach,cpm,cpc,inline_link_click_ctr,frequency,actions",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "campaign",
            "limit": 200,
        }
        data = _get(f"/{account_id}/insights", params)

        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        campaigns = []
        for i in data.get("data", []):
            actions = {a["action_type"]: int(float(a["value"])) for a in i.get("actions", [])}
            campaigns.append({
                "campaign_id": i.get("campaign_id"),
                "campaign_name": i.get("campaign_name", ""),
                "impressions": int(i.get("impressions", 0)),
                "clicks": int(i.get("inline_link_clicks", 0)),
                "spend_eur": float(i.get("spend", 0)),
                "reach": int(i.get("reach", 0)),
                "cpm": float(i.get("cpm", 0)),
                "cpc": float(i.get("cpc", 0)),
                "ctr_pct": float(i.get("inline_link_click_ctr", 0)),
                "frequency": float(i.get("frequency", 0)),
                "actions": actions,
            })

        return {"campaigns": campaigns, "period": f"{since}/{until}", "total": len(campaigns)}

    except Exception as e:
        return {"error": str(e)}


def get_ads(adset_id: str) -> dict:
    """Lista los anuncios de un ad set con estado y datos del creativo."""
    try:
        params = {
            "fields": "id,name,status,effective_status,creative{name,title,body,image_url}",
        }
        data = _get(f"/{adset_id}/ads", params)
        if "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}

        ads = []
        for a in data.get("data", []):
            creative = a.get("creative", {})
            ads.append({
                "id": a.get("id"),
                "name": a.get("name"),
                "status": a.get("status"),
                "effective_status": a.get("effective_status"),
                "creative_name": creative.get("name"),
                "creative_title": creative.get("title"),
                "creative_body": creative.get("body"),
            })
        return {"ads": ads, "total": len(ads), "adset_id": adset_id}

    except Exception as e:
        return {"error": str(e)}
