
$ mkdir folderName

$ cd folderName

$ python3 -m venv venv

$ source venv/bin/activate

$ python3 -m pip install --upgrade pip setuptools

$ pip install flask

$ pip freeze > requirements.txt

$ nano <file_name>.py

    from flask import Flask

    app = Flask(__name__)

    @app.route('/')

    def index():
        return"<h1>Home Page</h1>"

$ flask run

############ templates usage ############

$ mkdir templates

$ touch templates/index.html

    def index():
        return render_template('index.html')









