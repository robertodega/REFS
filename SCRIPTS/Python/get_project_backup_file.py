import os

"""
cd into folder you want to trace to build the project construction script, then run this script.
The script will create a file named 'project_construction.py' containing all the files and folders of the project, and a function to reconstruct the entire project structure and files with a single execution.
"""
OUTPUT_FILE = "project_construction.py"

IGNORE_LIST = {
    "venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    ".idea",
    OUTPUT_FILE,
    "pack_project.py",
    "tree.txt",
}


def should_ignore(path):
    """Verifica se il percorso contiene elementi da ignorare."""
    parts = path.split(os.sep)
    return any(part in IGNORE_LIST for part in parts)


def generate_construction_script():
    project_files = {}

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]

        if should_ignore(root):
            continue

        for file in files:
            if file in IGNORE_LIST:
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, ".").replace("\\", "/")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                project_files[relative_path] = content
                print(f"Impacchettato: {relative_path}")
            except Exception as e:
                print(
                    f"Saltato {relative_path} (probabilmente binario o non UTF-8): {e}"
                )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("""import os

# Dizionario contenente la mappa dei file e il rispettivo codice
PROJECT_DATA = {
""")

        for path, content in project_files.items():
            out.write(f"    {repr(path)}: {repr(content)},\n\n")

        out.write("""}

def build_project():
    print("-------------------------------------")
    print(" Avvio ricostruzione del progetto ...")
    print("-------------------------------------")
    
    for filepath, content in PROJECT_DATA.items():
        # Recupera la cartella che deve contenere il file
        dirname = os.path.dirname(filepath)
        
        # Se la cartella non esiste (es: app/routers), la crea
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            print(f"[Cartella] Creata: {dirname}")
            
        # Scrive il file con il suo contenuto originale
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[File]     Scritto: {filepath}")

    print("------------------------------------------------")
    print(" Ricostruzione completata con successo!         ")
    print(" - python3 -m venv venv                         ")
    print(" - source venv/bin/activate                     ")
    print(" - pip install -r requirements.txt              ")
    print(" - python3 run.py                               ")
    print("------------------------------------------------")

if __name__ == "__main__":
    build_project()
""")

    print(
        f"\nFatto! Il super-script di installazione '{OUTPUT_FILE}' è stato generato."
    )


if __name__ == "__main__":
    generate_construction_script()
