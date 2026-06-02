
- COMPOSER installation

        php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
        php -r "if (hash_file('sha384', 'composer-setup.php') === 'c8b085408188070d5f52bcfe4ecfbee5f727afa458b2573b8eaaf77b3419b0bf2768dc67c86944da1544f06fa544fd47') { echo 'Installer verified'.PHP_EOL; } else { echo 'Installer corrupt'.PHP_EOL; unlink('composer-setup.php'); exit(1); }"
        php composer-setup.php
        php -r "unlink('composer-setup.php');"

- PROJECT Creation

        -   composer create-project laravel/laravel <LARAVEL_PEOJECT_NAME>
        -   cd <LARAVEL_PEOJECT_NAME>
        -   php artisan --version

- PROJECT Customization

    -   in /opt/lampp/htdocs/WWW/PROJECTS/PHP/Laravel/<LARAVEL_PEOJECT_NAME>/.env

            DB_CONNECTION=mysql
            DB_HOST=127.0.0.1
            DB_PORT=3306
            DB_DATABASE=<PROJ_NAME>
            DB_USERNAME=root
            DB_PASSWORD=

    -   php artisan migrate

    -   nano routes/web.php

            Route::get('/', function () {
                return view('home');
            });

-   mkdir public/css public/js public/include

-   touch public/css/custom.css public/js/custom.js public/include/menunav.php

-   nano resources/views/home.blade.php

        <!DOCTYPE html>
        <html>
            <head>
                <title><PROJ_NAME> Laravel</title>
                <script src="https://code.jquery.com/jquery-3.7.1.slim.min.js" integrity="sha256-kmHvs0B+OpCW5GVHUNjv9rOmY0IvSIRcf7zGUDTDQM8=" crossorigin="anonymous"></script>
                <link rel="stylesheet" href="{{ asset('css/custom.css') }}">
            </head>
            <body>
                <?php include '../public/include/menunav.php'; ?>
                <h1>Benvenuto nella <PROJ_NAME> Laravel!</h1>
            </body>
        </html>

        <script src="{{ asset('js/custom.js') }}"></script>

-   Using Controller

    -   php artisan make:controller <PROJ_NAME>Controller

    -   nano routes/web.php

            use Illuminate\Support\Facades\Route;
            use App\Http\Controllers\<PROJ_NAME>Controller;

            Route::get('/', [<PROJ_NAME>Controller::class, 'index']);

    -   in /Laravel/<PROJ_NAME>/app/Http/Controllers/<PROJ_NAME>Controller.php:

            <?php

            namespace App\Http\Controllers;

            use Illuminate\Http\Request;

            class <PROJ_NAME>Controller extends Controller
            {
                public function index()
                {
                    return view('home');
                }
            }

    -   php artisan serve