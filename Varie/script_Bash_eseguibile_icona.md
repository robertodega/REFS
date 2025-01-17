    -   Creare lo script che si vuole eseguire
        -   es. <SCRIPT_PATH>/<SCRIPT_NAME>.sh

    -   Creare l'icona per lo script
        -   es. <SCRIPT_PATH>/<SCRIPT_ICON>.png

    -   Creare un file <EXEC_SCRIPT_PATH><FILENAME>.desktop: 
            -   <EXEC_SCRIPT_PATH> può essere
            -   una directory come ~/.local/share/applications/ se lo script deve essere disponibile solo per il singolo utente
            -   oppure /usr/share/applications/ per renderlo disponibile a tutti gli utenti

    -   modifica il file appena creato con le seguenti righe:

    -       Version=1.0
    -       Type=Application
    -       Name=NomeDelLauncher
    -       Comment=Descrizione del comando
    -       Exec=<SCRIPT_PATH>/<SCRIPT_NAME>.sh
    -       Icon=<SCRIPT_PATH>/<SCRIPT_ICON>.png
    -       Terminal=true
    -       Categories=Utility;

    -   Salvare e rendere eseguibile il file con estensione .desktop:
        -   chmod +x <EXEC_SCRIPT_PATH><FILENAME>.desktop
