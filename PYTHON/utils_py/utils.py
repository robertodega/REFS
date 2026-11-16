#   ----------------------------------------------------------------------------------------------
#   create mysql table utils
#   python3 -m venv .venv
#   source .venv/bin activate
#   python3 -m pip install mysql-connector-python
#   python3 utils.py
#   ----------------------------------------------------------------------------------------------

from functions import env_warm_up

if __name__ == "__main__":

    env_warm_up()

    from functions import (
        get_db_connection,
        header_print,
        search_term,
        footer_print,
    )

    conn = get_db_connection()

    header_print()
    search_term(conn)
    footer_print()
