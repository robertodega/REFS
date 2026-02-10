- mkdir assets assets/docs assets/docs/mutuo assets/docs/stipendio assets/img classes config css DB inc js
- touch index.php .htaccess classes/conn.php classes/dbman.php classes/manager.php config/config.php css/boostrap.css css/custom.css css/graphs.css css/notfound.css inc/404.inc.php inc/bck-man.inc.php inc/charts.inc.php inc/content-container.inc.php inc/content.inc.php inc/doc-viewer-form.inc.php inc/doc-viewer.inc.php inc/functions.inc.php inc/header.inc.php inc/parameters.inc.php inc/update-form.inc.php inc/update-op.inc.php js/bootstrap.js js/custom.js js/graphs.js js/jquery.js
- nano classes/conn.php

        <?php
        $pdo = new Dbman();
        $conn = $pdo->getConn();
        $manager = new Manager($conn);

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

            public function getData($table)
            {
                $stmt = $this->conn->prepare("SELECT * FROM $table");
                $stmt->execute();
                return $stmt->fetchAll(PDO::FETCH_ASSOC);
            }

            public function updateData($year, $month, $tableName, $column, $value, $name)
            {
                $value = str_replace(',', '.', $value);
                
                $query_exist = "SELECT COUNT(*) FROM $tableName WHERE ref_year = :year AND ref_month = :month";
                $queryUpdate = "UPDATE $tableName SET $column = :value WHERE ref_year = :year AND ref_month = :month";
                $queryInsert = "INSERT INTO $tableName (ref_year, ref_month, $column) VALUES (:year, :month, :value)";
                
                if (in_array($tableName, ['bills', 'overview'])) {
                    $query_exist .= " AND name = :target";
                    $queryUpdate .= " AND name = :target";
                    $queryInsert = "INSERT INTO $tableName (ref_year, ref_month, name, $column) VALUES (:year, :month, :target, :value)";
                }

                $stmt = $this->conn->prepare($query_exist);
                $stmt->bindParam(':year', $year);
                $stmt->bindParam(':month', $month);

                if (strpos($query_exist, ':target') !== false) {
                    $stmt->bindParam(':target', $name);
                }

                $stmt->execute();
                $exists = $stmt->fetchColumn();

                try {
                    $q = ($exists && $exists > 0) ? $queryUpdate : $queryInsert;

                    $stmt = $this->conn->prepare($q);

                    $stmt->bindParam(':year', $year);
                    $stmt->bindParam(':month', $month);
                    $stmt->bindParam(':value', $value);
                    if (strpos($q, ':target') !== false) {
                        $stmt->bindParam(':target', $name);
                    }

                    // /* DEBUG */ $this->printQ($q, $value, $year, $month, "".$name."");die(); /* */

                    $stmt->execute();

                } catch (PDOException $e) {
                    $updateResult = $e;
                    #   throw new Exception("Update data error: " . $e->getMessage());
                }
                return true;
            }

            public function backupDb()
            {
                $backup_file = DB_PATH . date('Y_m_d-H_i_s') . '.sql';
                $dumpPath = trim(shell_exec('which mysqldump'));
                if (empty($dumpPath)) {
                    $dumpPath = trim(shell_exec('whereis mysqldump'));
                    if (empty($dumpPath)) {
                        echo "
                            <pre>Errore: mysqldump non trovato nel PATH di sistema.</pre><hr />
                            <button type='button' class='btn btn-primary btn-sm' ref='home' id='homeButton' onclick=\"location.href='" . ROOT_PATH . "'\">Home</button>
                        ";
                        exit;
                    }
                }
                $dumpPath = substr($dumpPath, strlen("mysqldump: "));
                $command = escapeshellcmd($dumpPath) . " --user=" . escapeshellarg(DB_USER) . " --password=" . escapeshellarg(DB_PWD) . " --host=" . escapeshellarg(DB_HOST) . " " . escapeshellarg(DB_NAME) . " 2>&1 > " . escapeshellarg($backup_file);
                $output = [];
                $return_var = 0;
                exec($command, $output, $return_var);
                if ($return_var !== 0) {
                    echo "
                        <pre>Errore nel backup (" . $return_var . "):\n" . implode("\n", $output) . "</pre><hr />
                        <button type='button' class='btn btn-primary btn-sm' ref='home' id='homeButton' onclick=\"location.href='" . ROOT_PATH . "'\">Home</button>
                    ";
                    exit;
                }
            }

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

            /* DEBUG */
            public function printQ($q, $value, $year, $month, $target)
            {
                $debugQuery = $q;
                $debugQuery = str_replace(':value', var_export($value, true), $debugQuery);
                $debugQuery = str_replace(':year', var_export($year, true), $debugQuery);
                $debugQuery = str_replace(':month', var_export($month, true), $debugQuery);
                if (strpos($q, ':target') !== false) {
                    $debugQuery = str_replace(':target', var_export($target, true), $debugQuery);
                }
                echo $debugQuery . PHP_EOL . "<br />";
            }
            /* */

        }

