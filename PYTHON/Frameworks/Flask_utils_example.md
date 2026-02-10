
# project creation

- mkdir utils
- cd utils
- mkdir DB templates static static/js static/css static/img static/docs
- touch DB/utils_init.sql DB/utils.sql app.py config.py const.py parameters.py static/js/custom.js static/js/bootstrap.js static/js/jquery.js static/css/custom.css static/css/bootstrap.css templates/index.html templates/insert.html

    -   ( copiare bootstrap.css, bootstrap.js e jquery.js dal relativo file online )

# virtual env set

- sudo apt install python3.13-venv
- python3 -m venv venv
- source venv/bin/activate
- pip install flask mysql-connector-python

# project files customization

- nano DB/utils_init.sql

        -- phpMyAdmin SQL Dump
        -- version 5.2.1
        -- https://www.phpmyadmin.net/
        --
        -- Host: localhost
        -- Creato il: Gen 09, 2026 alle 08:58
        -- Versione del server: 10.4.28-MariaDB
        -- Versione PHP: 8.2.4

        SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
        START TRANSACTION;
        SET time_zone = "+00:00";


        /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
        /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
        /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
        /*!40101 SET NAMES utf8mb4 */;

        --
        -- Database: `utils`
        --

        -- --------------------------------------------------------

        --
        -- Struttura della tabella `utils`
        --

        DROP TABLE IF EXISTS `utils`;
        CREATE TABLE `utils` (
        `id` int(11) NOT NULL,
        `subject` varchar(50) NOT NULL,
        `username` varchar(100) NOT NULL,
        `password` varchar(100) NOT NULL,
        `note` text DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

        --
        -- Indici per le tabelle scaricate
        --

        --
        -- Indici per le tabelle `utils`
        --
        ALTER TABLE `utils`
        ADD PRIMARY KEY (`id`),
        ADD UNIQUE KEY `subject` (`subject`,`username`);

        --
        -- AUTO_INCREMENT per le tabelle scaricate
        --

        --
        -- AUTO_INCREMENT per la tabella `utils`
        --
        ALTER TABLE `utils`
        MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
        COMMIT;

        /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
        /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
        /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


- nano const.py

        db_const = {
            "localhost": {"host": "localhost", "dbname": "utils", "user": "root", "pwd": ""},
            "remote": {"host": "", "dbname": "", "user": "", "pwd": ""},
        }

        website_title = "utils"
        utils_table_name = "utils"
        rootpath = "./"



- nano config.py

        import mysql.connector
        from const import db_const

        def get_db_connection(env):
            cfg = db_const.get(env, {}) or {}
            if not cfg.get("dbname"):
                cfg = db_const.get("localhost")
            return mysql.connector.connect(
                host=cfg["host"],
                user=cfg["user"],
                password=cfg["pwd"],
                database=cfg["dbname"],
            )

- nano parameters.py

        from flask import request

        from config import get_db_connection


        def get_conn():
            host = request.host.split(":", 1)[0]
            env = "remote" if host != "localhost" else host
            return get_db_connection(env)


        def get_search_ref():
            return request.args.get("s", "")


        def search_db_ref(table_name, search_value):
            conn = get_conn()
            result = ""

            if conn:
                if search_value != "all":
                    q = (
                        "SELECT * FROM {} WHERE subject LIKE %s OR username LIKE %s OR note LIKE %s ORDER BY id DESC".format(
                            table_name
                        ),
                        (
                            "%" + search_value + "%",
                            "%" + search_value + "%",
                            "%" + search_value + "%",
                        ),
                    )
                else:
                    q = ("SELECT * FROM {} ORDER BY id DESC".format(table_name),)

                cursor = conn.cursor()
                cursor.execute(*q)
                result = cursor.fetchall()
                cursor.close()
                conn.close()

            return result


        def get_duplicate_check_query(table_name, subject_value, username_value):
            result = False

            subject_presence = search_db_ref(table_name, subject_value)

            if(subject_presence):
                for entry in subject_presence:
                    if(username_value == entry[2]):
                        result = True
                        break

            return result


        def get_insert_data():
            return {
                "insert-new-form": request.form.get("insert-new-form", ""),
                "subject": request.form.get("subject_field", ""),
                "username": request.form.get("username_field", ""),
                "password": request.form.get("password_field", ""),
                "note": request.form.get("note_field", ""),
            }


        def insert_db_ref(table_name, insert_data):
            conn = get_conn()
            results = ""
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO {} (subject, username, password, note) VALUES (%s, %s, %s, %s)".format(
                            table_name
                        ),
                        (
                            insert_data["subject"],
                            insert_data["username"],
                            insert_data["password"],
                            insert_data["note"],
                        ),
                    )
                    conn.commit()
                    cursor.close()
                    results = "New data has been successfully inserted into the database."
                except Exception as e:
                    results += (
                        " Failed to insert data for subject'{}', username '{}' ( {} ).".format(
                            insert_data["subject"], insert_data["username"], e
                        )
                    )
                finally:
                    conn.close()
            else:
                results = "Error in database connection operation for insertion task"
            return results


        # def get_delete_data():
        #     return {"delete-id": request.form.get("delete-id", "")}


        # def get_update_data():
        #     return {
        #         "update-id": request.form.get("update-id", ""),
        #         "subject": request.form.get("subject_field", ""),
        #         "username": request.form.get("username_field", ""),
        #         "password": request.form.get("password_field", ""),
        #         "note": request.form.get("note_field", ""),
        #     }


