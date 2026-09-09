from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_PROJECT_PATH = Path("/opt/lampp/htdocs/WWW/PROJECTS/Python/FastApi")

FILES: dict[str, str] = {
    "backend/requirements.txt": "fastapi[standard] \nfastapi>=0.115.0\npsutil\nuvicorn[standard]>=0.30.0\nsqlalchemy>=2.0.0\noracledb>=2.0.0\npydantic-settings>=2.0.0\nhttpx>=0.27.0\njinja2>=3.1.0\npython-multipart>=0.0.9\nrequests>=2.25.1\nPyYAML>=5.4.1\nopenpyxl\nitsdangerous\nargon2-cffi>=23.1.0\naiosmtplib>=3.0.0\n",
    "backend/main.py": 'from fastapi import FastAPI, HTTPException, Request\nfrom fastapi.middleware.cors import CORSMiddleware\nfrom pydantic import BaseModel\nimport sqlite3\nimport hashlib\nimport os\nimport binascii\nfrom pathlib import Path\nimport oracledb\nfrom contextlib import asynccontextmanager\n\nfrom templates import templates\nfrom config import get_settings\nfrom database import SessionLocal\nfrom crud import get_session_secret_key_from_db\n\n@asynccontextmanager\nasync def lifespan(app: FastAPI):\n    init_sqlite_db()\n    yield\n\n\nsettings = get_settings()\napp = FastAPI(lifespan=lifespan)\n\ndb = SessionLocal()\ntry:\n\tsession_secret_key = get_session_secret_key_from_db(db)\nfinally:\n\tdb.close()\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=["http://localhost:4200"],\n    allow_credentials=True,\n    allow_methods=["*"],\n    allow_headers=["*"],\n)\n\nBASE_DIR = Path(__file__).resolve().parent\nSQLITE_DB = BASE_DIR / "cache.db"\n\n\nclass LoginRequest(BaseModel):\n    username: str\n    password: str\n\n\ndef gget_oracle_connection():\n    dsn = oracledb.makedsn(\n        settings.oracle_host, settings.oracle_port, service_name=settings.oracle_service_name\n    )\n\n    return oracledb.connect(\n        user=settings.oracle_user, password=settings.oracle_password, dsn=dsn\n    )\n\n\ndef get_sqlite_connection():\n    conn = sqlite3.connect(SQLITE_DB)\n    conn.row_factory = sqlite3.Row\n    return conn\n\n\ndef hash_password(password: str, salt: str | None = None):\n    if salt is None:\n        salt = binascii.hexlify(os.urandom(16)).decode()\n\n    password_hash = hashlib.pbkdf2_hmac(\n        "sha256", password.encode(), salt.encode(), 100000\n    )\n\n    return binascii.hexlify(password_hash).decode(), salt\n\n\ndef verify_password(password: str, stored_hash: str, salt: str):\n    password_hash, _ = hash_password(password, salt)\n    return password_hash == stored_hash\n\n\ndef init_sqlite_db():\n    conn = get_sqlite_connection()\n    cursor = conn.cursor()\n\n    cursor.execute("""\n        CREATE TABLE IF NOT EXISTS app_login_users (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            username TEXT UNIQUE NOT NULL,\n            password_hash TEXT NOT NULL,\n            salt TEXT NOT NULL,\n            active INTEGER DEFAULT 1\n        )\n    """)\n\n    cursor.execute(f"""\n        SELECT COUNT(*) AS total\n        FROM app_login_users\n    """)\n\n    total = cursor.fetchone()["total"]\n\n    if total == 0:\n        password_hash, salt = hash_password("admin")\n\n        cursor.execute(\n            """\n            INSERT INTO app_login_users (\n                username,\n                password_hash,\n                salt,\n                active\n            )\n            VALUES (?, ?, ?, ?)\n        """,\n            ("admin", password_hash, salt, 1),\n        )\n\n    conn.commit()\n    conn.close()\n\n\n@app.post("/api/login")\ndef login(data: LoginRequest):\n    conn = get_sqlite_connection()\n    cursor = conn.cursor()\n\n    cursor.execute(\n        """\n        SELECT username, password_hash, salt, active\n        FROM app_login_users\n        WHERE username = ?\n    """,\n        (data.username,),\n    )\n\n    user = cursor.fetchone()\n    conn.close()\n\n    if user is None:\n        raise HTTPException(status_code=401, detail="Credenziali non valide")\n\n    if user["active"] != 1:\n        raise HTTPException(status_code=403, detail="Utente non attivo")\n\n    if not verify_password(data.password, user["password_hash"], user["salt"]):\n        raise HTTPException(status_code=401, detail="Credenziali non valide")\n\n    return {"success": True, "username": user["username"]}\n\n\n@app.get("/api/users")\ndef get_users(request: Request,):\n    if not settings.oracle_db_user_table.isidentifier():\n        raise HTTPException(\n            status_code=500, detail="settings.oracle_db_user_table non configurata"\n        )\n\n    conn = gget_oracle_connection()\n    cursor = conn.cursor()\n\n    cursor.execute(f"""\n        SELECT \n            USERNAME,\n            EMAIL,\n            ACTIVE,\n            CREATED_AT,\n            UPDATED_AT,\n            LASTLOGIN\n        FROM {settings.oracle_db_user_table}\n        ORDER BY USERNAME\n    """)\n\n    users = []\n\n    for row in cursor.fetchall():\n        users.append(\n            {\n                "username": row[0],\n                "email": row[1] if row[1] else None,\n                "active": row[2] if row[2] else None,\n                "created_at": row[3].isoformat() if row[3] else None,\n                "updated_at": row[4].isoformat() if row[4] else None,\n                "lastlogin": row[5].isoformat() if row[5] else None,\n            }\n        )\n\n    cursor.close()\n    conn.close()\n\n    return users\n\n',
    "backend/models.py": "from sqlalchemy import (\n\tString,\n\tInteger,\n\tDate,\n\tDateTime,\n\tNumeric,\n\tBoolean,\n\tColumn,\n\tCHAR,\n\tCLOB,\n\tText,\n\ttext,\n\tComputed,\n)\nfrom sqlalchemy.orm import Mapped, mapped_column\nfrom sqlalchemy.dialects.oracle import NUMBER\nfrom sqlalchemy.sql import func\nfrom .database import Base\n\nfrom typing import Optional  #   python version < 3.10\n",
    "backend/crud.py": 'import json\nfrom datetime import datetime, date, timezone\nfrom sqlalchemy import func, or_, select, inspect, text, update\nfrom sqlalchemy.orm import Session\nfrom sqlalchemy.dialects import oracle\nfrom sqlalchemy.sql.sqltypes import Numeric, Date\nfrom decimal import Decimal, ROUND_DOWN, InvalidOperation\nfrom fastapi import Request, status, HTTPException\nfrom fastapi.responses import RedirectResponse\nfrom pathlib import Path\nfrom typing import Any\n\nfrom config import get_settings\n\nfrom typing import Optional  #   python version < 3.10\n\nsettings = get_settings()\n\n#   LOGIN FUNCTIONS -------------------------------------------\n\ndef get_session_secret_key_from_db(db: Session) -> str:\n\tstmt = text("""\n\t\tSELECT CONFIG_VALUE\n\t\tFROM TBU_NEWPROJ_LOGIN_KEYS\n\t\tWHERE CONFIG_KEY = \'SESSION_SECRET_KEY\'\n\t""")\n\n\tvalue = db.execute(stmt).scalar_one_or_none()\n\n\tif not value:\n\t\traise RuntimeError("SESSION_SECRET_KEY non trovata in Oracle")\n\n\treturn value',
    "backend/database.py": "from sqlalchemy import create_engine\nfrom sqlalchemy.orm import declarative_base, sessionmaker\nfrom config import get_settings\n\nsettings = get_settings()\n\nengine = create_engine(\n\tsettings.oracle_dsn,\n\tpool_pre_ping=True,\n\tpool_size=settings.db_pool_size,\n\tmax_overflow=settings.db_max_overflow,\n\tpool_recycle=settings.db_pool_recycle,\n\tpool_timeout=settings.db_pool_timeout,\n\tfuture=True,\n)\n\nSessionLocal = sessionmaker(\n\tautocommit=False,\n\tautoflush=False,\n\tbind=engine,\n\tfuture=True,\n)\n\nBase = declarative_base()\n\ndef get_db():\n\tdb = SessionLocal()\n\ttry:\n\t\tyield db\n\tfinally:\n\t\tdb.close()",
    "backend/.env": "#   APP VARS ----------------------------------------------------------------------------------------------\nAPP_NAME=APP_MANAGER\nAPP_ENV=dev #   dev | prod\nDEBUG=false\nHOST=127.0.0.1\nPORT=8100\nLOGIN_ACTIVATION=false\n\n#   ORACLE DB PARAMS --------------------------------------------------------------------------------------\nORACLE_USER=campisi\nORACLE_PASSWORD=campisipwd\nORACLE_HOST=oraclelnx02             #   oraclelnx02 | 192.168.200.4\nORACLE_PORT=1521\nORACLE_SERVICE_NAME=antana\nORACLE_DB_USER_TABLE=TBU_NEWPROJ_LOGIN_USERS\n\nDB_POOL_SIZE=10\nDB_MAX_OVERFLOW=20\nDB_POOL_RECYCLE=1800\nDB_POOL_TIMEOUT=30",
    "backend/config.py": 'from functools import lru_cache\nfrom pydantic_settings import BaseSettings, SettingsConfigDict\nfrom typing import Optional\n\nclass Settings(BaseSettings):\n\t#   APP VARS ----------------------------------------------------------------------------------------------\n\tapp_name: str\n\tapp_env: str\n\tdebug: bool\n\thost: str\n\tport: int\n\tlogin_activation: bool\n\n\t#   ORACLE DB PARAMS --------------------------------------------------------------------------------------\n\toracle_user: str\n\toracle_password: str\n\toracle_host: str\n\toracle_port: int = 1521\n\toracle_service_name: str\n\toracle_db_user_table: str\n\n\tdb_pool_size: int\n\tdb_max_overflow: int\n\tdb_pool_recycle: int\n\tdb_pool_timeout: int\n\n\tmodel_config = SettingsConfigDict(\n\t\tenv_file=".env",\n\t\tenv_file_encoding="utf-8",\n\t\tcase_sensitive=False,\n\t)\n\n\t@property\n\tdef oracle_dsn(self) -> str:\n\t\treturn (\n\t\t\tf"oracle+oracledb://{self.oracle_user}:{self.oracle_password}"\n\t\t\tf"@{self.oracle_host}:{self.oracle_port}/?service_name={self.oracle_service_name}"\n\t\t)\n\n\t@property\n\tdef effective_docs_url(self) -> Optional[str]:\n\t\treturn self.docs_url if self.enable_docs else None\n\n\t@property\n\tdef effective_openapi_url(self) -> Optional[str]:\n\t\treturn self.openapi_url if self.enable_docs else None\n\n@lru_cache\ndef get_settings() -> Settings:\n\treturn Settings()',
    "backend/templates.py": 'from pathlib import Path\nfrom fastapi.templating import Jinja2Templates\n\nBASE_DIR = Path(__file__).resolve().parent\ntemplates = Jinja2Templates(directory=str(BASE_DIR / "templates"))\n',
    "frontend/src/app/app.config.ts": "import { ApplicationConfig } from '@angular/core';\nimport { provideHttpClient } from '@angular/common/http';\n\nexport const appConfig: ApplicationConfig = {\n  providers: [\n    provideHttpClient()\n  ]\n};\n\n",
    "frontend/src/app/app.ts": "import { Component, OnInit, ChangeDetectorRef } from '@angular/core';\nimport { HttpClient } from '@angular/common/http';\nimport { CommonModule } from '@angular/common';\n\ninterface User {\n  username: string;\n  email: string | null;\n  active: string | null;\n  created_at: string | null;\n  updated_at: string | null;\n  lastlogin: string | null;\n}\n\n@Component({\n  selector: 'app-root',\n  standalone: true,\n  imports: [CommonModule],\n  templateUrl: './app.html',\n  styleUrls: ['./app.css', './home.css']\n})\nexport class App implements OnInit {\n  users: User[] = [];\n\n  constructor(\n    private http: HttpClient,\n    private cdr: ChangeDetectorRef\n  ) {}\n\n  ngOnInit(): void {\n    this.loadUsers();\n  }\n\n  loadUsers(): void {\n    this.http.get<User[]>('http://127.0.0.1:8100/api/users')\n      .subscribe({\n        next: data => {\n          console.log('Users loaded:', data);\n          this.users = [...data];\n          this.cdr.detectChanges();\n        },\n        error: err => console.error('Errore caricamento utenti', err)\n      });\n  }\n}\n\n",
    "frontend/src/app/app.html": "<h1>Fastapi Angular App</h1>",
    "frontend/src/app/app.css": "",
    "frontend/src/app/home.css": "",
    "app_start.py": 'import os\nfrom pathlib import Path\nimport subprocess\nimport sys\nimport json\n\n#   INSERT THIS SCRIPT IN FASTAPI/ANGULAR PROJECT ROOT FOLDER\n\ndef clear_screen():\n    command = ["cmd", "/c", "cls"] if os.name == "nt" else ["clear"]\n    subprocess.run(command, check=False)\n\n\nBASE_DIR = Path(__file__).resolve().parent\nBACKEND_DIR = BASE_DIR / "backend"\nFRONTEND_DIR = BASE_DIR / "frontend"\nBACKEND_PYTHON = (\n    BACKEND_DIR / "venv" / "Scripts" / "python.exe"\n    if os.name == "nt"\n    else BACKEND_DIR / "venv" / "bin" / "python"\n)\nPID_FILE = BASE_DIR / "app_processes.json"\n\nif not BACKEND_PYTHON.exists():\n    raise FileNotFoundError(f"Python del venv non trovato: {BACKEND_PYTHON}")\n\nclear_screen()\nif os.name == "nt":\n\n    backend_proc = subprocess.Popen(\n        [\n            "cmd.exe",\n            "/k",\n            str(BACKEND_PYTHON),\n            "-m",\n            "uvicorn",\n            "main:app",\n            "--reload",\n            "--host",\n            "127.0.0.1",\n            "--port",\n            "8100",\n        ],\n        cwd=str(BACKEND_DIR),\n        creationflags=subprocess.CREATE_NEW_CONSOLE,\n    )\n\n    frontend_proc = subprocess.Popen(\n        [\n            "cmd.exe",\n            "/k",\n            "npx",\n            "ng",\n            "serve",\n        ],\n        cwd=str(FRONTEND_DIR),\n        creationflags=subprocess.CREATE_NEW_CONSOLE,\n    )\n\n    with open(PID_FILE, "w", encoding="utf-8") as f:\n        json.dump(\n            {\n                "backend_terminal_pid": backend_proc.pid,\n                "frontend_terminal_pid": frontend_proc.pid,\n            },\n            f,\n            indent=2,\n        )\n\n    print("Backend e frontend avviati.")\n    print(f"PID salvati in: {PID_FILE}")\n\nelse:\n\n    print(f"\\n\\n\\tLinux / macOS\\n\\n")\n\n    subprocess.Popen(\n        [\n            "bash",\n            "-c",\n            f\'cd "{BACKEND_DIR}" && \'\n            "source venv/bin/activate && "\n            "python -m uvicorn main:app --reload",\n        ]\n    )\n\n    subprocess.Popen(["bash", "-c", f\'cd "{FRONTEND_DIR}" && \' "ng serve"])\n\nprint("Backend and Frontend started.")\nprint("Open at http://localhost:4200")\nprint("Type \'python app_stop.py\' to stop the app")\nprint("Type \'python app_start.py\' to start the app")\n\n',
    "app_stop.py": 'import json\nfrom pathlib import Path\nimport subprocess\n\n#   INSERT THIS SCRIPT IN FASTAPI/ANGULAR PROJECT ROOT FOLDER\n\nBASE_DIR = Path(__file__).resolve().parent\nPID_FILE = BASE_DIR / "app_processes.json"\n\nif PID_FILE.exists():\n    with open(PID_FILE, "r", encoding="utf-8") as f:\n        data = json.load(f)\n\n    for key in ["backend_terminal_pid", "frontend_terminal_pid"]:\n        pid = data.get(key)\n\n        if pid:\n            print(f"Chiudo terminale {key}: PID {pid}")\n            subprocess.run(f"taskkill /PID {pid} /F /T", shell=True)\n\n    PID_FILE.unlink()\nelse:\n    print("File app_processes.json non trovato.")\n\n',
    "avvio.py": "import os\nimport subprocess\n\ntry:\n\tsubprocess.run(['python', 'app_start.py'])\n\nexcept KeyboardInterrupt:\n\tprint('Interrotto dall utente')",
    "stop.py": "import os\nimport subprocess\n\ntry:\n\tsubprocess.run(['python', 'app_stop.py'])\n\nexcept KeyboardInterrupt:\n\tprint('Interrotto dall utente')",
    "run.bat": "@echo off\n\nREM Avvia applicazione\npython avvio.py\n\npause",
    "stop.bat": "@echo off\n\nREM Avvia applicazione\npython stop.py\n\npause",
}


