from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_PROJECT_PATH = Path("C:/xampp/htdocs/PROJECTS/APPS/TESTS")

FILES: dict[str, str] = {
    "HOWTO/HOW_TO.md": "# Project creation\n"
    "\n"
    "- nano requirements.txt\n"
    "\n"
    "        fastapi[standard]\n"
    "        fastapi>=0.115.0\n"
    "        uvicorn[standard]>=0.30.0\n"
    "        sqlalchemy>=2.0.0\n"
    "        oracledb>=2.0.0\n"
    "        pydantic-settings>=2.0.0\n"
    "        httpx>=0.27.0\n"
    "        jinja2>=3.1.0\n"
    "        python-multipart>=0.0.9\n"
    "        requests>=2.25.1\n"
    "        PyYAML>=5.4.1\n"
    "        openpyxl\n"
    "\n"
    "# Project Activation\n"
    "\n"
    "    python -m venv venv\n"
    "    source venv/Scripts/activate        # Windows installation\n"
    "    source venv/bin/activate            # Linux installation\n"
    "    pip install -r requirements.txt\n"
    "\n"
    "# Project Customization\n"
    "\n"
    "# Project Run\n"
    "\n"
    "    from folder /c/xampp/htdocs/PROJECTS/DUMA/$PROJECT_NAME\n"
    "\n"
    "    - from terminal:\n"
    "            source venv/Scripts/activate    ( running on Windows )\n"
    "            source venv/bin/activate        ( running on Linux )\n"
    "            python run.py\n"
    "\n"
    "    - from executable:\n"
    "            CLICK on 'run.bat' file\n"
    "\n"
    "# Project view\n"
    "\n"
    "    http://127.0.0.1:8000/\n"
    "    http://127.0.0.1:8000/docs\n"
    "\n",
    "app/.env": "#   APP VARS "
    "----------------------------------------------------------------------------------------------\n"
    "APP_NAME=$PROJECT_NAME\n"
    "APP_ENV=dev                         #   dev | prod\n"
    "DEBUG=false\n"
    "HOST=127.0.0.1\n"
    "PORT=8000\n"
    "#   APP VARS "
    "----------------------------------------------------------------------------------------------\n"
    "\n"
    "#   EMAIL MANAGEMENT "
    "--------------------------------------------------------------------------------------\n"
    'SMTP_HOST = ""\n'
    "SMTP_PORT = 587\n"
    'SMTP_USER = ""\n'
    'SMTP_PASSWORD = ""\n'
    "#   EMAIL MANAGEMENT "
    "--------------------------------------------------------------------------------------\n"
    "\n"
    "#   LOGIN "
    "-------------------------------------------------------------------------------------------------\n"
    "LOGIN_ACTIVATION=true\n"
    'ALLOWED_MSG="Current user is allowed to use this section"\n'
    'NOT_ALLOWED_MSG="Current user is not allowed to use this section"\n'
    'ADMIN_LEVEL=["1"]\n'
    'USER_LEVEL=["1", "2"]\n'
    'GUEST_LEVEL=["1", "2", "3"]\n'
    "#   LOGIN "
    "-------------------------------------------------------------------------------------------------\n"
    "\n"
    "#   VARIABLES "
    "---------------------------------------------------------------------------------------------\n"
    "LOG_LEVEL=INFO\n"
    "\n"
    "ENABLE_DOCS=true                    #   true | false\n"
    "DOCS_URL=/docs\n"
    "OPENAPI_URL=/openapi.json\n"
    "\n"
    "# ORACLE DB PARAMS\n"
    "ORACLE_USER=campisi\n"
    "ORACLE_PASSWORD=campisipwd\n"
    "ORACLE_HOST=oraclelnx02             #   oraclelnx02 | 192.168.200.4\n"
    "ORACLE_PORT=1521\n"
    "ORACLE_SERVICE_NAME=antana\n"
    "\n"
    "DB_POOL_SIZE=10\n"
    "DB_MAX_OVERFLOW=20\n"
    "DB_POOL_RECYCLE=1800\n"
    "DB_POOL_TIMEOUT=30\n"
    "#   VARIABLES "
    "---------------------------------------------------------------------------------------------\n"
    "\n"
    "\n",
    "app/.gitignore": "# Python\n"
    "__pycache__/\n"
    "app/__pycache__/\n"
    "app/routers/__pycache__/\n"
    "*.py[cod]\n"
    "*$py.class\n"
    ".ipynb_checkpoints\n"
    "\n"
    "# Ambiente virtuale\n"
    ".venv/\n"
    "venv/\n"
    "ENV/\n"
    "env/\n"
    "\n"
    "# FastAPI / Uvicorn / Database\n"
    ".env\n"
    "db.sqlite3\n"
    "*.db\n"
    "\n"
    "# IDE\n"
    ".vscode/\n"
    ".idea/\n"
    "\n"
    "# Test e Copertura\n"
    "htmlcov/\n"
    ".tox/\n"
    ".coverage\n"
    ".pytest_cache/\n"
    "\n"
    "# Package\n"
    "build/\n"
    "develop-eggs/\n"
    "dist/\n"
    "downloads/\n"
    "eggs/\n"
    ".eggs/\n"
    "lib/\n"
    "lib64/\n"
    "parts/\n"
    "sdist/\n"
    "var/\n"
    "wheels/\n"
    "*.egg-info/\n"
    ".installed.cfg\n"
    "*.egg\n"
    "*.yml\n"
    "\n",
    "app/README.md": "",
    "app/app/__init__.py": "",
    "app/app/config.py": "from functools import lru_cache\n"
    "from pydantic_settings import BaseSettings, SettingsConfigDict\n"
    "\n"
    "\n"
    "class Settings(BaseSettings):\n"
    "    #   APP VARS "
    "----------------------------------------------------------------------------------------------\n"
    "    app_name: str\n"
    "    app_env: str\n"
    "    debug: bool\n"
    "    host: str\n"
    "    port: int\n"
    "    #   APP VARS "
    "----------------------------------------------------------------------------------------------\n"
    "\n"
    "    #   EMAIL MANAGEMENT -------------------------------------------\n"
    "    smtp_host: str\n"
    "    smtp_port: int\n"
    "    smtp_user: str\n"
    "    smtp_password: str\n"
    "    #   EMAIL MANAGEMENT -------------------------------------------\n"
    "\n"
    "    #   LOGIN -----------------------------------------------------\n"
    "    login_activation: bool\n"
    "    allowed_msg: str\n"
    "    not_allowed_msg: str\n"
    "    admin_level: list\n"
    "    user_level: list\n"
    "    guest_level: list\n"
    "    #   LOGIN -----------------------------------------------------\n"
    "\n"
    "    #   VARIABLES "
    "---------------------------------------------------------------------------------------------\n"
    '    log_level: str = "INFO"\n'
    "\n"
    "    enable_docs: bool = False  #   True | False\n"
    '    docs_url: str = "/docs"\n'
    '    openapi_url: str = "/openapi.json"\n'
    "\n"
    "    # ORACLE DB PARAMS\n"
    "    oracle_user: str\n"
    "    oracle_password: str\n"
    "    oracle_host: str\n"
    "    oracle_port: int = 1521\n"
    "    oracle_service_name: str\n"
    "\n"
    "    db_pool_size: int = 10\n"
    "    db_max_overflow: int = 20\n"
    "    db_pool_recycle: int = 1800\n"
    "    db_pool_timeout: int = 30\n"
    "    #   VARIABLES "
    "---------------------------------------------------------------------------------------------\n"
    "\n"
    "    model_config = SettingsConfigDict(\n"
    '        env_file=".env",\n'
    '        env_file_encoding="utf-8",\n'
    "        case_sensitive=False,\n"
    "    )\n"
    "\n"
    "    @property\n"
    "    def oracle_dsn(self) -> str:\n"
    "        return (\n"
    '            f"oracle+oracledb://{self.oracle_user}:{self.oracle_password}"\n'
    "            "
    'f"@{self.oracle_host}:{self.oracle_port}/?service_name={self.oracle_service_name}"\n'
    "        )\n"
    "\n"
    "    @property\n"
    "    def effective_docs_url(self) -> str | None:\n"
    "        return self.docs_url if self.enable_docs else None\n"
    "\n"
    "    @property\n"
    "    def effective_openapi_url(self) -> str | None:\n"
    "        return self.openapi_url if self.enable_docs else None\n"
    "\n"
    "\n"
    "@lru_cache\n"
    "def get_settings() -> Settings:\n"
    "    return Settings()\n"
    "\n",
    "app/app/crud.py": "import json\n"
    "from datetime import datetime, timezone\n"
    "from sqlalchemy import func, or_, select, text, update\n"
    "from sqlalchemy.orm import Session\n"
    "from sqlalchemy.dialects import oracle\n"
    "# from .models import (\n"
    "#     TableEntry,\n"
    "# )\n"
    "from fastapi import Request, status, HTTPException, BackgroundTasks\n"
    "from fastapi.responses import RedirectResponse\n"
    "from .config import get_settings\n"
    "\n"
    "from pathlib import Path\n"
    "import yaml\n"
    "\n"
    "import subprocess, sys\n"
    "\n"
    "from argon2 import PasswordHasher\n"
    "from argon2.exceptions import VerifyMismatchError\n"
    "\n"
    "from io import BytesIO\n"
    "from openpyxl import load_workbook\n"
    "from .import_manager import ImportErrorDetail, ImportResult\n"
    "\n"
    "from pydantic import BaseModel, EmailStr\n"
    "from email.message import EmailMessage\n"
    "import aiosmtplib\n"
    "\n"
    "settings = get_settings()\n"
    "\n"
    "def utcnow():\n"
    "    return datetime.now(timezone.utc).replace(tzinfo=None)\n"
    "\n"
    "\n"
    "#   LOGIN -----------------------------------------------------\n"
    "\n"
    "\n"
    "def get_session_secret_key_from_db(db: Session) -> str:\n"
    "    # Valore temporaneo per lo sviluppo; sostituire con lettura da Oracle.\n"
    '    return "development-secret-key-change-me"\n'
    "    \n"
    '    stmt = text("""\n'
    "        SELECT CONFIG_VALUE\n"
    "        FROM TBU_NEWPROJ_LOGIN_KEYS\n"
    "        WHERE CONFIG_KEY = 'SESSION_SECRET_KEY'\n"
    '    """)\n'
    "\n"
    "    value = db.execute(stmt).scalar_one_or_none()\n"
    "\n"
    "    if not value:\n"
    '        raise RuntimeError("SESSION_SECRET_KEY non trovata in Oracle")\n'
    "\n"
    "    return value\n"
    "\n"
    "\n"
    "def login_session_storage_from_db(\n"
    "    db: Session,\n"
    "    request: Request,\n"
    "    username: str,\n"
    "    password: str,\n"
    ") -> bool:\n"
    "\n"
    "    return True\n"
    "\n"
    '    stmt = text("""\n'
    "        SELECT \n"
    "            usr.ID as user_id\n"
    "                , usr.USERNAME as username\n"
    "                , usr.EMAIL as email\n"
    "                , usr.PASSWORD_HASH as password_hash\n"
    "                , usr.PROFILE_ID as profile_id\n"
    "                , usr.ACTIVE as active\n"
    "                , prof.NAME as profile_name\n"
    "            FROM \n"
    "                TBU_NEWPROJ_LOGIN_USERS usr\n"
    "                left join TBU_NEWPROJ_LOGIN_PROFILES prof on prof.id = usr.profile_id\n"
    "            WHERE USERNAME = :username\n"
    '    """)\n'
    "\n"
    '    result = db.execute(stmt, {"username": username}).mappings().first()\n'
    "\n"
    "    if result is None:\n"
    "        err_msg = f\"Wrong user '{username}'\"\n"
    '        print(f"\\n\\n\\t{err_msg}\\n\\n")\n'
    '        request.session["login_errors"] = err_msg\n'
    "        return False\n"
    "\n"
    '    if result["active"] == 0:\n'
    "        err_msg = f\"Access for user '{username}' is not allowed\"\n"
    '        print(f"\\n\\n\\t{err_msg}\\n\\n")\n'
    '        request.session["login_errors"] = err_msg\n'
    "        return False\n"
    "\n"
    "    ph = PasswordHasher()\n"
    "    try:\n"
    '        if ph.verify(result["password_hash"], password):\n'
    "            pass\n"
    "    except VerifyMismatchError:\n"
    "        err_msg = f\"Wrong Inserted Password for user '{username}'\"\n"
    '        print(f"\\n\\n\\t{err_msg}\\n\\n")\n'
    '        request.session["login_errors"] = err_msg\n'
    "        return False\n"
    "\n"
    '    request.session["app_env"] = settings.app_env\n'
    '    request.session["user_id"] = result["user_id"]\n'
    '    request.session["username"] = result["username"]\n'
    '    request.session["password_hash"] = result["password_hash"]\n'
    '    request.session["profile_id"] = result["profile_id"]\n'
    '    request.session["profile_name"] = result["profile_name"]\n'
    "\n"
    "    return True\n"
    "\n"
    "\n"
    "def check_login(request: Request, credential_type: list[str]):\n"
    "    if settings.login_activation:\n"
    '        if not request.session.get("username"):\n'
    "            return False\n"
    "        else:\n"
    '            if request.session.get("profile_id") not in credential_type:\n'
    '                print(f"\\t{settings.not_allowed_msg}\\n")\n'
    "                return False\n"
    "            else:\n"
    "                return True\n"
    "    else:\n"
    "        return True\n"
    "\n"
    "\n"
    "#   LOGIN -----------------------------------------------------\n"
    "\n",
    "app/app/database.py": "from sqlalchemy import create_engine\n"
    "from sqlalchemy.orm import declarative_base, sessionmaker\n"
    "from .config import get_settings\n"
    "\n"
    "settings = get_settings()\n"
    "\n"
    "engine = create_engine(\n"
    "    settings.oracle_dsn,\n"
    "    pool_pre_ping=True,\n"
    "    pool_size=settings.db_pool_size,\n"
    "    max_overflow=settings.db_max_overflow,\n"
    "    pool_recycle=settings.db_pool_recycle,\n"
    "    pool_timeout=settings.db_pool_timeout,\n"
    "    future=True,\n"
    ")\n"
    "\n"
    "SessionLocal = sessionmaker(\n"
    "    autocommit=False,\n"
    "    autoflush=False,\n"
    "    bind=engine,\n"
    "    future=True,\n"
    ")\n"
    "\n"
    "Base = declarative_base()\n"
    "\n"
    "\n"
    "def get_db():\n"
    "    db = SessionLocal()\n"
    "    try:\n"
    "        yield db\n"
    "    finally:\n"
    "        db.close()\n"
    "\n",
    "app/app/import_manager.py": "from pydantic import BaseModel\n"
    "\n"
    "\n"
    "class ImportErrorDetail(BaseModel):\n"
    "    row: int\n"
    "    message: str\n"
    "\n"
    "\n"
    "class ImportResult(BaseModel):\n"
    "    imported: int\n"
    "    skipped: int\n"
    "    errors: list[ImportErrorDetail]\n"
    "\n"
    "\n",
    "app/app/main.py": "from pathlib import Path\n"
    "\n"
    "from fastapi import FastAPI\n"
    "from fastapi.staticfiles import StaticFiles\n"
    "\n"
    "# ----- LOGIN -----\n"
    "\n"
    "import os\n"
    "from starlette.middleware.sessions import SessionMiddleware\n"
    "from sqlalchemy import text\n"
    "from .database import SessionLocal\n"
    "from .crud import get_session_secret_key_from_db\n"
    "\n"
    "# ----- LOGIN -----\n"
    "\n"
    "from .config import get_settings\n"
    "from .routers import home, login\n"
    "\n"
    "settings = get_settings()\n"
    "\n"
    "app = FastAPI(\n"
    "    title=settings.app_name,\n"
    "    debug=settings.debug,\n"
    "    docs_url=settings.effective_docs_url,\n"
    "    openapi_url=settings.effective_openapi_url,\n"
    "    redoc_url=None,\n"
    ")\n"
    "\n"
    "# ----- LOGIN -----\n"
    "\n"
    "# User | Password | Profile Authentication system\n"
    "# --------------------------\n"
    "# SESSION_SECRET_KEY from DB\n"
    "# --------------------------\n"
    "db = SessionLocal()\n"
    "try:\n"
    "    session_secret_key = get_session_secret_key_from_db(db)\n"
    "finally:\n"
    "    db.close()\n"
    "\n"
    "app.add_middleware(\n"
    "    SessionMiddleware,\n"
    "    secret_key=session_secret_key,\n"
    '    session_cookie="projects_name_session",\n'
    ")\n"
    "\n"
    "# ----- LOGIN -----\n"
    "\n"
    "base_dir = Path(__file__).resolve().parent\n"
    'app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")\n'
    "\n"
    "app.include_router(home.router)\n"
    "app.include_router(login.router)\n"
    "\n"
    "\n",
    "app/app/models.py": "from sqlalchemy import String, Integer, DateTime, Boolean, Column, Numeric, CLOB, "
    "Text\n"
    "from sqlalchemy.orm import Mapped, mapped_column\n"
    "from sqlalchemy.dialects.oracle import NUMBER\n"
    "from sqlalchemy.sql import func\n"
    "from .database import Base\n"
    "\n"
    "class UsersEntry(Base):\n"
    '    __tablename__ = "TBU_NEWPROJ_LOGIN_USERS"\n'
    "\n"
    '    id = Column("ID", NUMBER(38, 0), primary_key=True)\n'
    '    username = Column("USERNAME", String(100), nullable=False, unique=True)\n'
    '    email = Column("EMAIL", String(100), nullable=False, unique=True)\n'
    '    password_hash = Column("PASSWORD_HASH", String(255), nullable=False)\n'
    '    profile_id = Column("PROFILE_ID", String(2), nullable=True)\n'
    '    active: Mapped[bool] = mapped_column("ACTIVE", Boolean)\n'
    "    created_at = Column(\n"
    '        "CREATED_AT",\n'
    "        DateTime,\n"
    "        nullable=True,\n"
    "        server_default=func.now(),\n"
    "    )\n"
    "    updated_at = Column(\n"
    '        "UPDATED_AT",\n'
    "        DateTime,\n"
    "        nullable=True,\n"
    "        server_default=func.now(),\n"
    "    )\n"
    "\n",
    "app/app/routers/__init__.py": "",
    "app/app/routers/home.py": "import logging\n"
    "\n"
    "from fastapi import (\n"
    "    APIRouter,\n"
    "    Request,\n"
    "    status,\n"
    "    Form,\n"
    "    Depends,\n"
    "    HTTPException,\n"
    ")\n"
    "from fastapi.responses import HTMLResponse, RedirectResponse\n"
    "from sqlalchemy.orm import Session\n"
    "\n"
    "from ..config import get_settings\n"
    "from ..database import get_db\n"
    "from ..templates import templates\n"
    "# from ..models import TableEntry\n"
    "from ..crud import (\n"
    "    check_login,\n"
    "    utcnow,\n"
    ")\n"
    "\n"
    "from argon2 import PasswordHasher\n"
    "from argon2.exceptions import VerifyMismatchError, HashingError\n"
    "\n"
    "router = APIRouter()\n"
    "settings = get_settings()\n"
    "\n"
    "\n"
    '@router.get("/", response_class=HTMLResponse)\n'
    "def get_home_page(\n"
    "    request: Request,\n"
    "    db: Session = Depends(get_db),\n"
    "):\n"
    "    \n"
    "    return templates.TemplateResponse(\n"
    '        name="home.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_activation": settings.login_activation,\n'
    "        },\n"
    "    )\n"
    "\n"
    "    # ----- LOGIN -----\n"
    "\n"
    '    login_msg_err = ""\n'
    "    # allowed_level = settings.admin_level\n"
    "    # allowed_level = settings.user_level\n"
    "    allowed_level = settings.guest_level\n"
    "    allowed_msg = check_login(request, allowed_level)\n"
    "    if not allowed_msg:\n"
    "        login_msg_err = settings.not_allowed_msg\n"
    '        return RedirectResponse(url="/login", '
    "status_code=status.HTTP_303_SEE_OTHER)\n"
    "\n"
    "    # ----- LOGIN -----\n"
    "\n"
    "    pending_profiles = db.query(UsersEntry).filter(UsersEntry.active == "
    "0).all()\n"
    "\n"
    "    return templates.TemplateResponse(\n"
    '        name="home.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_msg_err": login_msg_err,\n'
    '            "allowed_msg": allowed_msg,\n'
    '            "pending_profiles_length": len(pending_profiles),\n'
    '            "allowed_value": False if allowed_msg == settings.not_allowed_msg '
    "else True,\n"
    "        },\n"
    "    )\n"
    "\n",
    "app/app/routers/login.py": "from fastapi import APIRouter, Form, Request, status, Depends, HTTPException, "
    "Query\n"
    "from fastapi.responses import HTMLResponse, RedirectResponse\n"
    "\n"
    "from ..config import get_settings\n"
    "from ..templates import templates\n"
    "# from ..models import TablesEntry\n"
    "\n"
    "from ..crud import login_session_storage_from_db, utcnow\n"
    "from ..database import get_db\n"
    "from sqlalchemy.orm import Session\n"
    "\n"
    "from argon2 import PasswordHasher\n"
    "from argon2.exceptions import HashingError\n"
    "\n"
    "router = APIRouter()\n"
    "settings = get_settings()\n"
    "\n"
    "\n"
    '@router.get("/login", response_class=HTMLResponse)\n'
    "def login_page(request: Request):\n"
    "\n"
    "    return True\n"
    "\n"
    "    return templates.TemplateResponse(\n"
    '        name="login.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_activation": settings.login_activation,\n'
    '            "app_name": settings.app_name,\n'
    '            "section_1_name": settings.section_1_name,\n'
    '            "section_2_name": settings.section_2_name,\n'
    '            "error": None,\n'
    "        },\n"
    "    )\n"
    "\n"
    "\n"
    '@router.post("/login")\n'
    "def login(\n"
    "    request: Request,\n"
    "    username_selector: str = Form(...),\n"
    "    password_selector: str = Form(...),\n"
    "    db: Session = Depends(get_db),\n"
    "):\n"
    "\n"
    "    return True\n"
    "\n"
    "    # -------------------------------\n"
    "    # login credentials usage from DB\n"
    "    # -------------------------------\n"
    "    if login_session_storage_from_db(\n"
    "        db,\n"
    "        request,\n"
    "        username_selector,\n"
    "        password_selector,\n"
    "    ):\n"
    '        return RedirectResponse(url="/", '
    "status_code=status.HTTP_303_SEE_OTHER)\n"
    "\n"
    "    # -------------------------------------\n"
    "\n"
    '    print(f"\\n\\n\\trequest.session: {request.session}\\n\\n")\n'
    "\n"
    "    return templates.TemplateResponse(\n"
    '        name="login.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_activation": settings.login_activation,\n'
    '            "app_name": settings.app_name,\n'
    '            "section_1_name": settings.section_1_name,\n'
    '            "section_2_name": settings.section_2_name,\n'
    '            "error": request.session["login_errors"] if "login_errors" in '
    'request.session else "",\n'
    "        },\n"
    "        status_code=400,\n"
    "    )\n"
    "\n"
    "\n"
    '@router.get("/logout")\n'
    "def logout(request: Request):\n"
    "    request.session.clear()\n"
    '    return RedirectResponse(url="/login", '
    "status_code=status.HTTP_303_SEE_OTHER)\n"
    "\n"
    "\n"
    '@router.get("/register", response_class=HTMLResponse)\n'
    "def login_page(request: Request):\n"
    "\n"
    "    return True\n"
    "\n"
    "    return templates.TemplateResponse(\n"
    '        name="register.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_activation": settings.login_activation,\n'
    '            "app_name": settings.app_name,\n'
    '            "section_1_name": settings.section_1_name,\n'
    '            "section_2_name": settings.section_2_name,\n'
    '            "error": None,\n'
    "        },\n"
    "    )\n"
    "\n"
    "\n"
    '@router.post("/register")\n'
    "async def update_profile_password(\n"
    "    request: Request,\n"
    "    reg_username_field: str = Form(...),\n"
    "    reg_email_field: str = Form(...),\n"
    "    reg_password_field: str = Form(...),\n"
    "    reg_password_retype_field: str = Form(...),\n"
    "    db: Session = Depends(get_db),\n"
    "):\n"
    "\n"
    "    return True\n"
    "\n"
    '    request.session["msg"] = []\n'
    '    request.session["errmsg"] = []\n'
    "\n"
    "    ph = PasswordHasher()\n"
    "\n"
    "    if reg_password_field != reg_password_retype_field:\n"
    '        request.session["errmsg"].append("Passwords do not match")\n'
    "\n"
    "    if len(reg_password_field) < 8:\n"
    '        request.session["errmsg"].append("Password must be at least 8 '
    'characters")\n'
    "\n"
    '    if request.session["errmsg"] == []:\n'
    "        try:\n"
    "            password_hash = ph.hash(reg_password_field)\n"
    "\n"
    "            # USER ADDITION IN DB\n"
    "            user = UsersEntry(\n"
    "                username=reg_username_field,\n"
    "                email=reg_email_field,\n"
    "                password_hash=password_hash,\n"
    "                profile_id=3,\n"
    "                active=0,\n"
    "                created_at=utcnow(),\n"
    "                updated_at=utcnow(),\n"
    "            )\n"
    "            db.add(user)\n"
    "            db.commit()\n"
    "\n"
    "            #   -----------------------------------------\n"
    "            #   REGISTRATION REQUEST EMAIL SEND TO ADMINS\n"
    "            #   -----------------------------------------\n"
    "            adminUsersList = "
    "(db.query(UsersEntry).filter(UsersEntry.profile_id.in_(settings.admin_level)).all())\n"
    '            email_subject = "DUMA Manager Profile Activation Request"\n'
    '            email_body = f"A DUMA Manager profile activation has been '
    'requested for user {reg_username_field} ( {reg_email_field} )"\n'
    "            for adm in adminUsersList:\n"
    "                email_sent = await send_profile_creation_email(adm.email, "
    "email_subject, email_body, reg_email_field)\n"
    "                if email_sent != True:\n"
    '                    request.session["errmsg"].append("Profile creation email '
    'request sent failure")\n'
    "            #   -----------------------------------------\n"
    "\n"
    "        except HashingError:\n"
    "            db.rollback()\n"
    '            request.session["errmsg"].append("Password hashing failed")\n'
    "\n"
    "        except Exception as e:\n"
    "            db.rollback()\n"
    "            print(e)\n"
    '            request.session["errmsg"].append("User creation failed")\n'
    "            \n"
    "    return templates.TemplateResponse(\n"
    '        name="profile_request.html",\n'
    "        request=request,\n"
    "        context={\n"
    '            "request": request,\n'
    '            "settings": settings,\n'
    '            "login_activation": settings.login_activation,\n'
    '            "app_name": settings.app_name,\n'
    '            "section_1_name": settings.section_1_name,\n'
    '            "section_2_name": settings.section_2_name,\n'
    '            "reg_username_field": reg_username_field,\n'
    '            "reg_email_field": reg_email_field,\n'
    "        },\n"
    "    )\n"
    "\n"
    "\n"
    '@router.post("/unregister")\n'
    "def delete_profile(\n"
    "    request: Request,\n"
    "    current_username_value_field: str = Form(...),\n"
    "    db: Session = Depends(get_db),\n"
    "):\n"
    "\n"
    "    return True\n"
    "\n"
    "    try:\n"
    "        user = db.query(UsersEntry).filter(UsersEntry.username == "
    "current_username_value_field).first()\n"
    "        db.delete(user)\n"
    "        db.commit()\n"
    "\n"
    "    except Exception as e:\n"
    "        db.rollback()\n"
    "        print(e)\n"
    '        request.session["errmsg"].append("User removal failed")\n'
    "\n"
    "    request.session.clear()\n"
    '    return RedirectResponse(url="/login", '
    "status_code=status.HTTP_303_SEE_OTHER)\n"
    "\n",
    "app/app/schemas.py": "",
    "app/app/static/css/bootstrap.css": "",
    "app/app/static/css/general.css": "",
    "app/app/static/js/bootstrap.js": "",
    "app/app/static/js/func.js": "",
    "app/app/static/js/jquery.js": "",
    "app/app/templates.py": "from pathlib import Path\n"
    "from fastapi.templating import Jinja2Templates\n"
    "\n"
    "BASE_DIR = Path(__file__).resolve().parent\n"
    'templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))\n'
    "\n",
    "app/app/templates/base.html": "<!DOCTYPE html>\n"
    '<html lang="it">\n'
    "<head>\n"
    '    <meta charset="UTF-8">\n'
    "    <title>{{ page_title }}</title>\n"
    '    <link rel="icon" type="image/png" sizes="32x32" href="../static/img/favicon.png">\n'
    '    <link rel="stylesheet" href="../static/css/bootstrap.css">\n'
    '    <link rel="stylesheet" href="../static/css/general.css">\n'
    '    <script src="../static/js/bootstrap.js"></script>\n'
    '    <script src="../static/js/jquery.js"></script>\n'
    "</head>\n"
    "<body>\n"
    '<div class="container">\n'
    '    <div class="topbar">\n'
    '        <div class="title-header-div"><h1><a href="/">{{ settings.app_name '
    "}}</a></h1></div>\n"
    "    </div>\n"
    "    {% block content %}{% endblock %}\n"
    "</div>\n"
    "</body>\n"
    "</html>\n"
    "\n"
    '<script src="../static/js/func.js"></script>\n'
    "\n",
    "app/app/templates/common/page.html": "",
    "app/app/templates/home.html": '{% extends "base.html" %}\n'
    "\n"
    '{% set page_section = "home" %}\n'
    '{% set page_link = "" %}\n'
    "{% set page_title = settings.app_name %}\n"
    "\n"
    "{% block content %}\n"
    "\n"
    '<div class="utility-bar-div">\n'
    '    <div class="utility-bar">Home Page</div>\n'
    "</div>\n"
    "\n"
    "{% endblock %}\n"
    "\n",
    "app/app/templates/home/page.html": "",
    "app/app/templates/login.html": '{% extends "base.html" %}\n'
    "\n"
    '{% set page_section = "home" %}\n'
    '{% set page_link = "" %}\n'
    "{% set page_title = settings.app_name %}\n"
    "\n"
    "{% block totalrecords %}\n"
    "{% endblock %}\n"
    "\n"
    "{% set loginCmdTXT='Login' %}\n"
    "{% set registerCmdTXT='Register' %}\n"
    "\n"
    "{% block content %}\n"
    '<div class="subTitle-div"><span class="subTitle">Login</span></div>\n'
    '<div class="form-div">\n'
    '<form id="login_row_form" name="login_row_form" method="post" '
    'action="/login">\n'
    '    <div class="login-form-div-container">\n'
    '        <div class="login-block-div-container">\n'
    '            <label class="filter_lbl" id="username_selector_lbl" '
    'for="username_selector">Username</label>\n'
    "        </div>\n"
    '        <div class="login-block-div-container">\n'
    '            <input type="text" class="form-control" '
    'name="username_selector" id="username_selector" placeholder="Username" '
    'value="" required>\n'
    "        </div>\n"
    "    </div>\n"
    '    <div class="login-form-div-container">\n'
    '        <div class="login-block-div-container">\n'
    '            <label class="filter_lbl" id="password_selector_lbl" '
    'for="password_selector">Password</label>\n'
    "        </div>\n"
    '        <div class="login-block-div-container">\n'
    '            <input type="password" class="form-control" '
    'name="password_selector" id="password_selector" placeholder="Password" '
    'value="" required>\n'
    "        </div>\n"
    "    </div>\n"
    '    <div class="login-form-div-container" id="login-result-div">\n'
    "        {% if error %}\n"
    '        <span class="error_msg">{{ error }}</span>\n'
    "        {% endif %}\n"
    "    </div>\n"
    "    <hr />\n"
    '    <button class="btn btn-primary" type="submit" id="login_btn">{{ '
    "loginCmdTXT }}</button>\n"
    '    <button class="btn btn-secondary" type="button" id="register_btn" '
    "onclick=\"document.location.href='/register'\">{{ registerCmdTXT "
    "}}</button>\n"
    "</form>\n"
    "</div>\n"
    "{% endblock %}\n"
    "\n",
    "app/avvio.py": "import os\n"
    "import subprocess\n"
    "\n"
    "try:\n"
    '    if os.name == "nt":\n'
    '        python_exe = r"venv\\Scripts\\python.exe"\n'
    "    else:\n"
    '        python_exe = "venv/bin/python"\n'
    "\n"
    '    subprocess.run([python_exe, "run.py"])\n'
    "\n"
    "except KeyboardInterrupt:\n"
    '    print("\\nInterrotto dall\'utente")\n'
    "\n",
    "app/project_tree.bat": "@echo off\n\nREM Avvia applicazione\npython project_tree.py\n\npause\n\n",
    "app/project_tree.py": "import os\n"
    "import sys\n"
    "\n"
    'EXCLUDE = {"venv", "__pycache__", ".git", ".idea", ".vscode", "node_modules"}\n'
    "\n"
    'def build_tree(root, prefix=""):\n'
    "    lines = []\n"
    "\n"
    "    try:\n"
    "        entries = sorted(\n"
    "            [x for x in os.listdir(root) if x not in EXCLUDE],\n"
    "            key=lambda x: (not os.path.isdir(os.path.join(root, x)), x.lower())\n"
    "        )\n"
    "    except PermissionError:\n"
    '        return [prefix + "[ACCESSO NEGATO]"]\n'
    "\n"
    "    total = len(entries)\n"
    "\n"
    "    for i, name in enumerate(entries):\n"
    "        path = os.path.join(root, name)\n"
    "        is_last = i == total - 1\n"
    "\n"
    '        branch = "└── " if is_last else "├── "\n'
    "        lines.append(prefix + branch + name)\n"
    "\n"
    "        if os.path.isdir(path):\n"
    '            extension = "    " if is_last else "│   "\n'
    "            lines.extend(build_tree(path, prefix + extension))\n"
    "\n"
    "    return lines\n"
    "\n"
    'if __name__ == "__main__":\n'
    '    project_path = "."\n'
    '    output_file = "tree.txt"\n'
    "\n"
    "    lines = [os.path.abspath(project_path)]\n"
    "    lines.extend(build_tree(project_path))\n"
    "\n"
    '    with open(output_file, "w", encoding="utf-8") as f:\n'
    '        f.write("\\n".join(lines))\n'
    "\n"
    '    print(f"Alberatura salvata in {output_file}")\n'
    "\n",
    "app/requirements.txt": "fastapi[standard]\n"
    "fastapi>=0.115.0\n"
    "uvicorn[standard]>=0.30.0\n"
    "sqlalchemy>=2.0.0\n"
    "oracledb>=2.0.0\n"
    "pydantic-settings>=2.0.0\n"
    "httpx>=0.27.0\n"
    "jinja2>=3.1.0\n"
    "python-multipart>=0.0.9\n"
    "requests>=2.25.1\n"
    "PyYAML>=5.4.1\n"
    "openpyxl\n"
    "itsdangerous\n"
    "argon2-cffi>=23.1.0\n"
    "aiosmtplib>=3.0.0\n"
    "\n",
    "app/run.bat": "@echo off\n\nREM Avvia applicazione\npython avvio.py\n\npause\n\n",
    "app/run.py": "import uvicorn\n"
    "from app.config import get_settings\n"
    "\n"
    "settings = get_settings()\n"
    "\n"
    'if __name__ == "__main__":\n'
    "    uvicorn.run(\n"
    '        "app.main:app",\n'
    "        host=settings.host,\n"
    "        port=settings.port,\n"
    "        reload=settings.debug,\n"
    "    )\n"
    "\n",
    "app/run.sh": "#!/bin/bash\npython avvio.py\n\n",
}

