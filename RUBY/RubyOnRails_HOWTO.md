
-- ------------------------- Dev Environment installation -----------------------------------------

- sudo gem install rails
- sudo apt-get install -y build-essential libyaml-dev
- sudo gem install bundler
- sudo gem install psych -v '5.2.3'
- sudo apt-get update
- sudo apt-get install -y build-essential libmariadb-dev
- sudo gem install mysql2 -v '0.5.6'
- rails -v

-- ------------------------- project creation -----------------------------------------------------

- rails new <PROJ_NAME> -d mysql
- cd <PROJ_NAME>
- bin/rails db:create

-- Model Generation -------------------------------------------------------------------------------

- rails generate model <MODEL_NAME> name:string email:string

    [ /app/models/<MODEL_NAME>.rb ( es. Usermanager ) ]

- rails db:migrate

MySQL check:

- roby@roby:/opt/lampp/htdocs/WWW/PROJECTS/Ruby/db_manager$ rails dbconsole
- SHOW TABLES;

-- Controller Generation --------------------------------------------------------------------------

- rails generate scaffold_controller Usermanager name:string email:string

    [ /app/controllers/usermanagers_controller.rb ]
    views will be automatically generated

in /config/routes.rb, insert model route:

- root 'usermanagers#index'

    at start, points to [ /app/views/usermanagers/index.html.erb ]


CSS File:

    /app/assets/stylesheets/application.css

JSFile: 

    /app/javascript/application.js




-- ------------------------- project run ----------------------------------------------------------

- rails server


