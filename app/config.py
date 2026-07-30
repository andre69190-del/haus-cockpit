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

# --- Räume: Prototyp-Etagen auf echte HA-Bereiche gemappt ---------------------
# Etage -> Raum-Anzeigename -> Liste der HA-Bereichsnamen, die dazugehören.
# So werden die Räume automatisch mit den echten Geräten dieser Bereiche gefüllt.
# Andre kann hier Räume/Bereiche ergänzen oder umbenennen.
FLOORS = ["Erdgeschoss", "Obergeschoss", "Dachgeschoss", "Praxis", "Garten"]

ROOM_MAP = {
    "Erdgeschoss": {
        "Eingang": ["Haustür"],
        "Flur": ["Flur EG", "EG Flur Boden", "Flur"],
        "Garderobe": ["Garderobe"],
        "Gäste-WC": ["Gäste WC"],
        "Küche": ["Küche", "Kuechenfenster"],
        "Wohnzimmer": ["Wohnzimmer", "Wohnzimmer t"],
    },
    "Obergeschoss": {
        "Flur": ["Flur OG"],
        "Schlafzimmer": ["Schlafzimmer", "Schlafzimmer 2"],
        "Oliver": ["Oliver", "Oliver q"],
        "Leonard": ["Leo", "Leonard"],
        "Badezimmer": ["Badezimmer"],
    },
    "Dachgeschoss": {
        "Freizeitraum": ["Freizeitraum DG", "Dachgeschoss"],
    },
    "Praxis": {
        "Praxis": ["Praxis", "Praxis Flur"],
    },
    "Garten": {
        "Garten": ["Garten"],
        "Cube": ["Garten - Cube"],
        "Einfahrt": ["Garageneinfahrt"],
        "Garage": ["Garage"],
        "Hauswand": ["Hauswand"],
        "Zaun": ["Zaun"],
        "Pool": ["Pool", "Wasserwand"],
    },
}

# Geräte, deren Name diese Wörter enthält, werden ausgeblendet (Hue-„Automation"-Schalter u. Ä.).
HIDE_NAME_CONTAINS = ["Automation", "buzzerEnable", "Zirkulation"]

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
