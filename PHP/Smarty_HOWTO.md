- mkdir SITE_NAME
- cd SITE_NAME
- cp -R smarty-4.5.5/libs .
- mkdir config inc styles scripts assets assets/docs assets/images classes DB templates templates_c
- chmod 777 templates templates_c
- touch .htaccess index.php config/config.php inc/functions.inc.php inc/dbman.inc.php DB/SITE_NAME.init.sql DB/SITE_NAME.sql css/style.css css/custom.css css/cookiebanner.css scripts/scripts.js classes/dbman.php classes/manager.php templates/index.tpl templates/notfound.tpl templates/TEMPLATE_SUB_FOLDER/navigation.tpl templates/TEMPLATE_SUB_FOLDER/header.tpl templates/TEMPLATE_SUB_FOLDER/page_content.tpl templates/TEMPLATE_SUB_FOLDER/footer.tpl .gitignore

- nano config/config.php

        <?php
        //	DB constants
        $env = ($_SERVER["HTTP_HOST"] !== "localhost") ? "remote" : $_SERVER["HTTP_HOST"];

        $dbConst = [
            "localhost" => [
                "host" => "localhost",
                "dbname" => "SITE_NAME",
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

        define("TEMPLATES_FOLDER", "TEMPLATE_SUB_FOLDER/");
        define("ROOT_PATH", "./");
        define("CLASSES_PATH", ROOT_PATH . "classes/");
        define("CONFIG_PATH", ROOT_PATH . "config/");
        define("INCLUDE_PATH", ROOT_PATH . "inc/");
        define("ASSETS_PATH", ROOT_PATH . "assets/");
        define("CSS_PATH", ROOT_PATH . "css/" . TEMPLATES_FOLDER);
        define("JS_PATH", ROOT_PATH . "scripts/" . TEMPLATES_FOLDER);
        define("IMG_PATH", ASSETS_PATH . TEMPLATES_FOLDER . "images/");
        define("DOCS_PATH", ASSETS_PATH . TEMPLATES_FOLDER . "docs/");

        define("KEYWORDS_TAG_VALUE", "");
        define("DESCRIPTION_TAG_VALUE", "");
        define("WEBSITE_AUTHOR", "");
        define("WEBSITE_OWNER", "");
        define("WEBSITE_TITLE", "");
        define("WEBSITE_NAME", "");
        define("WEBSITE_ADDRESS", "");

- nano inc/assigns.php

        <?php
        #   PATHS
        $smarty->assign('templates_folder', TEMPLATES_FOLDER);
        $smarty->assign('rootPath', ROOT_PATH);
        $smarty->assign('classesPath', CLASSES_PATH);
        $smarty->assign('confPath', CONFIG_PATH);
        $smarty->assign('incPath', INCLUDE_PATH);
        $smarty->assign('assetsPath', ASSETS_PATH);
        $smarty->assign('cssPath', CSS_PATH);
        $smarty->assign('jsPath', JS_PATH);
        $smarty->assign('imgPath', IMG_PATH);
        $smarty->assign('docsPath', DOCS_PATH);

        #   VARS
        $smarty->assign('keywordsTag', KEYWORDS_TAG_VALUE);
        $smarty->assign('descriptionTag', DESCRIPTION_TAG_VALUE);
        $smarty->assign('websiteAuthor', WEBSITE_AUTHOR);
        $smarty->assign('websiteOwner', WEBSITE_OWNER);
        $smarty->assign('websiteTitle', WEBSITE_TITLE);
        $smarty->assign('websiteName', WEBSITE_NAME);
        $smarty->assign('websiteAddress', WEBSITE_ADDRESS);

- nano inc/functions.inc.php

        <?php
        function e($value)
        {
            return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
        }

- nano inc/dbman.inc.php



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


- nano classes/manager.php

        <?php
        class Manager
        {
            private $conn;

            public function __construct($conn)
            {
                $this->conn = $conn;
            }

            #   content functions
            function scanContentDir($folder, $multilevel = false)
            {
                $res = [];
                $content = scandir($folder, 1);
                foreach ($content as $c) {
                    if (($c != '.') && ($c != '..')) {
                        if ($multilevel) {
                            $path = $folder . DIRECTORY_SEPARATOR . $c;
                            if (is_dir($path)) {
                                $res[$c] = scanContentDir($path, $multilevel);
                            } else {
                                $res[] = $c;
                            }
                        } else {
                            $res[] = $c;
                        }
                    }
                }
                return $res;
            }

            #   data functions
            public function getData($table)
            {
                $stmt = $this->conn->prepare("SELECT * FROM $table");
                $stmt->execute();
                return $stmt->fetchAll(PDO::FETCH_ASSOC);
            }
        }


- nano index.php

        <?php
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);

        require_once __DIR__ . '/libs/Smarty.class.php';

        include_once __DIR__ . '/config/config.php';
        include_once __DIR__ . '/classes/dbman.php';
        include_once __DIR__ . '/classes/manager.php';

        $smarty = new Smarty();
        $smarty->setTemplateDir(__DIR__ . '/templates/');
        $smarty->setCompileDir(__DIR__ . '/templates_c/');

        include_once __DIR__ . '/inc/assigns.php';

        include_once __DIR__ . '/inc/dbman.inc.php';

        $smarty->display('index.tpl');
        ?>

- nano templates/TEMPLATE_SUB_FOLDER/navigation.tpl

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container px-lg-5">
                <a class="navbar-brand" href="#!">Start Bootstrap</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item"><a class="nav-link active" aria-current="page" href="#!">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="about">About</a></li>
                        <li class="nav-item"><a class="nav-link" href="contact">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>

- nano templates/TEMPLATE_SUB_FOLDER/header.tpl

        <header class="py-5">
            <div class="container px-lg-5">
                <div class="p-4 p-lg-5 bg-light rounded-3 text-center">
                    <div class="m-4 m-lg-5">
                        <h1 class="display-5 fw-bold">TITLE</h1>
                        <p class="fs-4">SUBTITLE</p>
                        <a class="btn btn-primary btn-lg" href="#!">Call to action</a>
                    </div>
                </div>
            </div>
        </header>

- nano templates/TEMPLATE_SUB_FOLDER/page_content.tpl

        <section class="pt-4">
            <div class="container px-lg-5">
                ...
            </div>
        </section>

- nano templates/heroic/footer.tpl

        <footer class="py-5 bg-dark">
            <div class="container"><p class="m-0 text-center text-white">Copyright &copy; Your Website 2023</p></div>
        </footer>

- nano templates/index.tpl

        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>{$websiteTitle}</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
                <meta name="keywords" content="{$keywordsTag}">
                <meta name="description" content="{$descriptionTag}">
                <meta name="author" content="{$websiteAuthor}">
                <link rel="icon" type="image/x-icon" href="{$imgPath}favicon.ico" />
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet" />
                <link rel="stylesheet" href="{$cssPath}style.css" />
                <link rel="stylesheet" href="{$cssPath}cookiebanner.css" />
                <link rel="stylesheet" href="{$cssPath}custom.css" />
            </head>
            <body>
                
                {if !is_dir("templates/{$templates_folder}")}
                    {include file="templates/notfound.tpl"}
                {else}
                    {include file="templates/{$templates_folder}navigation.tpl"}
                    {include file="templates/{$templates_folder}header.tpl"}
                    {include file="templates/{$templates_folder}page_content.tpl"}
                    {include file="templates/{$templates_folder}footer.tpl"}
                {/if}

                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
                <script src="{$jsPath}scripts.js"></script>
            </body>
        </html>

- nano templates/notfound.tpl

        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>{$websiteTitle}</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
                <meta name="keywords" content="{$keywordsTag}">
                <meta name="description" content="{$descriptionTag}">
                <meta name="author" content="{$websiteAuthor}">
                <link rel="icon" type="image/x-icon" href="{$imgPath}favicon.ico" />
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet" />
                <link rel="stylesheet" href="{$cssPath}style.css" />
                <link rel="stylesheet" href="{$cssPath}cookiebanner.css" />
                <link rel="stylesheet" href="{$cssPath}custom.css" />
            </head>
            <body>
                Website template has not been found!
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
                <script src="{$jsPath}scripts.js"></script>
            </body>
        </html>

- nano .htaccess

        RewriteEngine On
            RewriteRule ^about$ about.php [L]
            RewriteRule ^contact$ contact.php [L]

- sudo /opt/lampp/lampp start
- Browse
