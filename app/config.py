"""
Konfiguration für das Haus-Cockpit.

Hier stehen die "Favoriten" – also die Geräte, die im Dashboard erscheinen.
Andre kann diese Liste jederzeit anpassen: Einträge entfernen, umbenennen (label),
Symbol (icon) ändern oder neue hinzufügen. Die entity_id findest du in Home Assistant
unter Einstellungen -> Geräte & Dienste -> Entitäten.
"""

# Schlager-Stream, den der Knopf "Schlager an" auf die Küche schickt.
SCHLAGER_STREAM = "http://webstream.schlagerparadies.de/schlagerparadies128k.mp3"

# Die Küche (Cast/Lenovo-Display) – Ziel für den Schlager-Knopf.
KITCHEN_PLAYER = "media_player.kuche"

# Favoriten fürs Dashboard.
#   type: "light" | "cover" | "media" | "switch"
#   problem: (optional) binary_sensor, das "on/Problem" meldet -> zeigt Warnhinweis
FAVORITES = [
    {
        "key": "kueche_musik",
        "type": "media",
        "entity_id": "media_player.kuche",
        "label": "Küche – Musik",
        "icon": "🎵",
    },
    {
        "key": "garage",
        "type": "cover",
        "entity_id": "cover.smart_garage_door_1909189360642490801948e1e95200f3_garage",
        "label": "Garagentor",
        "icon": "🚗",
        "problem": "binary_sensor.smart_garage_door_1909189360642490801948e1e95200f3_problem",
    },
    {
        "key": "haustur_links",
        "type": "light",
        "entity_id": "light.haustur_links_praxis",
        "label": "Haustür links",
        "icon": "💡",
    },
    {
        "key": "haustur_rechts",
        "type": "light",
        "entity_id": "light.haustur_rechts_esszimmer",
        "label": "Haustür rechts",
        "icon": "💡",
    },
]

# Nur diese HA-Service-Domänen dürfen über die App geschaltet werden.
# Schützt davor, dass die App mehr kann als beabsichtigt.
ALLOWED_SERVICE_DOMAINS = {
    "light",
    "switch",
    "cover",
    "media_player",
    "automation",
    "scene",
}

# --- Regel-Baukasten: Bausteine in einfacher Sprache ---------------------------
# Auslöser (wer/was) -> device_tracker- oder person-Entität, die zu "home" wechselt.
# Andre kann hier weitere Personen/Geräte ergänzen.
RULE_TRIGGERS = [
    {"key": "magdalena", "label": "Magdalena kommt heim", "entity_id": "device_tracker.iphone"},
]

# Aktionen (was soll passieren).
RULE_ACTIONS = [
    {"key": "schlager_kueche", "label": "Küche spielt Schlager"},
    {"key": "licht_haustuer_an", "label": "Haustürlicht anschalten"},
    {"key": "garage_zu", "label": "Garagentor schließen"},
]
