- search api link from https://newsapi.org/
- Login in https://newsapi.org/
- copy API key and use in main.py
- add extension 'JSON formatter' to Chrome

- python3 -m venv newsfeed
- source newsfeed/bin/activate
- pip3 install fastapi
- pip3 install uvicorn
- pip3 install requests
- cd newsfeed
- nano main.py

        from fastapi import FastAPI
        import requests
                
        app = FastAPI()


        @app.get("/")
        async def root():
            
            query = input("What kinf onews are you interested in today? ")
            api_key = "<API_KEY_FROM_newsapi.org>"

            url = f"https://newsapi.org/v2/everything?q={query}&from=2026-01-10&sortBy=publishedAt&apiKey={api_key}";   #   from https://newsapi.org/

            r = requests.get(url)
            
            # data = r.json()
            # articles = data["articles"]

            # for index, article in enumerate(articles):
            #     print(index + 1)
            #     print(article["publishedAt"])
            #     print(article["title"])
            #     print(article["url"])
            #     print(article["description"])
            #     print("\n")
                
            return r

- uvicorn main:app --reload
