#!/bin/bash

# ==================================
# FASTAPI PROJECT STRUCTURE CREATION
# ==================================

while true
do
    clear

    echo "========================================"
    echo "        NEW PROJECT CREATION"
    echo "========================================"
    echo ""

    read -p "Project name ( type in '0' to abort ): " PROJECT_NAME

    if [ "../$PROJECT_NAME" = "0" ]; then
        echo "Aborting Operation ..."
        exit 0
    fi

    if [ -n "../$PROJECT_NAME" ]; then
        break
    fi

    echo "Project Name cannot be empty"
done

# ================
# FOLDERS CREATION
# ================

mkdir -p "../$PROJECT_NAME"/{app,BACKUP,docs,HOWTO,app/app/routers/__pycache__,app/app/static/css,app/app/static/js,app/app/static/img,app/app/templates/home,app/app/templates/common,app/scripts}

# ==============
# FILES CREATION
# ==============

touch "../$PROJECT_NAME/app/README.md"
touch "../$PROJECT_NAME/app/run.sh"

touch "../$PROJECT_NAME/app/app/__init__.py"
touch "../$PROJECT_NAME/app/app/schemas.py"

touch "../$PROJECT_NAME/app/app/routers/__init__.py"

touch "../$PROJECT_NAME/app/app/static/css/bootstrap.css"
touch "../$PROJECT_NAME/app/app/static/css/style.css"

touch "../$PROJECT_NAME/app/app/static/js/func.js"
touch "../$PROJECT_NAME/app/app/static/js/bootstrap.js"
touch "../$PROJECT_NAME/app/app/static/js/jquery.js"

touch "../$PROJECT_NAME/app/app/templates/base.html"
touch "../$PROJECT_NAME/app/app/templates/home.html"
touch "../$PROJECT_NAME/app/app/templates/login.html"
touch "../$PROJECT_NAME/app/app/templates/home/page.html"
touch "../$PROJECT_NAME/app/app/templates/common/page.html"

# ======================
# .env FILE CREATION
# ======================
cat > "../$PROJECT_NAME/app/.env" <<EOF
#   APP VARS ----------------------------------------------------------------------------------------------
APP_NAME=$PROJECT_NAME
APP_ENV=dev                         #   dev | prod
DEBUG=false
HOST=127.0.0.1
PORT=8000
#   APP VARS ----------------------------------------------------------------------------------------------

#   EMAIL MANAGEMENT --------------------------------------------------------------------------------------
SMTP_HOST = ""
SMTP_PORT = 587
SMTP_USER = ""
SMTP_PASSWORD = ""
#   EMAIL MANAGEMENT --------------------------------------------------------------------------------------

#   LOGIN -------------------------------------------------------------------------------------------------
LOGIN_ACTIVATION=true
ALLOWED_MSG="Current user is allowed to use this section"
NOT_ALLOWED_MSG="Current user is not allowed to use this section"
ADMIN_LEVEL=["1"]
USER_LEVEL=["1", "2"]
GUEST_LEVEL=["1", "2", "3"]
#   LOGIN -------------------------------------------------------------------------------------------------

#   VARIABLES ---------------------------------------------------------------------------------------------
LOG_LEVEL=INFO

ENABLE_DOCS=true                    #   true | false
DOCS_URL=/docs
OPENAPI_URL=/openapi.json

# ORACLE DB PARAMS
ORACLE_USER=campisi
ORACLE_PASSWORD=campisipwd
ORACLE_HOST=oraclelnx02             #   oraclelnx02 | 192.168.200.4
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=antana

DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=1800
DB_POOL_TIMEOUT=30
#   VARIABLES ---------------------------------------------------------------------------------------------


EOF

