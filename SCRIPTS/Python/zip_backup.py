#!/usr/bin/env python3

import os
import zipfile
import shutil
from datetime import datetime


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def folder_search():
    return sorted(
        # [d for d in os.listdir("..") if os.path.isdir(f"../{d}") and d.upper() not in ("BACKUP", "SCRIPTS", "APP_MANAGER")]
        [d for d in os.listdir(".") if os.path.isdir(f"{d}")]
    )

def backup_creation(folder_path, comment):
    data = datetime.now().strftime("%Y_%m_%d_%H_%M")

    comment = comment.strip().replace(" ", "_")
    if not comment:
        comment = "backup"

    backup_dir = "BACKUP"
    os.makedirs(backup_dir, exist_ok=True)

    zip_name = f"{data}_{folder_path}_{comment}.zip"
    zip_path = os.path.join(backup_dir, zip_name)

    folder_path_app = (
        folder_path
        if os.path.isabs(folder_path)
        else os.path.join(os.getcwd(), folder_path)
    )

    print(f"\nCreating backup for folder: {folder_path_app}\n")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path_app):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path_app))
                zipf.write(file_path, arcname)

                print(".", end="", flush=True)

    print("\nBackup has been completed.")
    print(f"File has been created: {os.path.abspath(zip_path)}")


def main():
    folders = folder_search()
    if not folders:
        print("No folder available.")
        return

    while True:
        try:
            clear_screen()
            print("=== ZIP BACKUP CREATION ===\n")
            print(f"\n\n\tCurrent folder: {os.getcwd()}\n")
            print("Available folders:\n")
            for i, fold in enumerate(folders, start=1):
                print(f"{i}. {fold}")
            choice = int(
                input(
                    f"\nSelect folder number between 1 and {len(folders)} ( type 0 to exit ): "
                )
            )
            if 0 <= choice <= len(folders):
                break
        except ValueError:
            print("Insert a folder number.")

    if choice == 0:
        clear_screen()
        print(
            "\n\n\t============================ Thank you, bye bye. ============================\n\n"
        )
    else:
        folder = folders[choice - 1]
        comment = input("Backup comment: ")
        backup_creation(folder, comment)

if __name__ == "__main__":
    main()
