# Haus-Cockpit live schalten – Coolify

Ziel: **https://haus.arndt-software.de** (Name frei wählbar). Coolify läuft ja schon.

## Schritt 0 – Home-Assistant-Token erstellen (nur du)
1. In Home Assistant unten links auf deinen **Namen/Profil** klicken.
2. Reiter **Sicherheit** → ganz unten **„Langlebige Zugriffs-Tokens"** → **Token erstellen**.
3. Namen vergeben (z. B. „Haus-Cockpit"), Token **kopieren** (wird nur einmal gezeigt).
   Diesen Wert brauchst du gleich für `HA_TOKEN` in Coolify. **Nicht** in Git/Chat einfügen.

Die Fern-Adresse (`HA_URL`) findest du in HA unter **Einstellungen → Home Assistant Cloud**
(die `…ui.nabu.casa`-Adresse).

## Schritt 1 – Code nach GitHub (einmalig, du)
Im Ordner `HomeAssistant/haus-cockpit`:
```bash
cd Desktop/Cowork/HomeAssistant/haus-cockpit
git init && git add . && git commit -m "Haus-Cockpit MVP"
# Repo bei GitHub anlegen (andre69190-del), dann:
git remote add origin https://github.com/andre69190-del/haus-cockpit.git
git push -u origin main
```
(Die beiliegende `push-to-github.bat` macht das per Doppelklick.)

## Schritt 2 – Ressource in Coolify
1. Coolify öffnen (`coolify.arndt-software.de`) → Projekt → **+ New Resource**.
2. **Private/Public Repository** → `andre69190-del/haus-cockpit` → Branch `main`.
3. **Build Pack: Dockerfile** (liegt im Repo-Root, wird autoerkannt).
4. **Port**: `8000`.

## Schritt 3 – Domain
- **Domains** → `haus.arndt-software.de` eintragen.
- Voraussetzung ist der Wildcard-Eintrag `*.arndt-software.de` (wie bei trio) →
  Traefik holt automatisch das TLS-Zertifikat.

## Schritt 4 – ENV (Pflicht)
Unter **Environment Variables** eintragen:

| Key | Wert |
|---|---|
| `HA_URL` | `https://<deine-id>.ui.nabu.casa` |
| `HA_TOKEN` | der Token aus Schritt 0 |
| `HAUS_PASSWORD` | ein Passwort für die App |

## Schritt 5 – Deploy & Prüfen
- **Deploy** klicken. Coolify baut das Image und startet den Container.
- Healthcheck `/api/health` muss grün werden (zeigt auch `"ha": true`, wenn Token/URL stimmen).
- `https://haus.arndt-software.de` öffnen → Passwort eingeben → Dashboard testen.

---

**Was ich für dich übernehmen kann:** Gib mir die **Coolify-URL** und sei dort im Browser
eingeloggt – dann klicke ich die Schritte 2–5 per Browser-Steuerung. Schritt 0 (Token) und
Schritt 1 (GitHub-Push) musst du anstoßen; den Token gebe ich bewusst nicht selbst ein.
