"""
Schmaler Home-Assistant-Client. Hält den Token serverseitig – er verlässt
den Server nie Richtung Browser.
"""
import os
import httpx

HA_URL = os.environ.get("HA_URL", "").rstrip("/")
HA_TOKEN = os.environ.get("HA_TOKEN", "")

_TIMEOUT = httpx.Timeout(15.0)


class HAError(Exception):
    pass


def _headers():
    if not HA_URL or not HA_TOKEN:
        raise HAError("HA_URL oder HA_TOKEN nicht gesetzt (in Coolify als Env eintragen).")
    return {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}


async def _client():
    return httpx.AsyncClient(base_url=HA_URL, headers=_headers(), timeout=_TIMEOUT)


async def get_states():
    async with await _client() as c:
        r = await c.get("/api/states")
        r.raise_for_status()
        return r.json()


async def get_state(entity_id: str):
    async with await _client() as c:
        r = await c.get(f"/api/states/{entity_id}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()


async def call_service(domain: str, service: str, data: dict):
    async with await _client() as c:
        r = await c.post(f"/api/services/{domain}/{service}", json=data)
        r.raise_for_status()
        return r.json()


async def list_automation_states():
    states = await get_states()
    out = []
    for s in states:
        if s["entity_id"].startswith("automation."):
            attrs = s.get("attributes", {})
            out.append({
                "entity_id": s["entity_id"],
                "id": attrs.get("id"),
                "name": attrs.get("friendly_name", s["entity_id"]),
                "state": s["state"],
                "last_triggered": attrs.get("last_triggered"),
            })
    out.sort(key=lambda a: (a["name"] or "").lower())
    return out


async def get_automation_config(auto_id: str):
    async with await _client() as c:
        r = await c.get(f"/api/config/automation/config/{auto_id}")
        r.raise_for_status()
        return r.json()


async def save_automation_config(auto_id: str, config: dict):
    async with await _client() as c:
        r = await c.post(f"/api/config/automation/config/{auto_id}", json=config)
        r.raise_for_status()
        # Automationen neu laden, damit die Änderung sofort greift
        await c.post("/api/services/automation/reload", json={})
        return r.json()


async def ping():
    """True, wenn HA erreichbar und Token gültig ist."""
    try:
        async with await _client() as c:
            r = await c.get("/api/")
            return r.status_code == 200
    except Exception:
        return False
