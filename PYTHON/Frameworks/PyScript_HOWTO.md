- mkdir <PROJECT_NAME>
- cd <PROJECT_NAME>
- mkdir css js inc assets assets/img
- touch index.html const.py inc/app.py css/custom.css js/custom.js
- nano index.html

        <!doctype html>
        <html lang="it">

        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width,initial-scale=1" />
            <title>APP TITLE</title>
            
            <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
            <script defer src="https://pyscript.net/latest/pyscript.js"></script>

            <!-- Richiesta pacchetti Python da installare -->
            <py-config>
                <!-- packages = ["numpy", "matplotlib"] -->
            </py-config>

            <link rel="stylesheet" href="css/styles.css" />
        </head>

        <body>
            <main>
                <h1>PROJECT NAME</h1>

                <section class="presentation">
                    <h2>Welcome!</h2>
                    <p>APP PYSCRIPT</p>
                </section>

                <footer>
                    <p>Esempio APP sviluppata con PyScript</p>
                </footer>
            </main>

            <py-script src="inc/app.py"></py-script>

        </body>

        </html>

- open index.html from local server or from browser with

        python3 -m http.server 8000
        open http://localhost:8000


