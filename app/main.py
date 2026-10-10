"""Kleine Beispiel-API für den DevOps-Lernplan.

Endpunkte:
  GET  /          Infos zur Instanz (Version, Hostname)
  GET  /health    Liveness: läuft der Prozess?
  GET  /ready     Readiness: ist die Datenbank erreichbar?
  GET  /items     Alle Einträge auflisten
  POST /items     Neuen Eintrag anlegen  {"name": "..."}

Konfiguration ausschließlich über Umgebungsvariablen (siehe .env.example).
"""
import logging
import os
import socket
import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("app")

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
app = FastAPI(title="devops-portfolio-app", version=APP_VERSION)

_schema_ready = False


def db_config() -> dict:
    """Liest die DB-Konfiguration bei jedem Aufruf aus der Umgebung."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "appdb"),
        "user": os.getenv("DB_USER", "appuser"),
        "password": os.getenv("DB_PASSWORD", ""),
        "connect_timeout": 3,
    }


def get_conn() -> psycopg.Connection:
    return psycopg.connect(**db_config(), row_factory=dict_row)


def ensure_schema(conn: psycopg.Connection) -> None:
    """Legt die Tabelle beim ersten erfolgreichen DB-Zugriff an."""
    global _schema_ready
    if _schema_ready:
        return
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    conn.commit()
    _schema_ready = True
    log.info("Datenbankschema bereit")


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


@app.get("/")
def root() -> dict:
    return {
        "app": "devops-portfolio-app",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
    }


@app.get("/health")
def health() -> dict:
    # Liveness: prüft bewusst NICHT die Datenbank.
    # FORCE_UNHEALTHY=true simuliert einen Fehler (nützlich für Probe-Übungen).
    if os.getenv("FORCE_UNHEALTHY", "false").lower() == "true":
        raise HTTPException(status_code=503, detail="unhealthy (forced)")
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict:
    # Readiness: App ist nur bereit, wenn die Datenbank antwortet.
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
    except psycopg.Error as exc:
        log.warning("Readiness fehlgeschlagen: %s", exc)
        raise HTTPException(status_code=503, detail="database not reachable")
    return {"status": "ready"}


@app.get("/items")
def list_items() -> list[dict]:
    try:
        with get_conn() as conn:
            ensure_schema(conn)
            return conn.execute(
                "SELECT id, name, created_at FROM items ORDER BY id"
            ).fetchall()
    except psycopg.Error as exc:
        log.error("DB-Fehler bei GET /items: %s", exc)
        raise HTTPException(status_code=503, detail="database error")


@app.post("/items", status_code=201)
def create_item(item: ItemIn) -> dict:
    try:
        with get_conn() as conn:
            ensure_schema(conn)
            row = conn.execute(
                "INSERT INTO items (name) VALUES (%s) RETURNING id, name, created_at",
                (item.name,),
            ).fetchone()
            conn.commit()
            return row
    except psycopg.Error as exc:
        log.error("DB-Fehler bei POST /items: %s", exc)
        raise HTTPException(status_code=503, detail="database error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8000")),
    )