# =======================
# config.py FILE CREATION
# =======================
cat > "../$PROJECT_NAME/app/app/config.py" <<EOF
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #   APP VARS ----------------------------------------------------------------------------------------------
    app_name: str
    app_env: str
    debug: bool
    host: str
    port: int
    #   APP VARS ----------------------------------------------------------------------------------------------

    #   EMAIL MANAGEMENT -------------------------------------------
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    #   EMAIL MANAGEMENT -------------------------------------------

    #   LOGIN -----------------------------------------------------
    login_activation: bool
    allowed_msg: str
    not_allowed_msg: str
    admin_level: list
    user_level: list
    guest_level: list
    #   LOGIN -----------------------------------------------------

    #   VARIABLES ---------------------------------------------------------------------------------------------
    log_level: str = "INFO"

    enable_docs: bool = False  #   True | False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"

    # ORACLE DB PARAMS
    oracle_user: str
    oracle_password: str
    oracle_host: str
    oracle_port: int = 1521
    oracle_service_name: str

    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 1800
    db_pool_timeout: int = 30
    #   VARIABLES ---------------------------------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def oracle_dsn(self) -> str:
        return (
            f"oracle+oracledb://{self.oracle_user}:{self.oracle_password}"
            f"@{self.oracle_host}:{self.oracle_port}/?service_name={self.oracle_service_name}"
        )

    @property
    def effective_docs_url(self) -> str | None:
        return self.docs_url if self.enable_docs else None

    @property
    def effective_openapi_url(self) -> str | None:
        return self.openapi_url if self.enable_docs else None


@lru_cache
def get_settings() -> Settings:
    return Settings()

EOF

# ===============================
# models.py FILE CREATION
# ===============================
cat > "../$PROJECT_NAME/app/app/models.py" <<EOF
from sqlalchemy import String, Integer, DateTime, Boolean, Column, Numeric, CLOB, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.sql import func
from .database import Base

class UsersEntry(Base):
    __tablename__ = "TBU_NEWPROJ_LOGIN_USERS"

    id = Column("ID", NUMBER(38, 0), primary_key=True)
    username = Column("USERNAME", String(100), nullable=False, unique=True)
    email = Column("EMAIL", String(100), nullable=False, unique=True)
    password_hash = Column("PASSWORD_HASH", String(255), nullable=False)
    profile_id = Column("PROFILE_ID", String(2), nullable=True)
    active: Mapped[bool] = mapped_column("ACTIVE", Boolean)
    created_at = Column(
        "CREATED_AT",
        DateTime,
        nullable=True,
        server_default=func.now(),
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime,
        nullable=True,
        server_default=func.now(),
    )

EOF

# ===============================
# import_manager.py FILE CREATION
# ===============================
cat > "../$PROJECT_NAME/app/app/import_manager.py" <<EOF
from pydantic import BaseModel


class ImportErrorDetail(BaseModel):
    row: int
    message: str


class ImportResult(BaseModel):
    imported: int
    skipped: int
    errors: list[ImportErrorDetail]


EOF

# =====================
# crud.py FILE CREATION
# =====================
cat > "../$PROJECT_NAME/app/app/crud.py" <<EOF
import json
from datetime import datetime, timezone
from sqlalchemy import func, or_, select, text, update
from sqlalchemy.orm import Session
from sqlalchemy.dialects import oracle
# from .models import (
#     TableEntry,
# )
from fastapi import Request, status, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from .config import get_settings

from pathlib import Path
import yaml

import subprocess, sys

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from io import BytesIO
from openpyxl import load_workbook
from .import_manager import ImportErrorDetail, ImportResult

from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import aiosmtplib

settings = get_settings()

def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


#   LOGIN -----------------------------------------------------


def get_session_secret_key_from_db(db: Session) -> str:
    
    return True
    
    stmt = text("""
        SELECT CONFIG_VALUE
        FROM TBU_NEWPROJ_LOGIN_KEYS
        WHERE CONFIG_KEY = 'SESSION_SECRET_KEY'
    """)

    value = db.execute(stmt).scalar_one_or_none()

    if not value:
        raise RuntimeError("SESSION_SECRET_KEY non trovata in Oracle")

    return value


