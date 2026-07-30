"""
Haus-Cockpit – vereinfachte Home-Assistant-Oberfläche.
FastAPI-Backend (hält HA-Token serverseitig) + statisches Frontend, ein Container.
Passt zum arndt-software.de-Stack (Coolify: New Resource -> Dockerfile, Port 8000).
"""
import hashlib
import hmac
import os

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import config as cfg
from app import ha
from app import rules

APP_PASSWORD = os.environ.get("HAUS_PASSWORD", "")
_SECRET = (APP_PASSWORD or "change-me").encode()

app = FastAPI(title="Haus-Cockpit")

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")


# ---- Auth (einfacher Passwort-Schutz; HA-Token bleibt trotzdem serverseitig) ----
def _session_token() -> str:
    return hmac.new(_SECRET, b"haus-cockpit-session", hashlib.sha256).hexdigest()


def require_auth(request: Request):
    if not APP_PASSWORD:
        # Kein Passwort gesetzt -> Schutz aus (nur für lokalen Test gedacht).
        return True
    token = request.headers.get("X-Auth", "")
    if not hmac.compare_digest(token, _session_token()):
        raise HTTPException(status_code=401, detail="Nicht angemeldet")
    return True


class LoginIn(BaseModel):
    password: str


@app.post("/api/login")
async def login(body: LoginIn):
    if not APP_PASSWORD:
        return {"token": _session_token(), "note": "Kein Passwort gesetzt"}
    if not hmac.compare_digest(body.password, APP_PASSWORD):
        raise HTTPException(status_code=401, detail="Falsches Passwort")
    return {"token": _session_token()}


# ---- Health (für Coolify/Traefik) ----
@app.get("/api/health")
async def health():
    return {"status": "ok", "ha": await ha.ping()}


# ---- Dashboard ----
@app.get("/api/dashboard")
async def dashboard(_=Depends(require_auth)):
    try:
        states = await ha.get_states()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Home Assistant nicht erreichbar: {e}")
    by_id = {s["entity_id"]: s for s in states}

    def entry(fav):
        s = by_id.get(fav["entity_id"])
        item = {
            "key": fav["key"],
            "type": fav["type"],
            "entity_id": fav["entity_id"],
            "label": fav["label"],
            "icon": fav.get("icon", ""),
            "state": s["state"] if s else "unavailable",
            "attributes": s.get("attributes", {}) if s else {},
        }
        if fav.get("problem"):
            ps = by_id.get(fav["problem"])
            item["problem"] = bool(ps and ps["state"] == "on")
            item["offline"] = bool(not s or s["state"] == "unavailable")
        return item

    favs = [entry(f) for f in cfg.FAVORITES]

    # Anwesenheit: alle Personen live
    persons = [
        {
            "entity_id": s["entity_id"],
            "name": s["attributes"].get("friendly_name", s["entity_id"]),
            "home": s["state"] == "home",
            "state": s["state"],
        }
        for s in states
        if s["entity_id"].startswith("person.")
    ]
    persons.sort(key=lambda p: p["name"].lower())

    return {"favorites": favs, "persons": persons}


@app.get("/api/rooms")
async def rooms(_=Depends(require_auth)):
    """Etagen -> Räume -> echte Geräte (aus den gemappten HA-Bereichen)."""
    try:
        devices = await ha.get_area_devices()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Home Assistant nicht erreichbar: {e}")

    def hide(name: str) -> bool:
        n = name or ""
        return any(w.lower() in n.lower() for w in cfg.HIDE_NAME_CONTAINS)

    # Geräte nach Bereichsnamen gruppieren (Junk raus)
    by_area: dict[str, list] = {}
    for d in devices:
        if hide(d.get("n", "")):
            continue
        by_area.setdefault(d["area"], []).append({
            "entity_id": d["e"],
            "domain": d["d"],
            "name": d.get("n") or d["e"],
            "state": d.get("s"),
            "current_temperature": d.get("ct"),
            "position": d.get("pos"),
        })

    floors = []
    for floor in cfg.FLOORS:
        rooms_out = []
        for room_name, areas in cfg.ROOM_MAP.get(floor, {}).items():
            devs = []
            for area in areas:
                devs.extend(by_area.get(area, []))
            # doppelte entfernen, nach Name sortieren
            seen = set()
            uniq = []
            for x in sorted(devs, key=lambda z: (z["domain"], (z["name"] or "").lower())):
                if x["entity_id"] in seen:
                    continue
                seen.add(x["entity_id"])
                uniq.append(x)
            if uniq:
                rooms_out.append({"name": room_name, "devices": uniq})
        if rooms_out:
            floors.append({"name": floor, "rooms": rooms_out})

    return {"floors": floors}


class ServiceIn(BaseModel):
    domain: str
    service: str
    entity_id: str
    data: dict | None = None


@app.post("/api/service")
async def service(body: ServiceIn, _=Depends(require_auth)):
    if body.domain not in cfg.ALLOWED_SERVICE_DOMAINS:
        raise HTTPException(status_code=403, detail=f"Domäne '{body.domain}' nicht erlaubt")
    data = {"entity_id": body.entity_id}
    if body.data:
        data.update(body.data)
    try:
        await ha.call_service(body.domain, body.service, data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"HA-Fehler: {e}")
    return {"ok": True}


@app.post("/api/quick/schlager")
async def quick_schlager(_=Depends(require_auth)):
    try:
        await ha.call_service("media_player", "play_media", {
            "entity_id": cfg.KITCHEN_PLAYER,
            "media_content_id": cfg.SCHLAGER_STREAM,
            "media_content_type": "music",
        })
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"HA-Fehler: {e}")
    return {"ok": True}


# ---- Regeln ----
@app.get("/api/automations")
async def automations(_=Depends(require_auth)):
    try:
        return {"automations": await ha.list_automation_states()}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Home Assistant nicht erreichbar: {e}")


@app.get("/api/rules/blocks")
async def rule_blocks(_=Depends(require_auth)):
    return {"triggers": cfg.RULE_TRIGGERS, "actions": cfg.RULE_ACTIONS}


class SimpleRuleIn(BaseModel):
    trigger: str
    action: str


@app.post("/api/rules/simple")
async def create_simple_rule(body: SimpleRuleIn, _=Depends(require_auth)):
    try:
        auto_id, config = rules.build_simple_rule(body.trigger, body.action)
        await ha.save_automation_config(auto_id, config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"HA-Fehler: {e}")
    return {"ok": True, "id": auto_id, "alias": config["alias"]}


class ToggleIn(BaseModel):
    entity_id: str
    enable: bool


@app.post("/api/automations/toggle")
async def toggle_automation(body: ToggleIn, _=Depends(require_auth)):
    service = "turn_on" if body.enable else "turn_off"
    try:
        await ha.call_service("automation", service, {"entity_id": body.entity_id})
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"HA-Fehler: {e}")
    return {"ok": True}


# ---- Frontend ausliefern ----
@app.get("/")
async def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.exception_handler(HTTPException)
async def http_exc(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# statische Dateien (falls später CSS/JS ausgelagert werden)
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
