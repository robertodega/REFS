#!/usr/bin/env python3
"""
generate_project.py
====================

Genera la struttura iniziale di un'applicazione full-stack con:
  - backend: FastAPI (Python)
  - frontend: Angular (standalone components)
  - start.py: avvia backend e frontend e apre il browser
  - stop.py:  termina i processi avviati da start.py

Uso:
    python generate_project.py [nome_progetto] [--dir cartella_destinazione]

Esempio:
    python generate_project.py mia-app
    python generate_project.py mia-app --dir /percorso/dove/creare

Dopo la generazione:
    cd mia-app/backend  && python -m venv venv && (venv attivato) pip install -r requirements.txt
    cd mia-app/frontend && npm install
    cd mia-app          && python start.py
"""

import argparse
import os, subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Placeholder sostituiti per semplice replace (evita conflitti con le
# parentesi graffe usate da JSON / TypeScript / dict Python nei template)
# --------------------------------------------------------------------------
PH_NAME = "__APP_NAME__"
PH_SLUG = "__APP_SLUG__"

# --------------------------------------------------------------------------
# Template dei file
# --------------------------------------------------------------------------

README_MD = """# __APP_NAME__

Struttura iniziale generata automaticamente: **Angular** (frontend) + **FastAPI** (backend).

## Struttura del progetto

```
__APP_NAME__/
├── backend/            FastAPI
│   ├── app/
│   │   ├── main.py       Endpoint FastAPI (inclusi quelli CRUD su SQLite)
│   │   ├── database.py   Configurazione del database SQLite (engine, sessione)
│   │   ├── models.py     Modelli SQLAlchemy (tabelle)
│   │   └── schemas.py    Schemi Pydantic (validazione/serializzazione)
│   ├── requirements.txt
│   └── .env.example
├── frontend/           Angular (standalone components)
│   ├── src/
│   └── package.json
├── start.py            Avvia backend + frontend e apre il browser
├── stop.py             Termina i processi avviati con start.py
└── README.md
```

## Setup iniziale (una tantum)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Avvio dell'applicazione

Dalla cartella principale del progetto:

```bash
python start.py
```

Lo script avvia il backend su `http://127.0.0.1:8100`, il frontend su
`http://localhost:4200` e apre automaticamente il browser.

## Arresto dell'applicazione

```bash
python stop.py
```

## Endpoint di esempio

- `GET /api/health` — controllo dello stato del backend
- `GET /api/hello`  — messaggio di esempio consumato dal frontend

## Database (SQLite)

Il backend usa **SQLite** tramite **SQLAlchemy** come ORM. Al primo avvio viene
creato automaticamente il file `backend/app.db` con le tabelle definite in
`backend/app/models.py` — non serve alcuna configurazione manuale.

- `backend/app/database.py` — connessione al database e gestione della sessione
- `backend/app/models.py` — modelli SQLAlchemy (tabelle). Include una tabella
  di esempio `items`
- `backend/app/schemas.py` — schemi Pydantic per validare le richieste e
  serializzare le risposte

### Endpoint CRUD di esempio (tabella `items`)

- `POST /api/items` — crea un elemento (`{"name": "...", "description": "..."}`)
- `GET /api/items` — elenca tutti gli elementi
- `GET /api/items/{id}` — restituisce un singolo elemento
- `DELETE /api/items/{id}` — elimina un elemento

Puoi provarli dalla documentazione interattiva su
`http://127.0.0.1:8100/docs` una volta avviato il backend.

### Aggiungere nuove tabelle

1. Definisci un nuovo modello in `backend/app/models.py` (ereditando da `Base`).
2. Aggiungi gli schemi Pydantic corrispondenti in `backend/app/schemas.py`.
3. Aggiungi gli endpoint in `backend/app/main.py`.
4. Riavvia il backend: le nuove tabelle vengono create automaticamente
   (`Base.metadata.create_all`) se non esistono già.

Per modifiche più strutturate (es. produzione, migrazioni dello schema nel
tempo) è consigliato introdurre uno strumento come **Alembic**.

### Reset del database

Per ripartire da un database vuoto, ferma l'app (`python stop.py`) ed elimina
il file `backend/app.db`: verrà ricreato automaticamente al prossimo avvio.
"""

GITIGNORE = """# Python
__pycache__/
*.pyc
venv/
.venv/
.env

# Database
*.db
*.sqlite3

# Node / Angular
node_modules/
dist/
.angular/

# Runtime
.run/
*.log
"""

# ---------------------------- BACKEND ------------------------------------

BACKEND_REQUIREMENTS = """fastapi>=0.118
uvicorn[standard]>=0.32
python-dotenv>=1.0
pydantic>=2.12
sqlalchemy>=2.0
"""

BACKEND_ENV_EXAMPLE = """PORT=8100
ENV=development
"""

BACKEND_INIT = """"""

BACKEND_DATABASE = '''"""Configurazione del database SQLite e gestione della sessione."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Il file del database viene creato nella cartella backend/, accanto a app/
DB_PATH = Path(__file__).resolve().parent.parent / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False e' necessario perche' FastAPI puo' gestire le
# richieste su thread diversi, mentre SQLite di default permette l'accesso
# solo dal thread che ha aperto la connessione.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency FastAPI: fornisce una sessione DB e la chiude sempre a fine richiesta."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

BACKEND_MODELS = '''"""Modelli SQLAlchemy: definiscono le tabelle del database."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Item(Base):
    """Tabella di esempio: un semplice elenco di elementi con nome e descrizione."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
'''

BACKEND_SCHEMAS = '''"""Schemi Pydantic: validano le richieste in ingresso e serializzano le risposte."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Dati richiesti per creare un nuovo elemento."""
    pass


class ItemRead(ItemBase):
    """Dati restituiti dalle API, inclusi i campi generati dal database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
'''

BACKEND_MAIN = '''"""Punto di ingresso dell'applicazione FastAPI."""

from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, DB_PATH, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea il file SQLite e le tabelle all'avvio, se non esistono gia'.
    # Il print aiuta a diagnosticare subito eventuali problemi: se non vedi
    # questo messaggio nel terminale, il processo backend non sta partendo
    # correttamente (es. porta occupata, dipendenza mancante, errore di
    # import) - controlla l'output sopra per il traceback.
    print(f"-> Database SQLite: {DB_PATH}")
    Base.metadata.create_all(bind=engine)
    print("-> Tabelle create/verificate.")
    yield


app = FastAPI(title="__APP_NAME__ API", version="0.1.0", lifespan=lifespan)

# Consente al frontend Angular (in sviluppo) di chiamare le API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    """Endpoint di controllo dello stato del servizio."""
    return {"status": "ok"}


@app.get("/api/hello")
def hello() -> dict:
    """Endpoint di esempio consumato dal frontend."""
    return {"message": "Ciao dal backend FastAPI!"}


# --------------------------------------------------------------------------
# Esempio di CRUD su SQLite, tabella "items"
# --------------------------------------------------------------------------

@app.post("/api/items", response_model=schemas.ItemRead, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Crea un nuovo elemento nel database."""
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/api/items", response_model=List[schemas.ItemRead])
def list_items(db: Session = Depends(get_db)):
    """Restituisce tutti gli elementi salvati, dal piu' recente."""
    return db.query(models.Item).order_by(models.Item.id.desc()).all()


@app.get("/api/items/{item_id}", response_model=schemas.ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Restituisce un singolo elemento dato il suo id."""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Elemento non trovato")
    return item


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Elimina un elemento dato il suo id."""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Elemento non trovato")
    db.delete(item)
    db.commit()
    return None
'''

# ---------------------------- FRONTEND ------------------------------------

FRONTEND_PACKAGE_JSON = """{
  "name": "__APP_SLUG__-frontend",
  "version": "0.1.0",
  "scripts": {
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.3.0",
    "@angular/common": "^17.3.0",
    "@angular/compiler": "^17.3.0",
    "@angular/core": "^17.3.0",
    "@angular/forms": "^17.3.0",
    "@angular/platform-browser": "^17.3.0",
    "@angular/platform-browser-dynamic": "^17.3.0",
    "@angular/router": "^17.3.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.4"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.3.0",
    "@angular/cli": "^17.3.0",
    "@angular/compiler-cli": "^17.3.0",
    "typescript": "~5.4.2"
  }
}
"""

FRONTEND_ANGULAR_JSON = """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "frontend": {
      "projectType": "application",
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:application",
          "options": {
            "outputPath": "dist/frontend",
            "index": "src/index.html",
            "browser": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json",
            "assets": [],
            "styles": ["src/styles.css"],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kb",
                  "maximumError": "1mb"
                }
              ],
              "outputHashing": "all"
            },
            "development": {
              "optimization": false,
              "extractLicenses": false,
              "sourceMap": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {
            "port": 4200
          },
          "configurations": {
            "production": {
              "buildTarget": "frontend:build:production"
            },
            "development": {
              "buildTarget": "frontend:build:development"
            }
          },
          "defaultConfiguration": "development"
        }
      }
    }
  }
}
"""

FRONTEND_TSCONFIG_JSON = """{
  "compileOnSave": false,
  "compilerOptions": {
    "outDir": "./dist/out-tsc",
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "sourceMap": true,
    "declaration": false,
    "experimentalDecorators": true,
    "moduleResolution": "bundler",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022", "dom"]
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}
"""

FRONTEND_TSCONFIG_APP_JSON = """{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./out-tsc/app",
    "types": []
  },
  "files": ["src/main.ts"],
  "include": ["src/**/*.d.ts"]
}
"""

FRONTEND_INDEX_HTML = """<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>__APP_NAME__</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <app-root></app-root>
</body>
</html>
"""

FRONTEND_MAIN_TS = """import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient()]
}).catch((err) => console.error(err));
"""

FRONTEND_STYLES_CSS = """* {
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f5f6f8;
  color: #1a1a1a;
}
"""

FRONTEND_APP_COMPONENT_TS = """import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface HelloResponse {
  message: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = '__APP_NAME__';
  backendMessage = '';
  backendOnline = false;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<HelloResponse>('http://127.0.0.1:8100/api/hello').subscribe({
      next: (res) => {
        this.backendMessage = res.message;
        this.backendOnline = true;
      },
      error: () => {
        this.backendMessage = 'Backend non raggiungibile.';
        this.backendOnline = false;
      }
    });
  }
}
"""

FRONTEND_APP_COMPONENT_HTML = """<div class="page">
  <header class="topbar">
    <span class="brand">{{ title }}</span>
  </header>

  <main class="content">
    <section class="card">
      <h1>Benvenuto</h1>
      <p class="subtitle">Struttura iniziale generata con Angular e FastAPI.</p>

      <div class="status" [class.online]="backendOnline" [class.offline]="!backendOnline">
        <span class="dot"></span>
        <span>{{ backendMessage || 'Verifica connessione al backend...' }}</span>
      </div>
    </section>
  </main>
</div>
"""

FRONTEND_APP_COMPONENT_CSS = """.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.brand {
  font-weight: 600;
  font-size: 15px;
  letter-spacing: 0.02em;
  color: #111827;
}

.content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}

.card {
  width: 100%;
  max-width: 420px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 32px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.card h1 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.subtitle {
  margin: 0 0 24px 0;
  font-size: 14px;
  color: #6b7280;
}

.status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  padding: 10px 12px;
  border-radius: 6px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  color: #374151;
}

.status .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #9ca3af;
  flex-shrink: 0;
}

.status.online .dot {
  background-color: #16a34a;
}

.status.offline .dot {
  background-color: #dc2626;
}
"""

# ---------------------------- START / STOP --------------------------------

START_PY = '''#!/usr/bin/env python3
"""Avvia backend (FastAPI) e frontend (Angular), attende che siano pronti e apre il browser."""

import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
PID_FILE = ROOT / ".run" / "pids.json"

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8100
FRONTEND_PORT = 4200
FRONTEND_URL = f"http://localhost:{FRONTEND_PORT}"
BACKEND_HEALTH_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/health"

IS_WINDOWS = platform.system() == "Windows"


def find_venv_python() -> str:
    """Restituisce il python del virtualenv del backend, se presente, altrimenti quello di sistema."""
    for name in ("venv", ".venv"):
        venv_dir = BACKEND_DIR / name
        if venv_dir.exists():
            candidate = venv_dir / ("Scripts" if IS_WINDOWS else "bin") / ("python.exe" if IS_WINDOWS else "python")
            if candidate.exists():
                return str(candidate)
    return sys.executable


def wait_for(url: str, timeout: float = 60) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status < 500:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def popen_kwargs() -> dict:
    """Avvia il processo nel proprio process group/sessione, cosi' stop.py
    puo' terminare anche gli eventuali processi figli (es. 'ng serve'
    lanciato da 'npm start'), non solo il processo padre."""
    if IS_WINDOWS:
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def start_backend() -> subprocess.Popen:
    print("-> Avvio backend FastAPI...")
    python_bin = find_venv_python()
    cmd = [python_bin, "-m", "uvicorn", "app.main:app", "--host", BACKEND_HOST, "--port", str(BACKEND_PORT), "--reload"]
    return subprocess.Popen(cmd, cwd=str(BACKEND_DIR), **popen_kwargs())


def start_frontend() -> subprocess.Popen:
    print("-> Avvio frontend Angular...")
    npm_cmd = "npm.cmd" if IS_WINDOWS else "npm"
    cmd = [npm_cmd, "start", "--", "--port", str(FRONTEND_PORT)]
    return subprocess.Popen(cmd, cwd=str(FRONTEND_DIR), **popen_kwargs())


def save_pids(backend_pid: int, frontend_pid: int) -> None:
    PID_FILE.parent.mkdir(exist_ok=True)
    PID_FILE.write_text(json.dumps({"backend": backend_pid, "frontend": frontend_pid}))


def main() -> None:
    if not BACKEND_DIR.exists() or not FRONTEND_DIR.exists():
        print("Errore: le cartelle backend/ e/o frontend/ non sono state trovate.")
        sys.exit(1)

    backend_proc = start_backend()
    frontend_proc = start_frontend()
    save_pids(backend_proc.pid, frontend_proc.pid)

    print("-> Attendo che il backend sia pronto...")
    if wait_for(BACKEND_HEALTH_URL):
        print(f"   Backend pronto su http://{BACKEND_HOST}:{BACKEND_PORT}")
    else:
        print("   Attenzione: il backend non ha risposto in tempo, continuo comunque.")

    print("-> Attendo che il frontend sia pronto (puo' richiedere qualche istante al primo avvio)...")
    if wait_for(FRONTEND_URL, timeout=120):
        print(f"   Frontend pronto su {FRONTEND_URL}")
    else:
        print("   Attenzione: il frontend non ha risposto in tempo, apro comunque il browser.")

    webbrowser.open(FRONTEND_URL)
    print(f"\\nApp avviata. PID backend={backend_proc.pid}, PID frontend={frontend_proc.pid}")
    print("Usa 'python stop.py' per terminare i processi.")


if __name__ == "__main__":
    main()
'''

STOP_PY = '''#!/usr/bin/env python3
"""Termina i processi di backend e frontend avviati da start.py."""

import json
import os
import platform
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PID_FILE = ROOT / ".run" / "pids.json"
IS_WINDOWS = platform.system() == "Windows"


def kill_pid(pid, label: str) -> None:
    if pid is None:
        return
    try:
        if IS_WINDOWS:
            # /T termina anche l'intero albero di processi figli (es. 'ng serve'
            # lanciato da 'npm start'), non solo il processo con questo PID.
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, capture_output=True)
        else:
            # start.py avvia il processo con start_new_session=True, quindi il
            # suo PID coincide con il process group ID: terminando l'intero
            # gruppo si eliminano anche gli eventuali processi figli (es. 'ng
            # serve' lanciato da 'npm start'), evitando che restino appesi e
            # continuino a occupare la porta.
            try:
                os.killpg(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                os.kill(pid, signal.SIGTERM)
        print(f"-> Processo {label} (PID {pid}) terminato.")
    except ProcessLookupError:
        print(f"-> Processo {label} (PID {pid}) gia' non attivo.")
    except Exception as e:
        print(f"-> Impossibile terminare {label} (PID {pid}): {e}")


def main() -> None:
    if not PID_FILE.exists():
        print("Nessun processo registrato (file PID non trovato). L'app potrebbe non essere in esecuzione.")
        sys.exit(0)

    data = json.loads(PID_FILE.read_text())
    kill_pid(data.get("backend"), "backend")
    kill_pid(data.get("frontend"), "frontend")

    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass
    print("Fatto.")


if __name__ == "__main__":
    main()
'''


# --------------------------------------------------------------------------
# Generazione
# --------------------------------------------------------------------------


def clear_screen():
    subprocess.run(["cls"] if os.name == "nt" else ["clear"])


def ask_project_name() -> str:
    while True:
        clear_screen()
        print("========================================")
        print("        NEW PROJECT CREATION")
        print("========================================\n")
        project_name = input("Project name (type '0' to abort): ").strip()

        if project_name == "0":
            print("Aborting operation ...")
            raise SystemExit(0)

        if project_name and project_name not in {".", ".."}:
            if any(char in project_name for char in '<>:"/\\|?*'):
                print("Il nome contiene caratteri non validi per Windows.")
            else:
                return project_name
        else:
            print("Project name cannot be empty")

        input("Premi Invio per riprovare...")


def render(template: str, app_name: str, app_slug: str) -> str:
    return template.replace(PH_NAME, app_name).replace(PH_SLUG, app_slug)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(cmd: list, cwd: Path) -> None:
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def setup_and_start(project_root: Path) -> None:
    """Crea il venv, installa le dipendenze di backend e frontend e avvia l'app."""
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    is_windows = sys.platform.startswith("win")

    print("\n=== Setup backend ===")
    run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
    venv_python = (
        backend_dir
        / "venv"
        / ("Scripts" if is_windows else "bin")
        / ("python.exe" if is_windows else "python")
    )
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], cwd=backend_dir)
    run(
        [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=backend_dir,
    )

    print("\n=== Setup frontend ===")
    npm_cmd = "npm.cmd" if is_windows else "npm"
    run([npm_cmd, "install"], cwd=frontend_dir)

    print("\n=== Avvio applicazione ===")
    run([sys.executable, "start.py"], cwd=project_root)


def generate(app_name: str, target_dir: Path) -> Path:
    app_slug = app_name.lower().replace(" ", "-")
    project_root = target_dir / app_slug

    if project_root.exists():
        raise SystemExit(f"Errore: la cartella '{project_root}' esiste gia'.")

    files = {
        "README.md": README_MD,
        ".gitignore": GITIGNORE,
        "start.py": START_PY,
        "stop.py": STOP_PY,
        "backend/requirements.txt": BACKEND_REQUIREMENTS,
        "backend/.env.example": BACKEND_ENV_EXAMPLE,
        "backend/app/__init__.py": BACKEND_INIT,
        "backend/app/database.py": BACKEND_DATABASE,
        "backend/app/models.py": BACKEND_MODELS,
        "backend/app/schemas.py": BACKEND_SCHEMAS,
        "backend/app/main.py": BACKEND_MAIN,
        "frontend/package.json": FRONTEND_PACKAGE_JSON,
        "frontend/angular.json": FRONTEND_ANGULAR_JSON,
        "frontend/tsconfig.json": FRONTEND_TSCONFIG_JSON,
        "frontend/tsconfig.app.json": FRONTEND_TSCONFIG_APP_JSON,
        "frontend/src/index.html": FRONTEND_INDEX_HTML,
        "frontend/src/main.ts": FRONTEND_MAIN_TS,
        "frontend/src/styles.css": FRONTEND_STYLES_CSS,
        "frontend/src/app/app.component.ts": FRONTEND_APP_COMPONENT_TS,
        "frontend/src/app/app.component.html": FRONTEND_APP_COMPONENT_HTML,
        "frontend/src/app/app.component.css": FRONTEND_APP_COMPONENT_CSS,
    }

    for rel_path, content in files.items():
        write_file(project_root / rel_path, render(content, app_name, app_slug))

    # start.py e stop.py devono essere eseguibili su sistemi Unix
    for script in ("start.py", "stop.py"):
        script_path = project_root / script
        try:
            script_path.chmod(script_path.stat().st_mode | 0o111)
        except OSError:
            pass

    return project_root


def run(cmd: list, cwd: Path) -> None:
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def setup_and_start(project_root: Path) -> None:
    """Crea il venv, installa le dipendenze di backend e frontend e avvia l'app."""
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    is_windows = sys.platform.startswith("win")

    print("\n=== Setup backend ===")
    run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
    venv_python = (
        backend_dir
        / "venv"
        / ("Scripts" if is_windows else "bin")
        / ("python.exe" if is_windows else "python")
    )
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], cwd=backend_dir)
    run(
        [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=backend_dir,
    )

    print("\n=== Setup frontend ===")
    npm_cmd = "npm.cmd" if is_windows else "npm"
    run([npm_cmd, "install"], cwd=frontend_dir)

    print("\n=== Avvio applicazione ===")
    run([sys.executable, "start.py"], cwd=project_root)


def main() -> None:
    # parser = argparse.ArgumentParser(
    #     description="Genera la struttura iniziale di un'app Angular + FastAPI."
    # )
    # parser.add_argument(
    #     "nome", nargs="?", default="my-app", help="Nome del progetto (default: my-app)"
    # )
    # parser.add_argument(
    #     "--dir",
    #     dest="target_dir",
    #     default=".",
    #     help="Cartella in cui creare il progetto (default: cartella corrente)",
    # )
    # parser.add_argument(
    #     "--no-setup",
    #     action="store_true",
    #     help="Genera solo i file, senza installare le dipendenze ne' avviare l'app automaticamente",
    # )
    # args = parser.parse_args()

    # target_dir = Path(args.target_dir).resolve()
    # target_dir.mkdir(parents=True, exist_ok=True)

    # project_root = generate(args.nome, target_dir)

    # # project_name from command line
    # parser = argparse.ArgumentParser(description="Genera la struttura iniziale di un'app Angular + FastAPI.")
    # parser.add_argument("nome", nargs="?", default="my-app", help="Nome del progetto (default: my-app)")
    # parser.add_argument("--dir", dest="target_dir", default=".", help="Cartella in cui creare il progetto (default: cartella corrente)")
    # args = parser.parse_args()

    # target_dir = Path(args.target_dir).resolve()
    # project_name = args.nome

    # project_name from script request
    target_dir = Path("/opt/lampp/htdocs/WWW/PROJECTS/Python/FastApi")
    project_name = ask_project_name()

    target_dir.mkdir(parents=True, exist_ok=True)
    project_root = generate(project_name, target_dir)

    # Esecuzione automatica installazione
    try:
        setup_and_start(project_root)
    except subprocess.CalledProcessError as e:
        print(f"\nErrore durante il setup automatico (comando: {' '.join(e.cmd)}).")
        print("Puoi completare i passi manualmente:")
        print(
            f"  cd {project_root.name}/backend && python -m venv venv && {activate_hint} && pip install -r requirements.txt"
        )
        print(f"  cd {project_root.name}/frontend && npm install")
        print(f"  cd {project_root.name} && python start.py")
        sys.exit(1)
    except FileNotFoundError as e:
        print(
            f"\nComando non trovato: {e}. Verifica che Python, pip e npm siano installati e nel PATH."
        )
        sys.exit(1)

    # Descrizione passaggi installazione
    activate_hint = (
        "venv\\Scripts\\activate"
        if sys.platform.startswith("win")
        else "source venv/bin/activate"
    )
    print(f"Progetto creato in: {project_root}\n")
    print("Operazioni eseguite:")
    print(
        f"  cd {project_root.name}/backend && python3 -m venv venv && {activate_hint} && pip3 install -r requirements.txt"
    )
    print(f"  cd {project_root.name}/frontend && npm install")
    print(f"  cd {project_root.name} && python start.py")


if __name__ == "__main__":
    main()
