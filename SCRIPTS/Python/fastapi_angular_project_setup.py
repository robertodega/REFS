import os
import subprocess
import sys
import time
from pathlib import Path

# File da generare
FILES = {
    # -------------------------------------------------------------------------
    # BACKEND (FastAPI + SQLModel + SQLite)
    # -------------------------------------------------------------------------
    "backend/main.py": '''from typing import List, Optional
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select

# 1. Modello Database dimostrativo
class ProjectStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    module: str
    status: str

# 2. Configurazione Database SQLite
sqlite_file_name = "app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# 3. Inizializzazione FastAPI
app = FastAPI(title="App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(ProjectStatus)).all():
            initial_status = [
                ProjectStatus(module="FastAPI Backend", status="Attivo"),
                ProjectStatus(module="SQLite Database", status="Connesso"),
                ProjectStatus(module="Angular Frontend", status="In esecuzione")
            ]
            for item in initial_status:
                session.add(item)
            session.commit()

# 4. Endpoints API
@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "message": "Backend operativo",
        "version": "1.0.0"
    }

@app.get("/api/status", response_model=List[ProjectStatus])
def get_system_status(session: Session = Depends(get_session)):
    return session.exec(select(ProjectStatus)).all()
''',

    "backend/requirements.txt": """fastapi>=0.110.0
uvicorn>=0.28.0
sqlmodel>=0.0.16
""",

    # -------------------------------------------------------------------------
    # FRONTEND (Configurazioni Angular)
    # -------------------------------------------------------------------------
    "frontend/src/index.html": '''<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>Benvenuto nel Progetto</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="bg-slate-950 text-slate-100 antialiased font-sans">
  <app-root></app-root>
</body>
</html>
''',

    "frontend/src/main.ts": '''import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
''',

    "frontend/src/app/app.config.ts": '''import { ApplicationConfig, provideZonelessChangeDetection } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZonelessChangeDetection(),
    provideHttpClient()
  ]
};
''',

    # -------------------------------------------------------------------------
    # FRONTEND (Interfaccia di Benvenuto Semplice e Professionale)
    # -------------------------------------------------------------------------
    "frontend/src/app/app.component.ts": '''import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface SystemStatus {
  id?: number;
  module: string;
  status: string;
}

interface HealthResponse {
  status: string;
  message: string;
  version: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  private http = inject(HttpClient);

  isBackendOnline = false;
  backendMessage = 'Verifica connessione in corso...';
  systemModules: SystemStatus[] = [];

  ngOnInit() {
    this.checkHealth();
    this.loadStatus();
  }

  checkHealth() {
    this.http.get<HealthResponse>('http://localhost:8000/api/health')
      .subscribe({
        next: (res) => {
          this.isBackendOnline = true;
          this.backendMessage = res.message;
        },
        error: () => {
          this.isBackendOnline = false;
          this.backendMessage = 'Backend non raggiungibile';
        }
      });
  }

  loadStatus() {
    this.http.get<SystemStatus[]>('http://localhost:8000/api/status')
      .subscribe({
        next: (data) => this.systemModules = data,
        error: () => this.systemModules = []
      });
  }
}
''',

    "frontend/src/app/app.component.html": '''<div class="min-h-screen flex flex-col justify-between p-6 md:p-12">
  
  <!-- Header / Navigation Bar -->
  <header class="max-w-5xl mx-auto w-full flex justify-between items-center pb-6 border-b border-slate-800/80">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
        P
      </div>
      <span class="font-semibold tracking-wide text-slate-200">Workspace App</span>
    </div>
    
    <div class="flex items-center gap-2 text-xs font-medium px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800">
      <span class="w-2 h-2 rounded-full" [ngClass]="isBackendOnline ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'"></span>
      <span class="text-slate-400">{{ backendMessage }}</span>
    </div>
  </header>

  <!-- Main Welcome Hero Section -->
  <main class="max-w-5xl mx-auto w-full my-auto py-12">
    <div class="max-w-2xl">
      <span class="text-xs font-semibold tracking-widest uppercase text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-full">
        Ambiente configurato
      </span>
      
      <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white mt-4 leading-tight">
        Benvenuto nel tuo nuovo progetto Full-Stack.
      </h1>
      
      <p class="text-slate-400 text-base md:text-lg mt-4 leading-relaxed">
        L'architettura è pronta ed operativa. L'applicazione è configurata con Angular per l'interfaccia utente, FastAPI per la gestione delle API e SQLite per la persistenza dei dati.
      </p>

      <div class="mt-8 flex flex-wrap gap-4">
        <a 
          href="http://localhost:8000/docs" 
          target="_blank" 
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/25"
        >
          <span>Documentazione API</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </a>
      </div>
    </div>

    <!-- Status Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12 pt-8 border-t border-slate-800/50">
      @for (item of systemModules; track item.id) {
        <div class="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80 flex items-center justify-between">
          <span class="text-sm font-medium text-slate-300">{{ item.module }}</span>
          <span class="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-md border border-emerald-500/20">
            {{ item.status }}
          </span>
        </div>
      }
    </div>
  </main>

  <!-- Footer -->
  <footer class="max-w-5xl mx-auto w-full text-center text-xs text-slate-600 pt-6 border-t border-slate-800/80">
    Angular + FastAPI + SQLite Architecture Template
  </footer>

</div>
''',

    "frontend/src/app/app.component.css": """@import "tailwindcss";
""",

    # -------------------------------------------------------------------------
    # SCRIPT DI AVVIO E ARRESTO
    # -------------------------------------------------------------------------
    "start.py": '''import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

def get_venv_python():
    if sys.platform == "win32":
        return BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    return BACKEND_DIR / "venv" / "bin" / "python"

def main():
    print("Avvio dei servizi in corso...")
    
    python_venv = get_venv_python()
    if not python_venv.exists():
        print("Errore: Virtualenv non trovato. Esegui prima il setup!")
        sys.exit(1)

    # 1. Avvio Backend FastAPI
    print("-> Avvio Backend (FastAPI + SQLite su http://localhost:8000)...")
    backend_proc = subprocess.Popen(
        [str(python_venv), "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
        cwd=str(BACKEND_DIR)
    )
    (ROOT_DIR / ".backend.pid").write_text(str(backend_proc.pid))

    # 2. Avvio Frontend Angular
    print("-> Avvio Frontend (Angular su http://localhost:4200)...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "start"],
        cwd=str(FRONTEND_DIR)
    )
    (ROOT_DIR / ".frontend.pid").write_text(str(frontend_proc.pid))

    print("\\nIn attesa del caricamento dei servizi...")
    time.sleep(5)
    
    print("Apertura del browser...")
    webbrowser.open("http://localhost:4200")
    
    print("\\nServizi avviati con successo!")
    print("Per fermare l'applicazione, esegui: python stop.py")

if __name__ == "__main__":
    main()
''',

    "stop.py": '''import os
import signal
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()

def stop_process(pid_file):
    path = ROOT_DIR / pid_file
    if not path.exists():
        return
        
    try:
        pid = int(path.read_text().strip())
        print(f"Terminazione processo PID {pid} ({pid_file})...")
        
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, signal.SIGTERM)
            
    except Exception as e:
        print(f"Errore durante l'arresto di {pid_file}: {e}")
    finally:
        if path.exists():
            path.unlink()

if __name__ == "__main__":
    stop_process(".backend.pid")
    stop_process(".frontend.pid")
    print("Tutti i servizi sono stati arrestati.")
'''
}

