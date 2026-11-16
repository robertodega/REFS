import os
import sys
import subprocess
from pathlib import Path

from const import (
    utils_tbl,
    db_user,
    db_pwd,
    header_txt,
    welcomeLabel,
    footer_txt,
    searchTermLabel,
)


def clear_screen():
    if os.name == "nt":
        subprocess.run("cls", shell=True, check=False)
    else:
        subprocess.run(["clear"], check=False)


def env_warm_up():

    venv_dir = Path(".venv").resolve()
    venv_python = venv_dir / "bin" / "python"

    # ----------------------------
    # Virtual Environment Creation
    # ----------------------------
    if not venv_dir.exists():
        print("Virtual Environment Creation ...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    # ----------------------------

    # ------------------------
    # MySQL installation check
    # ------------------------
    check_mysql = subprocess.run(
        [str(venv_python), "-c", "import mysql.connector"], capture_output=True
    )
    if check_mysql.returncode != 0:
        print("Installazione mysql-connector-python...")
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "mysql-connector-python"],
            check=True,
        )
    # ------------------------

    # -------------------------
    # Virtual Environment Start
    # -------------------------
    if sys.prefix != sys.base_prefix:
        return

    print("Virtual Environment Start ...")
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    # -------------------------


def get_db_connection():
    import mysql.connector

    conn = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_pwd,
        database=utils_tbl,
    )

    return conn


def header_print():
    clear_screen()
    print(f"{header_txt}")
    print(f"{welcomeLabel}")


def footer_print():
    print(f"{footer_txt}")


def search_term(conn):
    while (searched_term := input(searchTermLabel)) != "0":
        search_result = search_db(conn, searched_term)
        result_print(searched_term, search_result)


def search_db(conn, searched_term):
    cursor = conn.cursor(dictionary=True)
    qBody = f"SELECT * FROM {utils_tbl} WHERE 1=1"
    if searched_term != "":
        qBody += " AND Subject LIKE %s"
    params = (f"%{searched_term}%",) if searched_term != "" else ()
    cursor.execute(qBody, params)
    search_result = cursor.fetchall()
    cursor.close()

    return search_result


def result_print(searched_term, search_result):

    clear_screen()

    if not search_result:
        print(f"\n\tNo match foud for term '{searched_term}'\n")
        return

    for row in search_result:
        print("-" * 50)

        for key, value in row.items():
            print(f"{key}: {value}")