DIRECTORIES: tuple[str, ...] = (
    "app",
    "BACKUP",
    "docs",
    "HOWTO",
    "app/app/routers/__pycache__",
    "app/app/static/css",
    "app/app/static/js",
    "app/app/static/img",
    "app/app/templates/home",
    "app/app/templates/common",
    "app/scripts",
)


def clear_screen() -> None:
    command = ["cmd", "/c", "cls"] if os.name == "nt" else ["clear"]
    subprocess.run(command, check=False)


def run(command: list[str], *, cwd: Path, stdout=None) -> None:
    print(f"> {' '.join(map(str, command))}")
    subprocess.run(command, cwd=cwd, check=True, stdout=stdout)


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


def get_venv_python(app_dir: Path) -> Path:
    if os.name == "nt":
        return app_dir / "venv" / "Scripts" / "python.exe"
    return app_dir / "venv" / "bin" / "python"


def create_structure(project_dir: Path) -> None:
    for relative_dir in DIRECTORIES:
        (project_dir / relative_dir).mkdir(parents=True, exist_ok=True)


def write_project_files(project_dir: Path, project_name: str) -> None:
    for relative_name, template in FILES.items():
        destination = project_dir / relative_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = template.replace("$PROJECT_NAME", project_name)
        destination.write_text(content, encoding="utf-8", newline="\n")
        print(f"Creato: {destination}")


