- Docker management commands

        sudo systemctl status docker
        sudo systemctl start docker
        sudo systemctl restart docker

- Project Creation

        mkdir <PATH_TO_APP>/<PROJECT_NAME>
        cd <PATH_TO_APP>/<PROJECT_NAME>
        python3 -m venv venv

- Project activation

        source venv/bin/activate
        touch app.py requirements.txt Dockerfile docker-compose.yml

    - nano app.py
    
                from flask import Flask

                app = Flask(__name__)

                @app.route("/")
                def home():
                return "Docker container is running!"

                if __name__ == "__main__":
                app.run(host="0.0.0.0", port=8080)

    - nano requirements.txt

                flask==2.3.2

    - nano docker-compose.yml                                                           #   per utilizzo di database

                version: "3.9"
                services:
                app:
                build:
                context: .
                ports:
                - "8080:8080"
                volumes:
                - .:/app


- Dockerfile constrution

        FROM python:3.9-slim                                                            #   Base Image
        WORKDIR /app                                                                    #   work directory set in container
        COPY requirements.txt .                                                         #   requirements file copy
        COPY . /app                                                                     #   App code copy
        RUN pip install --no-cache-dir -r requirements.txt mysql-connector-python       #   dependences installation
        EXPOSE 8080                                                                     #   port expose
        CMD ["python", "app.py"]                                                        #   container start command

- Docker Image creation

        docker build -t <PROJECT_NAME> .

- Docker Image save

        docker tag <PROJECT_NAME> <USERNAME>/<PROJECT_NAME>

- Docker Image upload

        docker push <USERNAME>/<PROJECT_NAME>

- Container Run

        docker run -d -p 8080:8080 <PROJECT_NAME>
        docker-compose up                                       #   if using Docker Compose

- Check

        docker exec -it <PROJECT_NAME> bash                     #   container access
        docker ps                                               #   Container in execution
        docker logs <CONTAINER_NAME>                            #   project output (debugging)
        docker stop <CONTAINER_NAME>                            #   Stops the container.
        http://localhost:8080                                   #   Application access

- Docker null containers/images removal
        docker container prune    # <none> container
        docker image prune        # <none> images
        docker image prune -a     # unused images