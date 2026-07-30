# Haus-Cockpit

Eine **vereinfachte Oberfläche für Home Assistant** – aufgeräumtes Dashboard plus
einfacher Regel-Baukasten. Von überall erreichbar (über die Nabu-Casa-Fernadresse),
abgesichert per Passwort. Der Home-Assistant-Token liegt **serverseitig** und geht
nie an den Browser.

Gleiches Muster wie deine anderen Apps: **FastAPI + statisches Frontend, ein Docker-Container,
Coolify aus GitHub**, Ziel-Domain z. B. `haus.arndt-software.de`.

## Was die App kann
- **Zuhause (Dashboard):** großer „Schlager an/aus"-Knopf für die Küche, Garagentor
  auf/zu (mit Offline-Warnung), Haustürlichter an/aus, Anzeige „wer ist zuhause".
- **Regeln:** alle Automationen ein-/ausschalten und mit dem Baukasten neue Regeln
  in einfacher Sprache anlegen („Wenn Magdalena heimkommt → Küche spielt Schlager").

## Aufbau
```
haus-cockpit/
  main.py            FastAPI: Login, Dashboard, Service-Aufrufe, Regeln, liefert Frontend
  app/
    ha.py            Home-Assistant-Client (hält Token serverseitig)
    config.py        >>> HIER Favoriten/Geräte anpassen <<<
    rules.py         Regel-Baukasten (Auslöser + Aktion -> Automation)
  frontend/index.html  mobile-optimierte Oberfläche (ein File)
  Dockerfile         Port 8000, /api/health
  .env.example       HA_URL, HA_TOKEN, HAUS_PASSWORD
```

## Geräte anpassen
Öffne `app/config.py`. Unter `FAVORITES` stehen die Dashboard-Kacheln. Du kannst
Einträge entfernen, umbenennen (`label`), das Symbol (`icon`) ändern oder neue
`entity_id`s hinzufügen. Neue Auslöser/Aktionen für den Regel-Baukasten stehen unter
`RULE_TRIGGERS` / `RULE_ACTIONS`.

## Wichtig zur Sicherheit
`HA_TOKEN` und `HAUS_PASSWORD` gehören **nur** in die Coolify-Env, nie in Git.
Die `.env` ist per `.gitignore` ausgeschlossen.

Deploy-Schritte: siehe `COOLIFY_DEPLOY_STEPS.md`.