def login_session_storage_from_db(
    db: Session,
    request: Request,
    username: str,
    password: str,
) -> bool:

    return True

    stmt = text("""
        SELECT 
            usr.ID as user_id
                , usr.USERNAME as username
                , usr.EMAIL as email
                , usr.PASSWORD_HASH as password_hash
                , usr.PROFILE_ID as profile_id
                , usr.ACTIVE as active
                , prof.NAME as profile_name
            FROM 
                TBU_NEWPROJ_LOGIN_USERS usr
                left join TBU_NEWPROJ_LOGIN_PROFILES prof on prof.id = usr.profile_id
            WHERE USERNAME = :username
    """)

    result = db.execute(stmt, {"username": username}).mappings().first()

    if result is None:
        err_msg = f"Wrong user '{username}'"
        print(f"\n\n\t{err_msg}\n\n")
        request.session["login_errors"] = err_msg
        return False

    if result["active"] == 0:
        err_msg = f"Access for user '{username}' is not allowed"
        print(f"\n\n\t{err_msg}\n\n")
        request.session["login_errors"] = err_msg
        return False

    ph = PasswordHasher()
    try:
        if ph.verify(result["password_hash"], password):
            pass
    except VerifyMismatchError:
        err_msg = f"Wrong Inserted Password for user '{username}'"
        print(f"\n\n\t{err_msg}\n\n")
        request.session["login_errors"] = err_msg
        return False

    request.session["app_env"] = settings.app_env
    request.session["user_id"] = result["user_id"]
    request.session["username"] = result["username"]
    request.session["password_hash"] = result["password_hash"]
    request.session["profile_id"] = result["profile_id"]
    request.session["profile_name"] = result["profile_name"]

    return True


def check_login(request: Request, credential_type: list[str]):
    if settings.login_activation:
        if not request.session.get("username"):
            return False
        else:
            if request.session.get("profile_id") not in credential_type:
                print(f"\t{settings.not_allowed_msg}\n")
                return False
            else:
                return True
    else:
        return True


#   LOGIN -----------------------------------------------------

EOF

# =========================
# database.py FILE CREATION
# =========================
cat > "../$PROJECT_NAME/app/app/database.py" <<EOF
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import get_settings

settings = get_settings()

engine = create_engine(
    settings.oracle_dsn,
    pool_pre_ping=True,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    pool_timeout=settings.db_pool_timeout,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

EOF

# ==========================
# templates.py FILE CREATION
# ==========================
cat > "../$PROJECT_NAME/app/app/templates.py" <<EOF
from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

EOF

# =====================
# home.py FILE CREATION
# =====================
cat > "../$PROJECT_NAME/app/app/routers/home.py" <<EOF
import logging

from fastapi import (
    APIRouter,
    Request,
    status,
    Form,
    Depends,
    HTTPException,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..templates import templates
# from ..models import TableEntry
from ..crud import (
    check_login,
    utcnow,
)

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError

router = APIRouter()
settings = get_settings()


@router.get("/", response_class=HTMLResponse)
def get_home_page(
    request: Request,
    db: Session = Depends(get_db),
):
    
    return templates.TemplateResponse(
        name="home.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_activation": settings.login_activation,
        },
    )

    # ----- LOGIN -----

    login_msg_err = ""
    # allowed_level = settings.admin_level
    # allowed_level = settings.user_level
    allowed_level = settings.guest_level
    allowed_msg = check_login(request, allowed_level)
    if not allowed_msg:
        login_msg_err = settings.not_allowed_msg
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # ----- LOGIN -----

    pending_profiles = db.query(UsersEntry).filter(UsersEntry.active == 0).all()

    return templates.TemplateResponse(
        name="home.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_msg_err": login_msg_err,
            "allowed_msg": allowed_msg,
            "pending_profiles_length": len(pending_profiles),
            "allowed_value": False if allowed_msg == settings.not_allowed_msg else True,
        },
    )

EOF

# =======================
# base.html FILE CREATION
# =======================
cat > "../$PROJECT_NAME/app/app/templates/base.html" <<EOF
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
    <link rel="stylesheet" href="../static/css/bootstrap.css">
    <link rel="stylesheet" href="../static/css/style.css">
    <script src="../static/js/bootstrap.js"></script>
    <script src="../static/js/jquery.js"></script>
</head>
<body>
<div class="container">
    <div class="topbar">
        <div class="title-header-div"><h1><a href="/">{{ settings.app_name }}</a></h1></div>
    </div>
    {% block content %}{% endblock %}
</div>
</body>
</html>

<script src="../static/js/func.js"></script>

EOF

# =======================
# home.html FILE CREATION
# =======================
cat > "../$PROJECT_NAME/app/app/templates/home.html" <<EOF
{% extends "base.html" %}

