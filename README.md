# devops-portfolio

Kleine Python-API (FastAPI + PostgreSQL) als roter Faden für den DevOps-Lernplan:
Docker → Terraform → Kubernetes → CI/CD.

## Endpunkte

| Methode | Pfad | Zweck |
|---|---|---|
| GET | `/` | Version und Hostname der Instanz |
| GET | `/health` | Liveness (prüft die DB bewusst nicht) |
| GET | `/ready` | Readiness (prüft die DB) |
| GET | `/items` | Einträge auflisten |
| POST | `/items` | Eintrag anlegen, Body: `{"name": "test"}` |

## Konfiguration

Nur über Umgebungsvariablen, siehe `.env.example`. Es gibt bewusst keine Werte im Code,
die für eine Umgebung spezifisch sind.

## Lokal starten (ohne Container)

1. Postgres starten (Passwort und Namen an `.env` anpassen):

   ```powershell
   docker run -d --name db -p 5432:5432 `
     -e POSTGRES_USER=appuser -e POSTGRES_PASSWORD=bitte-aendern -e POSTGRES_DB=appdb `
     -v pgdata:/var/lib/postgresql/data postgres:16
   ```

2. Python-Umgebung einrichten (Windows PowerShell):

   ```powershell
   cd app
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Umgebungsvariablen setzen und starten:

   ```powershell
   $env:DB_PASSWORD = "bitte-aendern"
   python main.py
   ```

4. Testen:

   ```powershell
   curl http://127.0.0.1:8000/health
   curl http://127.0.0.1:8000/ready
   curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" -d '{\"name\":\"test\"}'
   curl http://127.0.0.1:8000/items
   ```

   Die automatische API-Doku findest du unter http://127.0.0.1:8000/docs.

Hinweis: In PowerShell ist `curl` ein Alias für `Invoke-WebRequest`. Wenn das Quoting stört,
nutze die interaktive Doku unter `/docs`.

## Aufgaben für Woche 2 und 3 (Docker)

- [ ] `Dockerfile` schreiben (erst einfach, dann Multi-Stage), Non-Root-User, `.dockerignore`
- [ ] `HEALTHCHECK` ergänzen
- [ ] Beachten: Im Container muss `APP_HOST=0.0.0.0` gesetzt sein, sonst ist die App von außen nicht erreichbar
- [ ] `docker-compose.yml`: App + Postgres, eigenes Netzwerk, Volume, Env-Variablen
- [ ] Image in eine Registry pushen (GHCR oder Artifact Registry)

## Spätere Phasen

- `terraform/`: Bereitstellung in Google Cloud
- `k8s/`: Manifeste für CKAD-Übungen (Deployment, Service, ConfigMap, Secret, Probes)
- `.github/workflows/`: CI/CD mit GitHub Actions
