
[ https://laravel.com/docs/10.x#your-first-laravel-project ]



DEPENDENCES
---

download && install composer:

        php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
        php -r "if (hash_file('sha384', 'composer-setup.php') ==='55ce33d7678c5a611085589f1f3ddf8b3c52d662cd01d4ba75c0ee0459970c2200a51f492d557530c71c15d8dba01eae') { echo 'Installer verified'; } else { echo'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
        php composer-setup.php
        php -r "unlink('composer-setup.php');"

put the composer.phar into a directory to simply call composer from any directory (Global install)

        sudo mv composer.phar /usr/local/bin/composer

Run composer
---

        php composer.phar
        
install Node and NPM
--------------------

        https://nodejs.org/en


LARAVEL
---

create a new Laravel project via Composer

        > composer create-project laravel/laravel <APP_NAME>

Or create a new Laravel projects by globally installing the Laravel installer via Composer

        > composer global require laravel/installer

        > cd ~/.config/composer/vendor/bin/
        > pwd
         - copy this path into .bashrc file

                ...
                export PATH=<COPIED_PATH>:$PATH
        > laravel

                Laravel Installer 5.7.1
                        Usage:
                        ...
                        

        laravel new <APP_NAME>

start Laravel's local development server using the Laravel's Artisan CLI serve command

        cd <APP_NAME>
        php artisan serve

        http://localhost:8000. 

        - versione installata:  php artisan --version

VIRTUAL HOSTS
---

        >  sudo nano /opt/lampp/etc/httpd.conf
                -       ricerca di Virtual hosts
                -       decommentare #Include etc/extra/httpd-vhosts.conf
        > sudo nano /opt/lampp/etc/extra/httpd-vhosts.conf

                <VirtualHost *:80>
                        ServerAdmin webmaster@dummy-host2.example.com
                        DocumentRoot "/opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/public"
                        ServerName testProj.local
                        <Directory "/opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/public">
                                Options All
                                AllowOverride All
                                Rquire all granted
                        </Directory>
                        ErrorLog "logs/testProj-error_log"
                        CustomLog "logs/testProj-access_log" common
                </VirtualHost>
        >  cd
        >  cd /etc/
        > sudo nano hosts
                -       completare la riga 
                        
                        127.0.0.1       localhost 
                        
                        aggiungendo il nome del ServerName
                        
                        127.0.0.1       localhost testProj.local

                Riavviare XAMPP

DATABASE & MIGRATIONS
---

Run application's database migrations, which will create application's database tables

        php artisan migrate

VISTE AGGIUNTIVE
---
        -       Gestione pagine di errore

                -       php artisan vendor:publish
                        scendere fino a 'Tag: laravel-errors'

        Copying directory [vendor/laravel/framework/src/Illuminate/Foundation/Exceptions/views] to [resources/views/errors] ......................... DONE

                -       modificare a piacimento il file blade desiderato (es. '404.blade.php')
                
                        <?php /* * ?>

                        @section('message', __('Not Found'))
                        
                        <?php /* */ ?>
                        
                        @section('message')
                        {{$exception->getMessage()}}
                        @endsection
                        
                        <?php /* */ ?>

                        o il file blade esteso (es. 'minimal.blade.php')

LARAVEL IMPORTANT PATHS
---

        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/bootstrap/app.php                       # gestione management files
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/routes/web.php                          # gestione rotte
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/config/app.php                          # configurazione app
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/config/database.php                     # configurazione DB
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/.env                                    # variabili d'ambiente
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/app/Models/User.php                     # gestione utenti sistema
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/app/Http/Controllers/Controller.php     # classi sistema
        -       /opt/lampp/htdocs/WWW/PROJECTS/Laravel/testProj/resources/views/errors                  # pagine gestione errori (dopo php artisan vendor:publish)

GESTIONE ROTTE
---

        php artisan route:list                                                                          #       lista delle rotte predefinite

        Route::get('/users/{name?}/{lastname?}/{age?}', 
                #       static function(string $name, string $lastname, int $age) {                             #   parametri obbligatori
                static function(?string $name = '', ?string $lastname = '', ?int $age = 0) {            #   parametri opzionali
                        echo "<h1>Hello User $name $lastname, you are $age years old</h1>";
                }
        )
        ->where(                                                                                        #   check parametri passati
                [
                        'age' => '[0-9]{2,3}',                  #   check con regular expression su valore numerico età con minimo 2 massimo 3 cifre numeriche
                        'name' => '[a-zA-Z]{3,}',               #   check con regular expression su valore stringa name con minimo 3 caratteri
                        'lastname' => '[a-zA-Z]{2,}',           #   check con regular expression su valore stringa lastname con minimo 2 caratteri
                ]
        )

        Route::view('user-details', 'userDetail', [             #   rotta su vista custom (parametro url => destination file in /resources/views)
                'name' => 'Nome',
                'lastname' => 'Cognome',
        ]);

        Route::get('/dettaglioUtente', function () {
                return redirect('users/Nome/Cognome/47');       #   Route redirect
        });

GESTIONE ROTTE TRAMITE CONTROLLER
---

        -       Creazione controller
        -       --------------------
        -       php artisan make:controller --help              #    help menu
        -       php artisan make:controller <ControllerName>

                es. php artisan make:controller UsersController --resource -m User        # controller di tipo resource che usa il model di default User

        use App\Http\Controllers\UsersController;               #   inclusione controller

Route::resource
---
        Permette di mappare automaticamente i metodi
        --------------------------------------------

        Route::resource('users', UsersController::class);       #   gestione rotta users tramite controller UsersController

        -       edit public function index() del controller

                -       return [                                #       dato di esempio custom
                                'name' => 'Nome',
                                'lastname' => 'Cognome',
                                'age' => 'eta',
                        ];

                -       return User::all();                     #       dati da tabella users in DB

                il comando 'php artisan route:list' restituisce tra le altre:
                #   GET|HEAD        users/{user} ............................................................. users.show › UsersController@show
                gestisce quindi il singolo utente (users/{user}) tramite il metodo show del controller UsersController, che può essere editato:

                        public function show(User $user)
                        {
                                return $user;
                        }

Rotte verso metodi custom
---
        Route::get('users/detail/{user}', [UsersController::class, 'userDetail']);      #       utilizzo metodo custom userDetail da controller UsersController

VISTE
---

        php artisan make:controller PageController              #       creazione controller per le viste

        Passaggio parametri
        -------------------

        -       inserimento in controller del parametro da passare come protected

                        protected $data = [...]

        -       creazione vista e riferimento nel controller

                        public function staff(){

                                #   passaggio tramite variabile protected
                                #   -------------------------------------
                                return view('staff', 
                                    [
                                        'title' => 'Staff', 
                                        'staff' => $this->data
                                    ]
                                );

                                #   passaggio tramite metodo eloquent
                                #   ---------------------------------
                                return view('staff')
                                ->with('staff', $this->data)
                                ->with('title','Staff');

                                #   passaggio tramite metodi eloquent magici (non esistenti ma creati al volo da php)
                                #   ---------------------------------------------------------------------------------
                                return view('staff')->withStaff($this->data)->withTitle('Staff');

                                #   funzione compact di PHP
                                #   -----------------------
                                $staff = $this->data;
                                $title = 'Staff';
                                return view('staff', compact('title','staff'));
                        }
        
        -       nella vista, ciclare sull'array $staff per usare i campi inseriti nella variabile protected

