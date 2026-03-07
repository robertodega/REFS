#   filesystem construction
mkdir fastapi_course \
&& cd fastapi_course \
&& mkdir static templates static/css static/js static/img routers \
&& touch .env database.py config.py const.py static/css/bootstrap.css static/css/custom.css static/js/bootstrap.js static/js/jquery.js static/js/custom.js main.py routers/blog_get.py routers/blog_post.py templates/base.html templates/index.html

- nano static/css/bootstrap.css

        content from CSS bootstrap cdn link ( https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css )

- nano static/js/bootstrap.js

        content from JS ootstrap cdn link ( https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js )

- nano static/js/jquery.js

        content from JS jquery cdn link ( https://code.jquery.com/jquery-4.0.0.min.js )

- nano .env

        DB_USER=root
        DB_PASSWORD=
        DB_HOST=localhost
        DB_PORT=3306
        DB_NAME=utils

- nano config.php

        from pydantic_settings import BaseSettings, SettingsConfigDict

        class Settings(BaseSettings):
            DB_USER: str
            DB_PASSWORD: str
            DB_HOST: str
            DB_PORT: int
            DB_NAME: str

            @property
            def DATABASE_URL(self):
                return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

            model_config = SettingsConfigDict(env_file=".env")

        settings = Settings()

- nano database.py

        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        from config import settings

        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()

        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

- nano const.py

        website_title = "FastApi Course"
        rootpath = "./"

- nano main.py

        from fastapi import FastAPI, status, Response
        from enum import Enum
        from typing import Optional

        app = FastAPI()


        @app.get("/")
        async def root():
            return {"message": "fastapi Course"}


        @app.get("/hello")
        async def index():
            return {"message": "Hello World"}


        @app.post("/hello")
        async def index2():
            return {"message": "Hello World in POST"}


        #   position is important to prevent '/all' considered as failed int
        @app.get(
            "/blog/all",
            tags=["blog"],
            summary="Retrieve all blogs",
            description="This api call simulates fetching all blogs",
            response_description="List of available blogs",
        )
        def get_all_blocks():
            return {"message": "All blogs provided"}


        # Query parameters
        @app.get("/blog/allpages")
        def get_all_blogs_pages(page, page_size):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/blog/allpages?page=3&page_size=23


        @app.get("/blog/allpagesdefault")
        def get_all_blogs_pages(page=1, page_size=20):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/blog/allpagesdefault


        @app.get("/blog/allpagesdefaultoptional")
        def get_all_blogs_pages(page=1, page_size: Optional[int] = None):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/blog/allpagesdefaultoptional


        @app.get("/blog/{id}/comments/{comment_id}")
        def get_comment(
            id: int, comment_id: int, valid: bool = True, username: Optional[str] = None
        ):
            return {
                "message": f"blog_id {id}, comment {comment_id}, valid {valid}, username {username}"
            }
            # http://127.0.0.1:8000/blog/3/comments/2?valid=true&username=ciao


        # Predefined values for parameter
        class BlogType(str, Enum):
            short = "short"
            story = "story"
            howto = "howto"


        @app.get("/blog/type/{type}", tags=["blog"])
        def get_blog_type(type: BlogType):
            return {"message": f"Blog type {type}"}


        @app.get("/blog/{id}", tags=["blog"])
        def get_blog(id: int):  #   parameter validation
            return {"message": f"Blog with id {id}"}


        @app.get("/blog_with_statuscode/{id}", status_code=404)
        def get_blog(id: int):
            if id > 5:
                return {"error": f"Blog {id} not found"}
                # http://127.0.0.1:8000/blog_with_statuscode/6
            else:
                return {"message": f"Blog with id {id}"}
                # http://127.0.0.1:8000/blog_with_statuscode/3


        @app.get("/blog_with_statuscodepreset/{id}", status_code=status.HTTP_306_RESERVED)
        def get_blog(id: int):
            if id > 5:
                return {"error": f"Blog {id} reserved"}
                # http://127.0.0.1:8000/blog_with_statuscode/6
            else:
                return {"message": f"Blog with id {id}"}
                # http://127.0.0.1:8000/blog_with_statuscode/3


        @app.get("/blog_with_response/{id}", status_code=status.HTTP_404_NOT_FOUND)
        def get_blog(id: int, response: Response):
            if id > 5:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"error": f"Blog {id} not found"}
                # 'http://127.0.0.1:8000/blog_with_response/12
            else:
                response.status_code = status.HTTP_200_OK
                return {"message": f"Blog with id {id}"}
                # 'http://127.0.0.1:8000/blog_with_response/2


        @app.get("/blog_with_tags/{id}/comments/{comment_id}", tags=["blog", "comment"])
        def get_blog(id: int, response: Response):
            """
            Simulates blog comments list read

            - **id** mandatory query parameter
            - **comment_id** mandatory query parameter
            """
            return {"message": "All blogs provided with tags blog & comment"}
            # http://127.0.0.1:8000/blog_with_tags/3/comments/{comment_id}