{% set page_section = "home" %}
{% set page_link = "" %}
{% set page_title = settings.app_name %}

{% block content %}

<div class="utility-bar-div">
    <div class="utility-bar">Home Page</div>
</div>

{% endblock %}

EOF

# =======================
# login.html FILE CREATION
# =======================
cat > "../$PROJECT_NAME/app/app/templates/login.html" <<EOF
{% extends "base.html" %}

{% set page_section = "home" %}
{% set page_link = "" %}
{% set page_title = settings.app_name %}

{% block totalrecords %}
{% endblock %}

{% set loginCmdTXT='Login' %}
{% set registerCmdTXT='Register' %}

{% block content %}
<div class="subTitle-div"><span class="subTitle">Login</span></div>
<div class="form-div">
<form id="login_row_form" name="login_row_form" method="post" action="/login">
    <div class="login-form-div-container">
        <div class="login-block-div-container">
            <label class="filter_lbl" id="username_selector_lbl" for="username_selector">Username</label>
        </div>
        <div class="login-block-div-container">
            <input type="text" class="form-control" name="username_selector" id="username_selector" placeholder="Username" value="" required>
        </div>
    </div>
    <div class="login-form-div-container">
        <div class="login-block-div-container">
            <label class="filter_lbl" id="password_selector_lbl" for="password_selector">Password</label>
        </div>
        <div class="login-block-div-container">
            <input type="password" class="form-control" name="password_selector" id="password_selector" placeholder="Password" value="" required>
        </div>
    </div>
    <div class="login-form-div-container" id="login-result-div">
        {% if error %}
        <span class="error_msg">{{ error }}</span>
        {% endif %}
    </div>
    <hr />
    <button class="btn btn-primary" type="submit" id="login_btn">{{ loginCmdTXT }}</button>
    <button class="btn btn-secondary" type="button" id="register_btn" onclick="document.location.href='/register'">{{ registerCmdTXT }}</button>
</form>
</div>
{% endblock %}

EOF

# ======================
# login.py FILE CREATION
# ======================
cat > "../$PROJECT_NAME/app/app/routers/login.py" <<EOF
from fastapi import APIRouter, Form, Request, status, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import get_settings
from ..templates import templates
# from ..models import TablesEntry

from ..crud import login_session_storage_from_db, utcnow
from ..database import get_db
from sqlalchemy.orm import Session

from argon2 import PasswordHasher
from argon2.exceptions import HashingError

router = APIRouter()
settings = get_settings()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return True

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_activation": settings.login_activation,
            "app_name": settings.app_name,
            "section_1_name": settings.section_1_name,
            "section_2_name": settings.section_2_name,
            "error": None,
        },
    )


@router.post("/login")
def login(
    request: Request,
    username_selector: str = Form(...),
    password_selector: str = Form(...),
    db: Session = Depends(get_db),
):

    return True

    # -------------------------------
    # login credentials usage from DB
    # -------------------------------
    if login_session_storage_from_db(
        db,
        request,
        username_selector,
        password_selector,
    ):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # -------------------------------------

    print(f"\n\n\trequest.session: {request.session}\n\n")

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_activation": settings.login_activation,
            "app_name": settings.app_name,
            "section_1_name": settings.section_1_name,
            "section_2_name": settings.section_2_name,
            "error": request.session["login_errors"] if "login_errors" in request.session else "",
        },
        status_code=400,
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/register", response_class=HTMLResponse)
def login_page(request: Request):

    return True

    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_activation": settings.login_activation,
            "app_name": settings.app_name,
            "section_1_name": settings.section_1_name,
            "section_2_name": settings.section_2_name,
            "error": None,
        },
    )