def clear_screen() -> None:
    """Pulisce il terminale senza usare os.system()."""
    command = ["cmd", "/c", "cls"] if os.name == "nt" else ["clear"]
    subprocess.run(command, check=False)


def run(command: list[str], *, cwd: Path, stdout=None) -> None:
    """Esegue un comando e interrompe lo script in caso di errore."""
    print(f"> {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True, stdout=stdout)


def ask_project_name() -> str:
    while True:
        clear_screen()
        print("========================================")
        print("        NEW PROJECT CREATION")
        print("========================================")
        print()

        project_name = input("Project name (type '0' to abort): ").strip()

        if project_name == "0":
            print("Aborting operation ...")
            raise SystemExit(0)

        if project_name and project_name not in {".", ".."}:
            return project_name

        print("Project name cannot be empty")
        input("Premi Invio per riprovare...")


def write_project_files(project_dir: Path) -> None:
    """Crea i file non appartenenti al workspace Angular."""
    for relative_name, content in FILES.items():
        if relative_name.startswith("frontend/"):
            continue

        destination = project_dir / relative_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8", newline="\n")
        print(f"Creato: {destination}")


def activate_backend(project_dir: Path) -> None:
    print(f"\n\n\tActivating Backend ....\n\n")
    backend_dir = project_dir / "backend"
    backend_dir.mkdir(parents=True, exist_ok=True)

    run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)

    venv_python = get_venv_python(backend_dir)
    run(
        [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=backend_dir,
    )

    freeze_file = backend_dir / "requirements_freeze.txt"
    with freeze_file.open("w", encoding="utf-8", newline="\n") as stream:
        run([str(venv_python), "-m", "pip", "freeze"], cwd=backend_dir, stdout=stream)


def get_venv_python(backend_dir: Path) -> Path:
    if os.name == "nt":
        return backend_dir / "venv" / "Scripts" / "python.exe"
    return backend_dir / "venv" / "bin" / "python"


def create_frontend(project_dir: Path) -> None:
    npx_name = "npx.cmd" if os.name == "nt" else "npx"
    npx_path = shutil.which(npx_name) or shutil.which("npx")

    if npx_path is None:
        raise RuntimeError(
            "npx non trovato. Installa Node.js e verifica che sia nel PATH."
        )

    frontend_dir = project_dir / "frontend"

    print(f"\n\n\tCreating and activating Frontend ....\n\n")
    run(
        [
            npx_path,
            "--yes",
            "@angular/cli",
            "new",
            "frontend",
            "--defaults",
            "--skip-git",
        ],
        cwd=project_dir,
    )

    angular_json = frontend_dir / "angular.json"
    if not angular_json.is_file():
        raise RuntimeError(
            f"Workspace Angular non creato correttamente: {angular_json}"
        )

    can_customizate = input("\n\n\tReset frontend? (y/n)\n\n").strip()
    if can_customizate == "y":
        frontend_files_customization(project_dir)


def frontend_files_customization(project_dir):
    print(f"\n\n\tFrontend files customization ....\n\n")
    backups = [
        (
            "frontend/src/app/app.html",
            "frontend/src/app/demo.html",
        ),
    ]

    for source, destination in backups:
        src = project_dir / source
        dst = project_dir / destination

        if src.exists():
            shutil.copy2(src, dst)
            print(f"Backup creato: {dst}")

    for relative_name in (
        "frontend/src/app/app.config.ts",
        "frontend/src/app/app.ts",
        "frontend/src/app/app.html",
        "frontend/src/app/app.css",
        "frontend/src/app/home.css",
    ):
        destination = project_dir / relative_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(FILES[relative_name], encoding="utf-8", newline="\n")
        print(f"Aggiornato: {destination}")


def project_folder_creation():
    project_root_text = input(f"Project root [{DEFAULT_PROJECT_PATH}]: ").strip()
    project_root = (
        Path(project_root_text).expanduser()
        if project_root_text
        else DEFAULT_PROJECT_PATH
    )

    project_name = ask_project_name()
    project_dir = project_root / project_name

    if project_dir.exists():
        raise FileExistsError(f"La cartella esiste già: {project_dir}")

    project_dir.mkdir(parents=True)
    return project_dir


def main() -> None:
    try:
        project_dir = project_folder_creation()
        write_project_files(project_dir)
        activate_backend(project_dir)
        create_frontend(project_dir)
        run([sys.executable, "app_start.py"], cwd=project_dir)
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"\nErrore durante la creazione del progetto: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"\nProgetto creato in: {project_dir}")


if __name__ == "__main__":
    main()
