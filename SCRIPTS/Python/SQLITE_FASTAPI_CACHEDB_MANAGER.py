import sqlite3
import os
import subprocess

introMmsg = "\n\n\t============================== fastapi Sqlite management script ==============================\n\n"
choiceMmsg = "\n\n\tSelect Action:\n\n\t1: Drop\n\t2: Truncate\n\t0: Exit\n\n\t"
exitMsg = "\n\n\t========================================= Thank you! =========================================\n\n"
canProceed = False


# def clear_screen():
#     os.system("cls" if os.name == "nt" else "clear")


def clear_screen():
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "cls"], check=False)
    else:
        subprocess.run(["clear"], check=False)


while True:
    clear_screen()

    action = (
        input(f"{introMmsg}{choiceMmsg}")
        .strip()
        .lower()
    )

    if action in ("1", "2", "0"):

        if action == "1":
            commandName = "DROP"
            commandValue = "DROP TABLE IF EXISTS"
            actionEffect = "DROPPED"
        elif action == "2":
            commandName = "TRUNCATE"
            commandValue = "DELETE FROM"
            actionEffect = "TRUNCATED"
        elif action == "0":
            print(exitMsg)
            exit(0)
        else:
            print("Action is not valid")
            exit(1)

        if action != "0":

            conn = sqlite3.connect("C:/xampp/htdocs/PROJECTS/APPS/fastapi/cache.db")
            cur = conn.cursor()

            tables = [
                r[0]
                for r in cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            ]

            print(
                f"\nSelect Table Name to {commandName}:\n\n\t\n\n\tAvailable tables are:\n\n"
            )
            for t in tables:
                print(f"\t\t{t}\n")

            tableName = input(f"\nTable Name:\n\n\t").strip().upper()

            for t in tables:
                if t == tableName:
                    canProceed = True
                    break

            if canProceed:
                print(f"\n\n\t\t> {commandValue} {tableName} ... ", end="")
                cur.execute(f'{commandValue} "{t}"')
                print(f"DONE")

                if action == "2":
                    try:
                        print(f"\n\n\t\t> Deleting from sqlite_sequence ... ", end="")
                        cur.execute("DELETE FROM sqlite_sequence")
                        print(f"DONE")
                    except sqlite3.OperationalError:
                        pass

                conn.commit()
                conn.close()

                print(f"\n\n\tTable {tableName} has been {actionEffect}\n\n")
            else:
                print(f"\n\n\n\tTable {tableName} is not a valid table name\n\n")

        break

print(exitMsg)
