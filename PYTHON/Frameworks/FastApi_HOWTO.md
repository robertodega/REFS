- installazione system wide

        - sudo apt install python3 fastapi
        - sudo apt install python3 uvicorn

- installazione in virtual environment ( consigliato )

        - python3 -m venv env
        - source env/bin/activate
        - pip3 install fastapi
        - pip3 install "uvicorn[standard]"

- creazione app

        - nano main.py


            from fastapi import FastAPI

            app = FastAPI()


            @app.get("/")
            async def root():
                return {"greeting": "Hello world"}

- uvicorn main:app --reload