def create_structure():
    # 1. Richiesta del nome del progetto
    project_name = input("Inserisci il nome del progetto: ").strip()
    if not project_name:
        print("Errore: Il nome del progetto non può essere vuoto.")
        sys.exit(1)

    project_dir = Path(project_name).resolve()
    
    if project_dir.exists() and any(project_dir.iterdir()):
        print(f"Attenzione: La cartella '{project_name}' esiste già e non è vuota.")
        conferma = input("Vuoi continuare comunque? (s/N): ").strip().lower()
        if conferma != 's':
            print("Operazione annullata.")
            sys.exit(0)
            
    project_dir.mkdir(parents=True, exist_ok=True)
    backend_dir = (project_dir / "backend").resolve()
    frontend_dir = (project_dir / "frontend").resolve()
    backend_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nInizializzazione progetto in: {project_dir}")

    # 2. Inizializzazione Angular tramite CLI
    if not frontend_dir.exists():
        print("Creazione progetto Angular tramite Angular CLI...")
        ng_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
        subprocess.run([
            ng_cmd, "-p", "@angular/cli", "ng", "new", "frontend",
            "--style=css", "--routing=false", "--skip-git", "--skip-install", "--ssr=false"
        ], cwd=str(project_dir), check=True)

    # 3. Scrittura dei file
    for path_str, content in FILES.items():
        file_path = project_dir / path_str
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Creato/Aggiornato: {project_name}/{path_str}")

    # 4. Creazione Ambiente Virtuale (venv)
    venv_dir = (backend_dir / "venv").resolve()
    print(f"\nCreazione ambiente virtuale Python in {venv_dir}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    # 5. Dipendenze Backend
    print("Installazione dipendenze Python nell'ambiente virtuale...")
    req_file = (backend_dir / "requirements.txt").resolve()
    subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(req_file)], cwd=str(backend_dir), check=True)

    # 6. Dipendenze Frontend
    print("\nInstallazione pacchetti npm (Angular + Tailwind)...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    subprocess.run([npm_cmd, "install"], cwd=str(frontend_dir), check=True)
    subprocess.run([npm_cmd, "install", "@tailwindcss/vite@latest"], cwd=str(frontend_dir), check=True)

    print("\n" + "="*60)
    print("SETUP COMPLETATO CON SUCCESSO!")
    print("Spostamento nella cartella di progetto e avvio dell'app...")
    print("="*60 + "\n")

    # 7. Spostamento nella cartella di progetto ed esecuzione di start.py
    os.chdir(project_dir)
    subprocess.run([sys.executable, "start.py"])

if __name__ == "__main__":
    create_structure()