# App creation

- nano app.py

        from flask import Flask, render_template, request

        # from config import get_db_connection
        import const
        from parameters import (
            get_conn,
            get_search_ref,
            search_db_ref,
            get_insert_data,
            insert_db_ref,
            get_duplicate_check_query,
        )

        app = Flask(__name__)


        @app.route("/")
        def index():

            conn = get_conn()
            search_ref = get_search_ref()
            results = ""

            if conn:
                if search_ref:
                    try:
                        results = search_db_ref(const.utils_table_name, search_ref)
                    except Exception as e:
                        results = {"Database query error: {}".format(e)}
                    finally:
                        conn.close()
            else:
                results = {"Error in database reading operation"}

            return render_template(
                "index.html",
                search_ref=search_ref,
                results=results,
            )


        @app.route("/insert", methods=["GET", "POST"])
        def insert():

            insert_data = get_insert_data()
            results = ""

            if insert_data["insert-new-form"]:

                conn = get_conn()

                if conn:
                    try:
                        # Check for duplicates before insertion
                        check_db_presence = get_duplicate_check_query(
                            const.utils_table_name,
                            insert_data["subject"],
                            insert_data["username"],
                        )
                        if check_db_presence:
                            results = (
                                "Duplicate entry for subject '{}' with username '{}'.".format(
                                    insert_data["subject"], insert_data["username"]
                                )
                            )
                            return render_template(
                                "insert.html",
                                insert_data=insert_data,
                                results=results,
                            )

                        # No duplicates found, proceed with insertion
                        results = insert_db_ref(const.utils_table_name, insert_data)

                    except Exception as e:
                        results = " Failed to insert data for subject'{}', username '{}' ( {} ).".format(
                            insert_data["subject"], insert_data["username"], e
                        )
                    finally:
                        conn.close()
                else:
                    results = "Error in database connection operation for insertion task"

            return render_template(
                "insert.html",
                insert_data=insert_data,
                results=results,
            )


        if __name__ == "__main__":
            app.run(debug=True)