@router.post("/register")
async def update_profile_password(
    request: Request,
    reg_username_field: str = Form(...),
    reg_email_field: str = Form(...),
    reg_password_field: str = Form(...),
    reg_password_retype_field: str = Form(...),
    db: Session = Depends(get_db),
):

    return True

    request.session["msg"] = []
    request.session["errmsg"] = []

    ph = PasswordHasher()

    if reg_password_field != reg_password_retype_field:
        request.session["errmsg"].append("Passwords do not match")

    if len(reg_password_field) < 8:
        request.session["errmsg"].append("Password must be at least 8 characters")

    if request.session["errmsg"] == []:
        try:
            password_hash = ph.hash(reg_password_field)

            # USER ADDITION IN DB
            user = UsersEntry(
                username=reg_username_field,
                email=reg_email_field,
                password_hash=password_hash,
                profile_id=3,
                active=0,
                created_at=utcnow(),
                updated_at=utcnow(),
            )
            db.add(user)
            db.commit()

            #   -----------------------------------------
            #   REGISTRATION REQUEST EMAIL SEND TO ADMINS
            #   -----------------------------------------
            adminUsersList = (db.query(UsersEntry).filter(UsersEntry.profile_id.in_(settings.admin_level)).all())
            email_subject = "DUMA Manager Profile Activation Request"
            email_body = f"A DUMA Manager profile activation has been requested for user {reg_username_field} ( {reg_email_field} )"
            for adm in adminUsersList:
                email_sent = await send_profile_creation_email(adm.email, email_subject, email_body, reg_email_field)
                if email_sent != True:
                    request.session["errmsg"].append("Profile creation email request sent failure")
            #   -----------------------------------------

        except HashingError:
            db.rollback()
            request.session["errmsg"].append("Password hashing failed")

        except Exception as e:
            db.rollback()
            print(e)
            request.session["errmsg"].append("User creation failed")
            
    return templates.TemplateResponse(
        name="profile_request.html",
        request=request,
        context={
            "request": request,
            "settings": settings,
            "login_activation": settings.login_activation,
            "app_name": settings.app_name,
            "section_1_name": settings.section_1_name,
            "section_2_name": settings.section_2_name,
            "reg_username_field": reg_username_field,
            "reg_email_field": reg_email_field,
        },
    )


@router.post("/unregister")
def delete_profile(
    request: Request,
    current_username_value_field: str = Form(...),
    db: Session = Depends(get_db),
):

    return True

    try:
        user = db.query(UsersEntry).filter(UsersEntry.username == current_username_value_field).first()
        db.delete(user)
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        request.session["errmsg"].append("User removal failed")

    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

EOF

# =======================
# main.py FILE CREATION
# =======================
cat > "../$PROJECT_NAME/app/app/main.py" <<EOF
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# ----- LOGIN -----

import os
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text
from .database import SessionLocal
from .crud import get_session_secret_key_from_db

# ----- LOGIN -----

from .config import get_settings
from .routers import home, login

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url=settings.effective_docs_url,
    openapi_url=settings.effective_openapi_url,
    redoc_url=None,
)

# ----- LOGIN -----

# User | Password | Profile Authentication system
# --------------------------
# SESSION_SECRET_KEY from DB
# --------------------------
db = SessionLocal()
try:
    session_secret_key = get_session_secret_key_from_db(db)
finally:
    db.close()

app.add_middleware(
    SessionMiddleware,
    secret_key=session_secret_key,
    session_cookie="projects_name_session",
)

# ----- LOGIN -----

base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")

app.include_router(home.router)


EOF

# ======================
# avvio.py FILE CREATION
# ======================

cat > "../$PROJECT_NAME/app/avvio.py" <<EOF
import os
import subprocess

try:
    if os.name == "nt":
        python_exe = r"venv\Scripts\python.exe"
    else:
        python_exe = "venv/bin/python"

    subprocess.run([python_exe, "run.py"])

except KeyboardInterrupt:
    print("\nInterrotto dall'utente")

EOF

# ==============================
# project_tree bat FILE CREATION
# ==============================

cat > "../$PROJECT_NAME/app/project_tree.bat" <<EOF
@echo off

REM Avvia applicazione
python project_tree.py

pause

EOF

# ==============================
# project_tree py FILE CREATION
# ==============================

cat > "../$PROJECT_NAME/app/project_tree.py" <<EOF
import os
import sys

EXCLUDE = {"venv", "__pycache__", ".git", ".idea", ".vscode", "node_modules"}

