- mkdir Login
- cd Login
- mkdir config classes inc templates css js DB
- touch index.php logout.php check_session.php .htaccess functions.php config/config.php classes/dbman.php classes/manager.php classes/conn.php css/custom.css js/custom.js templates/loginform.php templates/signinform.php templates/dashboard.php DB/login.sql

- nano .htaccess

        RewriteEngine On
            RewriteRule ^login$ index.php [L]
            RewriteRule ^logout$ logout.php [L]
            RewriteRule ^dashboard$ dashboard.php [L]

- nano DB/login.sql

        -- phpMyAdmin SQL Dump
        -- version 5.2.1
        -- https://www.phpmyadmin.net/
        --
        -- Host: localhost
        -- Creato il: Gen 27, 2026 alle 14:39
        -- Versione del server: 10.4.28-MariaDB
        -- Versione PHP: 8.2.4

        SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
        START TRANSACTION;
        SET time_zone = "+00:00";


        /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
        /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
        /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
        /*!40101 SET NAMES utf8mb4 */;

        --
        -- Database: `login`
        --
        CREATE DATABASE IF NOT EXISTS `login` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
        USE `login`;

        -- --------------------------------------------------------

        --
        -- Struttura della tabella `users`
        --

        DROP TABLE IF EXISTS `users`;
        CREATE TABLE `users` (
        `id` int(11) NOT NULL,
        `profile_id` int(11) DEFAULT NULL,
        `username` varchar(50) DEFAULT NULL,
        `password_hash` varchar(255) DEFAULT NULL,
        `email` varchar(100) DEFAULT NULL,
        `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
        `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

        --
        -- Indici per le tabelle scaricate
        --

        --
        -- Indici per le tabelle `users`
        --
        ALTER TABLE `users`
        ADD PRIMARY KEY (`id`);

        --
        -- AUTO_INCREMENT per le tabelle scaricate
        --

        --
        -- AUTO_INCREMENT per la tabella `users`
        --
        ALTER TABLE `users`
        MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
        COMMIT;

        /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
        /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
        /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


- nano inc/functions.php

        <?php
            function e($value)
            {
                return htmlspecialchars($value, ENT_QUOTES, "UTF-8");
            }

- nano config/config.php

        <?php

            //	DB constants
            $env = ($_SERVER["HTTP_HOST"] !== "localhost") ? "remote" : $_SERVER["HTTP_HOST"];

            $dbConst = [
                "localhost" => [
                    "host" => "localhost",
                    "dbname" => "login",
                    "user" => "root",
                    "pwd" => ""
                ],
                "remote" => [
                    "host" => "",
                    "dbname" => "",
                    "user" => "",
                    "pwd" => ""
                ]
            ];
            define("DB_HOST", $dbConst["" . $env . ""]["host"]);
            define("DB_NAME", $dbConst["" . $env . ""]["dbname"]);
            define("DB_USER", $dbConst["" . $env . ""]["user"]);
            define("DB_PWD", $dbConst["" . $env . ""]["pwd"]);

            //  path constants
            define("ROOT_PATH", "./");
            define("CSS_PATH", ROOT_PATH . "css/");
            define("JS_PATH", ROOT_PATH . "js/");

            // other constants
            define("WEBSITE_TITLE", "Login App");
            define("USERNAME_LABEL", "Username");
            define("PASSWORD_LABEL", "Password");
            define("LOGIN_BUTTON_TEXT", "Login");
            define("RESET_BUTTON_TEXT", "Reset");
            define("SIGNIN_BUTTON_TEXT", "Sign in!");


- nano classes/dbman.php

        <?php

            class Dbman
            {
                private $pdo;

                public function __construct()
                {
                    try {
                        $this->pdo = new PDO('mysql:host=' . DB_HOST . '; dbname=' . DB_NAME . '', DB_USER, DB_PWD);
                    } catch (PDOException $e) {
                        die("DB Connection failed: " . $e->getMessage());
                    }
                }

                public function getConn()
                {
                    return $this->pdo;
                }
            }

- nano classe/manager.php

        <?php
            class Manager
            {
                private $conn;

                public function __construct($conn)
                {
                    $this->conn = $conn;
                }

                public function getData($table, $field = '', $param = '')
                {
                    $q = "SELECT * FROM $table";
                    if ($field && $param) {
                        $q .= " WHERE " . $field . " = '" . $param . "'";
                    }
                    $stmt = $this->conn->prepare($q);
                    $stmt->execute();
                    return $stmt->fetchAll(PDO::FETCH_ASSOC);
                }

                function auth_user($login_json)
                {
                    session_start([
                        'cookie_lifetime' => 86400,
                        'cookie_httponly' => true, // JS cookie-stealing fix
                        // 'cookie_secure' => true,   // for HTTPS use only
                        'samesite' => 'Strict',
                    ]);

                    if ($_SERVER['REQUEST_METHOD'] === 'POST') {

                        $username = $_POST['username'] ?? '';
                        $pass = $_POST['password'] ?? '';

                        if (empty($username) || empty($pass)) {
                            return false;
                        }

                        try {
                            $user_data = $this->getData('users', 'username', $username);

                            if (!empty($user_data)) {
                                if (password_verify($pass, $user_data[0]['password_hash'])) {

                                    session_regenerate_id(true);
                                    $_SESSION['loggedin'] = true;
                                    $_SESSION['user_id'] = $user_data[0]['id'];
                                    $_SESSION['username'] = $username;
                                    $_SESSION['profile_id'] = $user_data[0]['profile_id'];

                                    return true;
                                } else {
                                    return false;
                                }
                            } else {
                                return false;
                            }
                        } catch (Exception $e) {
                            return htmlspecialchars($e->getMessage());
                            exit;
                        }
                    }
                    return false;
                }
            }

- nano classes/conn.php

        <?php
            $pdo = new Dbman();
            $conn = $pdo->getConn();
            $manager = new Manager($conn);

- nano index.php

        <?php
        require_once __DIR__ . "/config/config.php";
        require_once __DIR__ . "/inc/functions.php";
        require_once __DIR__ . "/classes/dbman.php";
        require_once __DIR__ . "/classes/manager.php";
        require_once __DIR__ . "/classes/conn.php";

        $auth_user_msg = $manager->auth_user();
        ?>
        <!DOCTYPE HTML>
        <html>

        <head>
            <title><?= WEBSITE_TITLE ?></title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />

            <script src="https://code.jquery.com/jquery-4.0.0.min.js" integrity="sha256-OaVG6prZf4v69dPg6PhVattBXkcOWQB62pdZ3ORyrao=" crossorigin="anonymous"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>

            <link rel="stylesheet" href="<?= CSS_PATH ?>custom.css" />

        </head>

        <body>
            <?php
                if (!$auth_user_msg) {
                    include __DIR__ . "/templates/loginform.php";
                } else {
                    $signin = $_GET['signin'] ?? false;
                    if (!$signin) {include __DIR__ . "/templates/signinform.php";}
                    else{include __DIR__ . "/templates/dashboard.php";}
                }
            ?>

        </body>

        </html>
        <script src="<?= JS_PATH ?>custom.js"></script>


- nano templates/loginform.php

        <form method="post" action="login" id="login-form" name="login-form">
            <div class="form-group">
                <label for="username"><?= USERNAME_LABEL ?></label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password"><?= PASSWORD_LABEL ?></label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="login-btn" id="login-btn"><?= LOGIN_BUTTON_TEXT ?></button>
            <button type="reset" class="login-btn" id="reset-btn"><?= RESET_BUTTON_TEXT ?></button>
            <button type="button" class="login-btn" id="signin-btn"><?= SIGNIN_INSTR_LABEL ?></button>
        </form>
        
- nano templates/dashbard.php

        <?php require_once __DIR__ . '/../check_session.php'; ?>
        <div class="dashboard-container">
            <div class="dashboard-header">
                <div class="dashboard-title">
                    Dashboard
                </div>
                <div class="dashboard-logout">
                    <a href="logout">Logout</a>
                </div>
            </div>
            <div class="dashboard-container">
                You Logged In!
            </div>
        </div>

- nano templates/signinform.php

        <?php
        $signin_act = $_POST['signin-field'] ?? false;
        if ($signin_act) {
            // $set_user_msg = $manager->set_user($signin_json);
            ?><h2>Memorizzando ... </h2><?php
        } else {
        ?>
            <form method="post" id="login-form" name="login-form" action="signin">
                <div class="form-group">
                    <label for="username"><?= USERNAME_LABEL ?></label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="email"><?= EMAIL_LABEL ?></label>
                    <input type="text" id="email" name="email">
                </div>
                <div class="form-group">
                    <label for="password"><?= PASSWORD_LABEL ?></label>
                    <input type="password" id="password" name="password" required>
                </div>

                <input type="hidden" id="signin-field" name="signin-field" value="1">

                <button type="submit" class="login-btn" id="signin-act-btn"><?= SIGNIN_BUTTON_TEXT ?></button>
                <button type="reset" class="login-btn" id="reset-btn"><?= RESET_BUTTON_TEXT ?></button>
                <button type="button" class="login-btn" id="undo-btn"><?= UNDO_BUTTON_TEXT ?></button>
            </form>
        <?php
        }
        ?>

- nano logout.php

        <?php
        session_unset();
        session_destroy();
        header('Location: ./');

- nano check_session.php

        <?php
            if (session_status() === PHP_SESSION_NONE) {
                session_start();
            }

            function check_auth()
            {
                if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
                    session_unset();
                    session_destroy();
                    header("Location: ".ROOT_PATH."");
                    exit;
                }
            }

            check_auth();

- nano js/custom.js

        $("#signin-btn").on("click", function () {
          $("#login-form").attr("action", "signin");
          $("#username").removeAttr("required");
          $("#password").removeAttr("required");
          $("#login-form").submit();
        });

        $("#undo-btn").on("click", function () {
          document.location.href = "login";
        });