- nano routers/blog_get.py

        from typing import Optional
        from fastapi import APIRouter, status, Response
        from enum import Enum

        router = APIRouter(prefix="/blog", tags=["blog"])


        #   position is important to prevent '/all' considered as failed int
        @router.get(
            "/all",
            summary="Retrieve all blogs",
            description="This api call simulates fetching all blogs",
            response_description="List of available blogs",
        )
        def get_all_blocks():
            return {"message": "All blogs provided"}


        # Query parameters
        @router.get("/allpages")
        def get_all_blogs_pages(page, page_size):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/allpages?page=3&page_size=23


        @router.get("/allpagesdefault")
        def get_all_blogs_pages(page=1, page_size=20):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/allpagesdefault


        @router.get("/allpagesdefaultoptional")
        def get_all_blogs_pages(page=1, page_size: Optional[int] = None):
            return {"message": f"All {page_size} blogs on page {page}"}
            # http://127.0.0.1:8000/allpagesdefaultoptional


        @router.get("/{id}/comments/{comment_id}")
        def get_comment(
            id: int, comment_id: int, valid: bool = True, username: Optional[str] = None
        ):
            return {
                "message": f"blog_id {id}, comment {comment_id}, valid {valid}, username {username}"
            }
            # http://127.0.0.1:8000/3/comments/2?valid=true&username=ciao


        # Predefined values for parameter
        class BlogType(str, Enum):
            short = "short"
            story = "story"
            howto = "howto"


        @router.get("/type/{type}")
        def get_blog_type(type: BlogType):
            return {"message": f"Blog type {type}"}


        @router.get("/{id}")
        def get_blog(id: int):  #   parameter validation
            return {"message": f"Blog with id {id}"}


        @router.get("_with_statuscode/{id}", status_code=404)
        def get_blog(id: int):
            if id > 5:
                return {"error": f"Blog {id} not found"}
                # http://127.0.0.1:8000_with_statuscode/6
            else:
                return {"message": f"Blog with id {id}"}
                # http://127.0.0.1:8000_with_statuscode/3


        @router.get("_with_statuscodepreset/{id}", status_code=status.HTTP_306_RESERVED)
        def get_blog(id: int):
            if id > 5:
                return {"error": f"Blog {id} reserved"}
                # http://127.0.0.1:8000_with_statuscode/6
            else:
                return {"message": f"Blog with id {id}"}
                # http://127.0.0.1:8000_with_statuscode/3


        @router.get("_with_response/{id}", status_code=status.HTTP_404_NOT_FOUND)
        def get_blog(id: int, response: Response):
            if id > 5:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"error": f"Blog {id} not found"}
                # 'http://127.0.0.1:8000_with_response/12
            else:
                response.status_code = status.HTTP_200_OK
                return {"message": f"Blog with id {id}"}
                # 'http://127.0.0.1:8000_with_response/2


        @router.get("_with_tags/{id}/comments/{comment_id}", tags=["comment"])
        def get_blog(id: int, response: Response):
            """
            Simulates blog comments list read

            - **id** mandatory query parameter
            - **comment_id** mandatory query parameter
            """
            return {"message": "All blogs provided with tags blog & comment"}
            # http://127.0.0.1:8000_with_tags/3/comments/{comment_id}

- mv main.py main_old.py

- nano main.py

        from fastapi import FastAPI
        from routers import blog_get
        from routers import blog_post

        app = FastAPI()
        app.include_router(blog_get.router)
        app.include_router(blog_post.router)


        @app.get("/")
        async def root():
            return {"message": "fastapi Course with routes"}


- nano routers/blog_post.py

        from fastapi import APIRouter

        router = APIRouter(prefix="/blog", tags=["blog"])


        @router.post("/new")
        def create_blog():
            pass

- nano templates/base.html

        <!DOCTYPE html>
        <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                <link rel="stylesheet" href="{{ url_for('static', path='css/bootstrap.css') }}">
                <script src="{{ url_for('static', path='js/jquery.js') }}"></script>
                <script src="{{ url_for('static', path='js/bootstrap.js') }}"></script>
                
                <link rel="stylesheet" href="{{ url_for('static', path='css/custom.css') }}">
                <script src="{{ url_for('static', path='js/custom.js') }}"></script>

                <title>{{ const.website_title }}</title>
            </head>

            <body>
                <div class="headerDiv">
                    <div class="headerBlockDiv">
                        <div class="headerTitleDiv" id="headerPathDiv">
                            <a href="./">{{ const.website_title }}</a>
                        </div>
                    </div>
                </div>
                <div class="contentDiv">
                    {% block content %} {% endblock %}
                </div>
            </body>
        </html>

- nano templates/index.html

        {% extends "base.html" %}

        {% block content %}
        <div class="content-container-div">
            This is the content of index.html
        </div>
        {% endblock %}

- nano static/css/custom.css

        body{
            background-color: antiquewhite;
            padding: 2%;

            .headerDiv{
                background-color: lightgrey;
                padding: 1%;
                text-align: center;
                font-weight: bold;
                font-size: 2rem;
            }

            .contentDiv{
                background-color: whitesmoke;
                padding: 1%;
                margin-top: 1%;
            }
        }

#   app run
- python3 -m venv fastapiCourse
- Windows:
    -   source fastapiCourse/Scripts/activate
- Linux:
    -   source fastapiCourse/bin/activate

- pip3 install fastapi uvicorn jinja2 requests python-multipart sqlalchemy pymysql pydantic-settings

- uvicorn main:app --reload

- http://127.0.0.1:8000             #   Main App
- http://127.0.0.1:8000/docs        #   Swagger interface

- cd .. && rm -rf dbManager && clear && ls -la
