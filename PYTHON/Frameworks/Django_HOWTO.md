- from https://docs.djangoproject.com/en/6.0/intro/tutorial01/

# Project dir creation
- mkdir mysite
- cd mysite
- mkdir djangotutorial
- django-admin startproject mysite djangotutorial
- cd djangotutorial
- python3 manage.py runserver

# Project App creation
- python3 manage.py startapp polls

# Project App customization
- nano polls/views.py

        from django.http import HttpResponse

        def index(request):
            return HttpResponse("Hello, world. You're at the polls index.")

- nano polls/urls.py

        from django.urls import path

        from . import views

        urlpatterns = [
            path("", views.index, name="index"),
        ]

# Project App inclusion
- nano mysite/urls.py

        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path("polls/", include("polls.urls")),
            path("admin/", admin.site.urls),
        ]

# DB setup
- python3 manage.py migrate

# Models creation ( database layout )
- nano polls/models.py

        from django.db import models

        class Question(models.Model):
            question_text = models.CharField(max_length=200)
            pub_date = models.DateTimeField("date published")


        class Choice(models.Model):
            question = models.ForeignKey(Question, on_delete=models.CASCADE)
            choice_text = models.CharField(max_length=200)
            votes = models.IntegerField(default=0)

- nano polls/app.py
    -   copy config class name

- nano mysite/settings.py
    -   in INSTALLED_APPS list paste APP (polls) config class name

            INSTALLED_APPS = [
                "polls.apps.PollsConfig",       // <= NEW CONFIG ADDED
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
            ] 

# store Model changes
- python3 manage.py makemigrations polls

# Model Table changes in DB
- python3 manage.py migrate

# Interactive Python Shell
- python3 manage.py shell

# Admin User
- python3 manage.py createsuperuser

# App managed by Admin
- nano polls/admin.py

        from django.contrib import admin

        from .models import Question

        admin.site.register(Question)

# Views management
- nano polls/views.py

        def detail(request, question_id):
            return HttpResponse("You're looking at question %s." % question_id)


        def results(request, question_id):
            response = "You're looking at the results of question %s."
            return HttpResponse(response % question_id)


        def vote(request, question_id):
            return HttpResponse("You're voting on question %s." % question_id)

# Views activation in urls
- nano polls/urls.py

        from django.urls import path

        from . import views

        urlpatterns = [
            path("", views.index, name="index"),
            
            path("<int:question_id>/", views.detail, name="detail"),
            path("<int:question_id>/results/", views.results, name="results"),
            path("<int:question_id>/vote/", views.vote, name="vote"),
        ]

# Update views with database API
- nano polls/views.py

        ...
        from .models import Question
        ...
        def index(request):
    
        #       return HttpResponse("Hello, world. You're at the polls index.")

        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        output = "<br />".join([q.question_text for q in latest_question_list])
        return HttpResponse(output)

# Design from Python separation ( templates usage )
- mkdir polls/templates polls/templates/polls
- nano polls/templates/polls/index.html

        <h1>Polls page</h1>
        {% if latest_question_list %}
            <ul>
            {% for question in latest_question_list %}
                <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No polls are available.</p>
        {% endif %}

# View update for template usage
- nano polls/views.py

        from django.shortcuts import render
        from django.http import HttpResponse
        from .models import Question
        from django.template import loader

        def index(request):
            latest_question_list = Question.objects.order_by("-pub_date")[:5]
            context = {"latest_question_list": latest_question_list}
            template = loader.get_template("polls/index.html")
            return HttpResponse(template.render(context, request))
        
        ...

# Djang0 Render shortcut
- nano polls/views.py

        from django.shortcuts import render
        from django.http import HttpResponse
        from .models import Question
        #   from django.template import loader

        def index(request):
            latest_question_list = Question.objects.order_by("-pub_date")[:5]
            context = {"latest_question_list": latest_question_list}
            #   template = loader.get_template("polls/index.html")
            #   return HttpResponse(template.render(context, request))
            return render(request, "polls/index.html", context)
            
        ...

# Error page management
- nano polls/templates/polls/detail.html

        {{ question }}

- nano polls/views.py

        from django.http import Http404
        
        ...

        def detail(request, question_id):
            #   return HttpResponse("You're looking at question %s." % question_id)
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                raise Http404("Question does not exist")
            return render(request, "polls/detail.html", {"question": question})

- Error Raise shortcut
    -   nano polls/views.py

            from django.shortcuts import get_object_or_404, render
            ...
            def detail(request, question_id):
                #   try:
                #       question = Question.objects.get(pk=question_id)
                #   except Question.DoesNotExist:
                #       raise Http404("Question does not exist")
                #   return render(request, "polls/detail.html", {"question": question})
                question = get_object_or_404(Question, pk=question_id)
                return render(request, "polls/detail.html", {"question": question})

    - nano polls/templates/polls/detail.html

            <h1>{{ question.question_text }}</h1>
            <ul>
            {% for choice in question.choice_set.all %}
                <li>{{ choice.choice_text }}</li>
            {% endfor %}
            </ul>

# name param use from APP urls.py
- nano polls/templates/polls/index.html

        <h1>Polls page</h1>
        {% if latest_question_list %}
        <ul>
            {% for question in latest_question_list %}
            <!--<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>-->
            <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No polls are available.</p>
        {% endif %}

- nano polls/templates/polls/detail.html 

        <hr /><a href="{% url 'index' %}">Home</a><hr />
        <h1>{{ question.question_text }}</h1>
        <ul>
        {% for choice in question.choice_set.all %}
            <li>{{ choice.choice_text }}</li>
        {% endfor %}
        </ul>

- nano polls/urls.py

        possibility to change entire path for all templates which use it in one operation:

        ...
        #   path("<int:question_id>/", views.detail, name="detail"),
        path("specifics/<int:question_id>/", views.detail, name="detail"),
        ...
    
# Namespaces
- APP organization in namespaces for projects with many apps
    - nano polls/urls.py

            from django.urls import path

            from . import views

            app_name = "polls"
            urlpatterns = [
                path("", views.index, name="index"),
                path("<int:question_id>/", views.detail, name="detail"),
                path("<int:question_id>/results/", views.results, name="results"),
                path("<int:question_id>/vote/", views.vote, name="vote"),
            ]

    - nano polls/templates/polls/index.html

            ...
            <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
            ...

    - nano polls/templates/polls/detail.html

            <hr /><a href="{% url 'polls:index' %}">Home</a><hr />
            ...

# Form usage
- nano polls/templates/polls/detail.html

        <hr /><a href="{% url 'polls:index' %}">Home</a>
        <form action="{% url 'polls:vote' question.id %}" method="post">
            {% csrf_token %}
            <fieldset>
                <legend>
                    <h1>{{ question.question_text }}</h1>
                </legend>
                {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
                {% for choice in question.choice_set.all %}
                <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
                <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
                {% endfor %}
            </fieldset>
            <input type="submit" value="Vote">
        </form>

    # Static style
    - mkdir polls/static/polls
    - nano polls/static/polls/style.css
        -   ...
    - nano polls/templates/polls/index.html

            {% load static %}

            <link rel="stylesheet" href="{% static 'polls/style.css' %}">
            ...

