- mkdir news-api
- cd news-api
- search api link from https://newsapi.org/

    -   Ex. https://newsapi.org/v2/everything?q=tesla&from=2026-01-10&sortBy=publishedAt&apiKey=API_KEY

- Login in https://newsapi.org/
- copy API key and use in main.py
- add extension 'JSON formatter' to Chrome

- nano main.py

        import requests
        import webbrowser
        import os

        os.system('clear')

        query = input("What kinf onews are you interested in today? ")
        api_key = "<API_KEY_FROM_newsapi.org>"

        url = f"https://newsapi.org/v2/everything?q={query}&from=2026-01-10&sortBy=publishedAt&apiKey={api_key}";   #   from https://newsapi.org/

        r = requests.get(url)
        data = r.json()
        articles = data["articles"]

        for index, article in enumerate(articles):
            print(index + 1)
            print(article["publishedAt"])
            print(article["title"])
            print(article["url"])
            print(article["description"])
            print("\n")

