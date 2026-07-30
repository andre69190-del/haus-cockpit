"""
Regel-Baukasten: übersetzt einfache Auswahl (Auslöser + Aktion) in eine
gültige Home-Assistant-Automation.
"""
import time
from . import config as cfg


def _trigger(trigger_key: str):
    t = next((x for x in cfg.RULE_TRIGGERS if x["key"] == trigger_key), None)
    if not t:
        raise ValueError(f"Unbekannter Auslöser: {trigger_key}")
    return {
        "trigger": "state",
        "entity_id": t["entity_id"],
        "from": "not_home",
        "to": "home",
    }, t["label"]


def _action(action_key: str):
    if action_key == "schlager_kueche":
        return [{
            "action": "media_player.play_media",
            "target": {"entity_id": cfg.KITCHEN_PLAYER},
            "data": {"media_content_id": cfg.SCHLAGER_STREAM, "media_content_type": "music"},
        }], "Küche spielt Schlager"
    if action_key == "licht_haustuer_an":
        return [{
            "action": "light.turn_on",
            "target": {"entity_id": ["light.haustur_links_praxis", "light.haustur_rechts_esszimmer"]},
        }], "Haustürlicht an"
    if action_key == "garage_zu":
        return [{
            "action": "cover.close_cover",
            "target": {"entity_id": "cover.smart_garage_door_1909189360642490801948e1e95200f3_garage"},
        }], "Garagentor schließen"
    raise ValueError(f"Unbekannte Aktion: {action_key}")


def build_simple_rule(trigger_key: str, action_key: str):
    """Baut eine Automation aus Auslöser + Aktion. Gibt (auto_id, config) zurück."""
    trig, trig_label = _trigger(trigger_key)
    acts, act_label = _action(action_key)
    auto_id = str(int(time.time() * 1000))
    alias = f"{trig_label} → {act_label}"
    config = {
        "id": auto_id,
        "alias": alias,
        "description": "Erstellt über das Haus-Cockpit",
        "triggers": [trig],
        "conditions": [],
        "actions": acts,
        "mode": "single",
    }
    return auto_id, config
