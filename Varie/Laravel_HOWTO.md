        -   composer create-project laravel/laravel <LARAVEL_PEOJECT_NAME>
        -   php artisan --version
        -   in /opt/lampp/htdocs/WWW/PROJECTS/PHP/Laravel/<LARAVEL_PEOJECT_NAME>/.env

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

        -   creazione di <LARAVEL_PEOJECT_NAME>/resources/views/home.blade.php
        -   link del blade in <LARAVEL_PEOJECT_NAME>/routes/web.php

                Route::get('/', function () {
                return view('home');
                });

        -   creazione <LARAVEL_PEOJECT_NAME>/public/css/custom.css e link in blade

                <link rel="stylesheet" href="{{ asset('css/custom.css') }}">

        -   creazione <LARAVEL_PEOJECT_NAME>/public/js/custom.js e link in blade

                <script src="{{ asset('js/custom.js') }}"></script>



    