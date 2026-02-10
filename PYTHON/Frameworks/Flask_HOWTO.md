
# project creation

- mkdir <PROJ_NAME>
- cd <PROJ_NAME>
- mkdir DB templates static static/js static/css static/img static/docs
- touch DB/db_init.sql app.py config.py const.py parameters.py static/js/custom.js static/js/bootstrap.js static/js/jquery.js static/css/custom.css static/css/bootstrap.css templates/index.html

    -   ( copiare bootstrap.css, bootstrap.js e jquery.js dal relativo file online )

# virtual env set

- sudo apt install python3.13-venv
- python3 -m venv venv
- source venv/bin/activate
- pip install flask mysql-connector-python

# project files customization

- nano const.py

        db_const = {
            "localhost": {"host": "localhost", "dbname": "<PROJ_NAME>", "user": "root", "pwd": ""},
            "remote": {"host": "", "dbname": "", "user": "", "pwd": ""},
        }

        website_title = "<PROJ_NAME>"
        table_name = "<TABLE_NAME>"
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

        def get_search_ref():
            return request.args.get("s", "")

# App creation

- nano app.py

        from flask import Flask, render_template, request
        from config import get_db_connection
        import const
        from parameters import get_search_ref

        app = Flask(__name__)


        @app.route("/")
        def index():

            host = request.host.split(":", 1)[0]
            env = "remote" if host != "localhost" else host
            conn = get_db_connection(env)

            search_ref = get_search_ref()
            results = ''

            if conn:
                if search_ref:
                    try:
                        if search_ref != "all":
                            cursor = conn.cursor()
                            cursor.execute(
                                "SELECT * FROM {} WHERE subject LIKE %s OR username LIKE %s OR note LIKE %s".format(
                                    const.table_name
                                ),
                                ("%" + search_ref + "%", "%" + search_ref + "%", "%" + search_ref + "%")
                            )
                            results = cursor.fetchall()
                            cursor.close()
                        else:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM {}".format(const.utils_table_name))
                            results = cursor.fetchall()
                            cursor.close()
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

            <div class="utils-form-div" id="search-form-div">
                <form action="{{ rootpath }}" method="get" id="search-form">
                    <input type="text" name="s" id="search-input" class="utils-input" placeholder="Enter search term"
                        value="{{ search_ref }}">
                    <input type="submit" value="Search" id="search-submit" class="utils-button">
                </form>
            </div>

            <div class="result-div" id="result-div">
                {% if results %}
                    <h3>Search Results:</h3>

                    <table class='table table-striped table-bordered'>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Subject</th>
                                <th>Username</th>
                                <th>Password</th>
                                <th>Note</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for result in results %}
                            <tr>
                                <td>{{ result[0] }}</td>
                                <td>{{ result[1] }}</td>
                                <td>{{ result[2] }}</td>
                                <td>{{ result[3] }}</td>
                                <td>{{ result[4] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>

                {% else %}
                    <h3>No results found.</h3>
                {% endif %}
            </div>
        </body>

        </html>

# project execution

[ from App root ]

- python3 app.py