- nano config/config.php

        <?php
        //	DB constants
        $env = ($_SERVER["HTTP_HOST"] !== "localhost") ? "remote" : $_SERVER["HTTP_HOST"];

        $dbConst = [
            "localhost" => [
                "host" => "localhost",
                "dbname" => "finanza",
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

        define("ROOT_PATH", "./");
        define("CLASSES_PATH", ROOT_PATH . "classes/");
        define("INCLUDE_PATH", ROOT_PATH . "include/");
        define("CONFIG_PATH", ROOT_PATH . "config/");
        define("DB_PATH", ROOT_PATH . "DB/");
        define("CSS_PATH", ROOT_PATH . "css/");
        define("JS_PATH", ROOT_PATH . "js/");
        define("ASSETS_PATH", ROOT_PATH . "assets/");
        define("IMG_PATH", ASSETS_PATH . "img/");
        define("DOCS_PATH", ASSETS_PATH . "docs/");
        define("MUTUO_DOCS_PATH", DOCS_PATH . "mutuo/");
        define("INCOME_DOCS_PATH", DOCS_PATH . "stipendio/");
        define("CHARTS_JS_PATH", ASSETS_PATH . "charts/");

        define("MUTUO_START_YEAR", 2022);

        define("WEBSITE_OWNER", "Roberto De Gaetano");
        define("WEBSITE_OWNER_NICK", "RobDeGa");
        define("WEBSITE_TITLE", "Finanza&nbsp;&bull;&nbsp;" . WEBSITE_OWNER_NICK . "");
        define("DOCNOTFOUND_TITLE", "Doc Not Found");
        define("DOCNOTFOUND_MSG", "The document you were looking for doesn't exist.");
        define("DOCNOTFOUND_MSG_2", "Maybe it has not been uploaded yet.");

        $months = [
            'Gennaio' => '1',
            'Febbraio' => '2',
            'Marzo' => '3',
            'Aprile' => '4',
            'Maggio' => '5',
            'Giugno' => '6',
            'Luglio' => '7',
            'Agosto' => '8',
            'Settembre' => '9',
            'Ottobre' => '10',
            'Novembre' => '11',
            'Dicembre' => '12'
        ];

        $menuTags = [
            "totali",
            "overview",
            "bollette",
            "stipendio",
            "mutuo",
        ];
        $pageRefs = $menuTags;
        $pageRefs[] = "backup";
        $pageRefs[] = "backupDb";

        $tablesList = [
            "totali" => "contocorrente",
            "overview" => "overview",
            "bollette" => "bills",
            "stipendio" => "stipendio",
            "mutuo" => "mutuo",
        ];

        $datetime_fields = [
            'payment_date' => 'Data pagamento',
            'bill_date' => 'Data fattura'
        ];

        $allowedTags = [
            "totali" => ['spese_fisse', 'spese_extra', 'spese_totali', 'saldo'],
            "overview" => ['auto - Bollo', 'auto - Assicurazione', 'auto - Gomme', 'auto - Carburante', 'silat - Sporting', 'silat - Mike', 'bollette', 'siti_web', 'mutuo', 'viaggi'],
            "bollette" => ['luce', 'gas', 'acqua', 'spazzatura', 'internet', 'netflix', 'amazon_prime', 'assicurazione_casa', 'alleanza', 'telepass'],
            "stipendio" => ['lordo', 'netto', 'ticket_n', 'ticket_value', 'taxes', 'taxes_perc', 'tot_income'],
            "mutuo" => ['payment_date', 'amount', 'interests', 'capital'],
        ];

        $editableTags = [
            "totali" => ['saldo'],
            "overview" => ['auto - Bollo', 'auto - Assicurazione', 'auto - Gomme', 'auto - Carburante', 'silat - Sporting', 'silat - Mike', 'siti_web', 'viaggi'],
            "bollette" => ['luce', 'gas', 'acqua', 'spazzatura', 'internet', 'netflix', 'amazon_prime', 'assicurazione_casa', 'alleanza', 'telepass'],
            "stipendio" => ['lordo', 'netto', 'ticket_n', 'ticket_value'],
            "mutuo" => ['payment_date', 'amount', 'interests', 'capital'],
        ];

        $graphType = [
            "totali" => "Pie",
            "overview" => "Pie",
            "bollette" => "Pie",
            "stipendio" => "Pie",
            "mutuo" => "Pie",
        ];

        $graphAllowedTags = [
            "totali" => ['spese_fisse', 'spese_extra', 'spese_totali', 'saldo'],
            "overview" => ['auto - Bollo', 'auto - Assicurazione', 'auto - Gomme', 'auto - Carburante', 'silat - Sporting', 'silat - Mike', 'bollette', 'siti_web', 'mutuo', 'viaggi'],
            "bollette" => ['luce', 'gas', 'acqua', 'spazzatura', 'internet', 'netflix', 'amazon_prime', 'assicurazione_casa', 'alleanza', 'telepass'],
            "stipendio" => ['lordo', 'netto', 'taxes', 'tot_income'],
            "mutuo" => ['amount', 'interests', 'capital'],
        ];