def build_tree(root, prefix=""):
    lines = []

    try:
        entries = sorted(
            [x for x in os.listdir(root) if x not in EXCLUDE],
            key=lambda x: (not os.path.isdir(os.path.join(root, x)), x.lower())
        )
    except PermissionError:
        return [prefix + "[ACCESSO NEGATO]"]

    total = len(entries)

    for i, name in enumerate(entries):
        path = os.path.join(root, name)
        is_last = i == total - 1

        branch = "└── " if is_last else "├── "
        lines.append(prefix + branch + name)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            lines.extend(build_tree(path, prefix + extension))

    return lines

if __name__ == "__main__":
    project_path = "."
    output_file = "tree.txt"

    lines = [os.path.abspath(project_path)]
    lines.extend(build_tree(project_path))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Alberatura salvata in {output_file}")

EOF

# ==============================
# requirements.txt FILE CREATION
# ==============================

cat > "../$PROJECT_NAME/app/requirements.txt" <<EOF
fastapi[standard]
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
oracledb>=2.0.0
pydantic-settings>=2.0.0
httpx>=0.27.0
jinja2>=3.1.0
python-multipart>=0.0.9
requests>=2.25.1
PyYAML>=5.4.1
openpyxl
itsdangerous
argon2-cffi>=23.1.0
aiosmtplib>=3.0.0

EOF

# =====================
# run.bat FILE CREATION
# =====================

cat > "../$PROJECT_NAME/app/run.bat" <<EOF
@echo off

REM Avvia applicazione
python avvio.py

pause

EOF

# ====================
# run.py FILE CREATION
# ====================

cat > "../$PROJECT_NAME/app/run.py" <<EOF
import uvicorn
from app.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

EOF

# ====================
# run.sh FILE CREATION
# ====================
cat > "../$PROJECT_NAME/app/run.sh" <<EOF
#!/bin/bash
python avvio.py

EOF

# =======================
# gitignore FILE CREATION
# =======================

cat > "../$PROJECT_NAME/app/.gitignore" <<EOF
# Python
__pycache__/
app/__pycache__/
app/routers/__pycache__/
*.py[cod]
*$py.class
.ipynb_checkpoints

# Ambiente virtuale
.venv/
venv/
ENV/
env/

# FastAPI / Uvicorn / Database
.env
db.sqlite3
*.db

# IDE
.vscode/
.idea/

# Test e Copertura
htmlcov/
.tox/
.coverage
.pytest_cache/

# Package
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.yml

EOF

# ===================
# HOWTO FILE CREATION
# ===================

cat > "../$PROJECT_NAME/HOWTO/HOW_TO.md" <<EOF
# Project creation

- nano requirements.txt

        fastapi[standard]
        fastapi>=0.115.0
        uvicorn[standard]>=0.30.0
        sqlalchemy>=2.0.0
        oracledb>=2.0.0
        pydantic-settings>=2.0.0
        httpx>=0.27.0
        jinja2>=3.1.0
        python-multipart>=0.0.9
        requests>=2.25.1
        PyYAML>=5.4.1
        openpyxl

# Project Activation

    python -m venv venv
    source venv/Scripts/activate        # Windows installation
    source venv/bin/activate            # Linux installation
    pip install -r requirements.txt

# Project Customization

# Project Run

    from folder /c/xampp/htdocs/PROJECTS/DUMA/$PROJECT_NAME

    - from terminal:
            source venv/Scripts/activate    ( running on Windows )
            source venv/bin/activate        ( running on Linux )
            python run.py

    - from executable:
            CLICK on 'run.bat' file

# Project view

    http://127.0.0.1:8000/
    http://127.0.0.1:8000/docs

EOF

clear

echo "=========================================================================================="
echo " PROJECT '$PROJECT_NAME' CREATION ..."
echo "=========================================================================================="
echo ""
echo "filesystem structure has been correctly generated."
echo ""
echo "Main folder:"
echo " - $PROJECT_NAME"
echo ""
echo "HOWTO generated:"
echo " - HOWTO/HOW_TO.md"
echo ""
echo "Application is ready."
echo "=========================================================================================="

echo ""
echo "=========================================================================================="
echo "Project '$PROJECT_NAME' activation ..."
echo "=========================================================================================="
cd "../$PROJECT_NAME" || exit
cd "app"

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
pip freeze > requirements_freeze.txt

# python avvio.py

python run.py