def create_environment(project_dir: Path) -> Path:
    app_dir = project_dir / "app"
    requirements = app_dir / "requirements.txt"

    run([sys.executable, "-m", "venv", "venv"], cwd=app_dir)
    venv_python = get_venv_python(app_dir)

    if not venv_python.exists():
        raise FileNotFoundError(f"Python del virtualenv non trovato: {venv_python}")

    run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=app_dir,
    )
    run(
        [str(venv_python), "-m", "pip", "install", "-r", str(requirements)],
        cwd=app_dir,
    )

    freeze_file = app_dir / "requirements_freeze.txt"
    with freeze_file.open("w", encoding="utf-8", newline="\n") as stream:
        run(
            [str(venv_python), "-m", "pip", "freeze"],
            cwd=app_dir,
            stdout=stream,
        )

    return venv_python


def print_summary(project_dir: Path, project_name: str) -> None:
    clear_screen()
    print("=" * 90)
    print(f" PROJECT '{project_name}' CREATION ...")
    print("=" * 90)
    print("\nFilesystem structure has been correctly generated.")
    print(f"\nMain folder:\n - {project_dir}")
    print("\nHOWTO generated:\n - HOWTO/HOW_TO.md")
    print("\nApplication is ready.")
    print("=" * 90)


def main() -> None:
    project_root_text = input(f"Project root [{DEFAULT_PROJECT_PATH}]: ").strip()
    project_root = (
        Path(project_root_text).expanduser().resolve()
        if project_root_text
        else DEFAULT_PROJECT_PATH
    )

    project_name = ask_project_name()
    project_dir = project_root / project_name

    if project_dir.exists():
        raise FileExistsError(f"La cartella esiste già: {project_dir}")

    project_dir.mkdir(parents=True)

    try:
        create_structure(project_dir)
        write_project_files(project_dir, project_name)
        venv_python = create_environment(project_dir)
        print_summary(project_dir, project_name)

        app_dir = project_dir / "app"
        print(f"\nAvvio applicazione da: {app_dir}")
        run([str(venv_python), "run.py"], cwd=app_dir)

    except KeyboardInterrupt:
        print("\nInterrotto dall'utente")
        raise SystemExit(130)
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"\nErrore durante la creazione del progetto: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
