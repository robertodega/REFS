        -   composer create-project laravel/laravel <LARAVEL_PROJECT_NAME>
        -   cd <LARAVEL_PROJECT_NAME>
        -   in /opt/lampp/htdocs/WWW/PROJECTS/PHP/Laravel/<LARAVEL_PROJECT_NAME>/.env

                DB_CONNECTION=mysql
                DB_HOST=127.0.0.1
                DB_PORT=3306
                DB_DATABASE=LARAVEL_DB_NAME
                DB_USERNAME=root
                DB_PASSWORD=

        -   php artisan migrate

                WARN  The database 'bianchifalegnameria_Laravel' does not exist on the 'mysql' connection.  

                ┌ Would you like to create it? ────────────────────────────────┐
                │ Yes                                                          │
                └──────────────────────────────────────────────────────────────┘

                INFO  Preparing database.  

                Creating migration table ............................................................................................................. 7.27ms DONE

                INFO  Running migrations.  

                0001_01_01_000000_create_users_table ................................................................................................ 24.42ms DONE
                0001_01_01_000001_create_cache_table ................................................................................................. 6.61ms DONE
                0001_01_01_000002_create_jobs_table ................................................................................................. 19.34ms DONE

        -   creazione di <LARAVEL_PROJECT_NAME>/resources/views/home.blade.php
        -   link del blade in <LARAVEL_PROJECT_NAME>/routes/web.php

                Route::get('/', function () {
                return view('home');
                });

        -   creazione <LARAVEL_PROJECT_NAME>/public/css/custom.css e link in blade

                <link rel="stylesheet" href="{{ asset('css/custom.css') }}">

        -   creazione <LARAVEL_PROJECT_NAME>/public/js/custom.js e link in blade

                <script src="{{ asset('js/custom.js') }}"></script>

        -   definizione di costanti da /opt/lampp/htdocs/WWW/PROJECTS/PHP/Laravel/<LARAVEL_PROJECT_NAME>/.env

                XAMPP_LOCALHOST="localhost"
                XAMPP_LOCALHOST_EXT="127.0.0.1"
                LARAVEL_LOCALHOST="127.0.0.1:8000"

        -   creazione di file di configurazione in config/const.php

                return [
                        'env' => ( ($_SERVER["HTTP_HOST"] !== env('XAMPP_LOCALHOST'))       #   utilizo di costanti da .env
                                && ($_SERVER["HTTP_HOST"] !== env('XAMPP_LOCALHOST_EXT')) 
                                && ($_SERVER["HTTP_HOST"] !== env('LARAVEL_LOCALHOST')) ) 
                                ? 'remote' 
                                : 'localhost',
                        'dbConst' => [
                                'localhost' => [
                                        'host' => 'localhost',
                                        'dbname' => 'miodb',
                                        'user' => 'root',
                                        'pwd' => ''
                                ],
                                'remote' => [
                                        'host' => '',
                                        'dbname' => '',
                                        'user' => '',
                                        'pwd' => ''
                                ]
                        ],
                ];

        -    utilizzo delle costanti in blade 
                
                {{ config('const.dbConst.' . config('const.env') . '.host') }} 





    