- nano templates/index.html

        <!DOCTYPE html>
        <html lang="en">

        <head>
            <title>{{ website_title }}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <script src="{{ url_for('static', filename='js/jquery.js') }}"></script>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
            <script src="{{ url_for('static', filename='js/bootstrap.js') }}"></script>

            <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='img/favicon.ico') }}">
            <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
        </head>

        <body>
            <div class="headerDiv">
                <div class="headerBlockDiv">
                    <div class="headerTitleDiv" id="headerPathDiv">
                        <h2><a href='{{ rootpath }}'>{{ website_title }}</a></h2>
                    </div>
                </div>
            </div>

            <div class="form-div">
                <div class="utils-form-div" id="search-form-div">
                    <form action="{{ rootpath }}" method="get" id="search-form">
                        <input type="text" name="s" id="search-input" class="utils-input" placeholder="Enter search term"
                            value="{{ search_ref }}">
                        <input type="submit" value="Search" id="search-submit" class="utils-button">
                        <input type="submit" value="Reset" id="search-reset" name="search-reset" class="utils-button">
                        <input type="button" value="New" id="insert-new" name="insert-new" class="utils-button">
                    </form>
                </div>

                <div class="value-div" id="search-value-div">
                    <span class="evidence">{{ results|length }}</span> results found
                    {% if search_ref %}with keyword "<span class="evidence">{{ search_ref }}</span>"{% endif %}
                </div>
            </div>

            <div class="result-div" id="result-div">
                {% if results %}
                <table class='table table-striped table-bordered results-table-labels'>
                    <thead>
                        <tr>
                            <th class="table_cell table_head_title">Subject</th>
                            <th class="table_cell table_head_title">Username</th>
                            <th class="table_cell table_head_title">Password</th>
                            <th class="table_cell table_head_title">Note</th>
                        </tr>
                    </thead>
                </table>
                <div class="results-table-div" id="results-table-body-div">
                    <table class='table table-striped table-bordered results-table-body'>
                        <tbody>
                            {% for result in results %}
                            <tr>
                                <!-- <td class="table_cell delete_cell">
                                    <div class="td_item td_item_del">delete</div>
                                    <div class="td_item">{{ result[1] }}</div>
                                </td> -->
                                <td class="table_cell table_value">{{ result[1] }}</td>
                                <td class="table_cell table_value">{{ result[2] }}</td>
                                <td class="table_cell table_value">{{ result[3] }}</td>
                                <td class="table_cell table_value">{{ result[4] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
            </div>
        </body>

        </html>

        <script src="{{ url_for('static', filename='js/custom.js') }}"></script>

- nano templates/insert.html

        <!DOCTYPE html>
        <html lang="en">

        <head>
            <title>{{ website_title }}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <script src="{{ url_for('static', filename='js/jquery.js') }}"></script>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
            <script src="{{ url_for('static', filename='js/bootstrap.js') }}"></script>

            <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='img/favicon.ico') }}">
            <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
        </head>

        <body>
            <div class="headerDiv">
                <div class="headerBlockDiv">
                    <div class="headerTitleDiv" id="headerPathDiv">
                        <h2><a href='{{ rootpath }}'>{{ website_title }}</a></h2>
                    </div>
                </div>
            </div>

            <div class="form-div">

                <div class="utils-form-div" id="search-form-div">
                    <form action="{{ rootpath }}/insert" method="post" id="search-form">
                        <input type="hidden" name="insert-new-form" value="true">
                        <input type="text" name="subject_field" id="subject_field" class="utils-input"
                            placeholder="Enter subject value" value="" required>
                        <input type="text" name="username_field" id="username_field" class="utils-input"
                            placeholder="Enter username value" value="" required>
                        <input type="text" name="password_field" id="password_field" class="utils-input"
                            placeholder="Enter password value" value="" required>
                        <input type="text" name="note_field" id="note_field" class="utils-input" placeholder="Enter note value"
                            value="">
                        <input type="submit" value="Insert" id="insert-new-btn" class="utils-button">
                        <input type="button" value="Home" id="HomeBtn" class="utils-button">
                    </form>
                </div>

            </div>

            {% if insert_data["insert-new-form"] %}
            <div class="result-div" id="result-div">
                <table class='table table-striped table-bordered results-table-body'>
                    <thead>
                        <tr>
                            <th class="table_cell table_head_title">Subject</th>
                            <th class="table_cell table_head_title">Username</th>
                            <th class="table_cell table_head_title">Password</th>
                            <th class="table_cell table_head_title">Note</th>
                        </tr>
                    </thead>
                    <tr>
                        <td class="table_cell">{{ insert_data.subject }}</td>
                        <td class="table_cell">{{ insert_data.username }}</td>
                        <td class="table_cell">{{ insert_data.password }}</td>
                        <td class="table_cell">{{ insert_data.note }}</td>
                    </tr>
                </table>
            </div>

            <table class='table table-striped table-bordered results-table-body'>
                <tbody>
                    <tr>
                        <td class="table_cell">{{ results }}</td>
                    </tr>
                </tbody>
            </table>
            {% endif %}
            
        </body>

        </html>

        <script src="{{ url_for('static', filename='js/custom.js') }}"></script>

-   nano static/js/custom.js

        $('#search-reset').on('click', function() {
            $('#search-input').val('');
        });

        $('#insert-new').on('click', function() {
            window.location.href = '/insert';
        });

        $('#HomeBtn').on('click', function() {
            window.location.href = '/';
        });

-   nano static/js/custom.css

        .table_cell {
          text-align: center;
          width: 20%;
        
          &.table_value {
            text-align: left;
            padding-left: 30px;
          }
        
          /* &.delete_cell {
            width: 500px;
            display: flex;
            gap: 20px;
        
            .td_item {
              border: 1px solid #ccc;
            }
        
            .td_item_del{
              font-weight: bold;
              cursor: pointer;
              color: red;
            }
          } */
        
        }
        
        .evidence {
          font-weight: bold;
          color: #2a9d8f;
        }
        
        .form-div {
          display: flex;
          gap: 20px;
          padding: 1%;
        
          #search-value-div {
            border: 0px solid red;
            font-weight: normal;
          }
        }
        
        #result-div {
          .results-table-labels {
            .table_cell {
              font-weight: bold;
              background-color: #f2f2f2;
            }
          }
          .results-table-div {
            height: 700px;
            overflow: auto;
          }
        }

# project execution

[ from App root ]

- python3 ./app.py