import os
import shutil
#   from pathlib import Path

project_folders = [
    "config",
    "classes",
    "inc",
    "templates",
    "assets",
    "assets/images",
    "css",
    "js",
    "DB",
]

file_body_content = {
    ".htaccess":"RewriteEngine On\
            \n\tRewriteRule ^login$ index.php?login=true [L]\
            \n\tRewriteRule ^signin$ index.php?signin=true [L]\
            \n\tRewriteRule ^dashboard$ dashboard.php [L]\
    ",
    "inc/functions.php":"<?php\
            \n\tfunction e($value)\
            \n\t{\
                \n\t\treturn htmlspecialchars($value, ENT_QUOTES, 'UTF-8');\
            \n\t}\
    ",
    "config/config.php":"",
    "classes/dbman.php":"<?php\
            \n\tclass Dbman\
            \n\t{\
                \n\t\tprivate $pdo;\
                \n\t\tpublic function __construct()\
                \n\t\t{\
                    \n\t\t\ttry {\
                        \n\t\t\t\t$this->pdo = new PDO('mysql:host=' . DB_HOST . '; dbname=' . DB_NAME . '', DB_USER, DB_PWD);\
                    \n\t\t\t} catch (PDOException $e) {\
                        \n\t\t\t\tif (strpos($e->getMessage(), 'Unknown database')) {\
                            \n\t\t\t\t\tdie('DB is apparently missing - Try loading DB/db.sql in PHPMyAdmin');\
                        \n\t\t\t\t}else{\
                        \n\t\t\t\t\tdie('DB Connection failed: ' . $e->getMessage());\
                        \n\t\t\t\t}\
                    \n\t\t\t}\
                \n\t\t}\
                \n\t\tpublic function getConn()\
                \n\t\t{\
                    \n\t\t\treturn $this->pdo;\
                \n\t\t}\
            \n\t}\
    ",
    "classes/manager.php":"<?php\
            \n\tclass Manager\
            \n\t{\
                \n\t\tprivate $conn;\
                \n\t\tpublic function __construct($conn)\
                \n\t\t{\
                    \n\t\t\t$this->conn = $conn;\
                \n\t\t}\
                \n\t\tpublic function getData($table, $field = '', $param = '')\
                \n\t\t{\
                    \n\t\t\t$q = 'SELECT * FROM $table';\
                    \n\t\t\tif ($field && $param) {\
                        \n\t\t\t\t$q .= \" WHERE ' . $field . ' = ' . $param . '\";\
                    \n\t\t\t}\
                    \n\t\t\t$stmt = $this->conn->prepare($q);\
                    \n\t\t\t$stmt->execute();\
                    \n\t\t\treturn $stmt->fetchAll(PDO::FETCH_ASSOC);\
                \n\t\t}\
                \n\t\tfunction auth_user()\
                \n\t\t{\
                    \n\t\t\tsession_start([\
                        \n\t\t\t\t'cookie_lifetime' => 86400,\
                        \n\t\t\t\t'cookie_httponly' => true, // JS cookie-stealing fix\
                        \n\t\t\t\t// 'cookie_secure' => true,   // for HTTPS use only\
                        \n\t\t\t\t// 'samesite' => 'Strict',\
                    \n\t\t\t]);\
                    \n\t\t\tif ($_SERVER['REQUEST_METHOD'] === 'POST') {\
                        \n\t\t\t\t$username = $_POST['username'] ?? '';\
                        \n\t\t\t\t$pass = $_POST['password'] ?? '';\
                        \n\t\t\t\tif (empty($username) || empty($pass)) {\
                            \n\t\t\t\t\treturn false;\
                        \n\t\t\t\t}\
                        \n\t\t\t\ttry {\
                            \n\t\t\t\t\t$user_data = $this->getData('users', 'username', $username);\
                            \n\t\t\t\t\tif (!empty($user_data)) {\
                                \n\t\t\t\t\t\tif (password_verify($pass, $user_data[0]['password_hash'])) {\
                                    \n\t\t\t\t\t\t\tsession_regenerate_id(true);\
                                    \n\t\t\t\t\t\t\t$_SESSION['loggedin'] = true;\
                                    \n\t\t\t\t\t\t\t$_SESSION['user_id'] = $user_data[0]['id'];\
                                    \n\t\t\t\t\t\t\t$_SESSION['username'] = $username;\
                                    \n\t\t\t\t\t\t\t$_SESSION['profile_id'] = $user_data[0]['profile_id'];\
                                    \n\t\t\t\t\t\t\treturn true;\
                                \n\t\t\t\t\t\t} else {\
                                    \n\t\t\t\t\t\t\treturn false;\
                                \n\t\t\t\t\t\t}\
                            \n\t\t\t\t\t} else {\
                                \n\t\t\t\t\t\treturn false;\
                            \n\t\t\t\t\t}\
                        \n\t\t\t\t} catch (Exception $e) {\
                            \n\t\t\t\t\treturn htmlspecialchars($e->getMessage());\
                            \n\t\t\t\t\texit;\
                        \n\t\t\t\t}\
                    \n\t\t\t}\
                    \n\t\t\treturn false;\
                \n\t\t}\
            \n\t}\
    ",
    "classes/conn.php":"<?php\
            \n\t$pdo = new Dbman();\
            \n\t$conn = $pdo->getConn();\
            \n\t$manager = new Manager($conn);\
    ",
    "DB/db.sql":"",
    "index.php":"<?php\
        \nrequire_once __DIR__ . '/config/config.php';\
        \nrequire_once __DIR__ . '/inc/functions.php';\
        \nrequire_once __DIR__ . '/classes/dbman.php';\
        \nrequire_once __DIR__ . '/classes/manager.php';\
        \nrequire_once __DIR__ . '/classes/conn.php';\n\
        \n$auth_user_msg = $manager->auth_user();\
        \n?>\
        \n<!DOCTYPE HTML>\
        \n<html>\
        \n\t<head>\
            \n\t\t<title><?= WEBSITE_TITLE ?></title>\
            \n\t\t<meta charset='utf-8' />\
            \n\t\t<meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />\
            \n\t\t<script src='https://code.jquery.com/jquery-4.0.0.min.js' integrity='sha256-OaVG6prZf4v69dPg6PhVattBXkcOWQB62pdZ3ORyrao=' crossorigin='anonymous'></script>\
            \n\t\t<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' integrity='sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH' crossorigin='anonymous'>\
            \n\t\t<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js' integrity='sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy' crossorigin='anonymous'></script>\
            \n\t\t<link rel='stylesheet' href='<?= CSS_PATH ?>custom.css' />\
        \n\t</head>\
        \n\t<body>\
            \n\t<?php\
                \n\t\tif (!$auth_user_msg) {\
                    \n\t\t\tinclude __DIR__ . '/templates/loginform.php';\
                \n\t\t} else {\
                    \n\t\t\t$signin = $_GET['signin'] ?? false;\
                    \n\t\t\tif (!$signin) {include __DIR__ . '/templates/signinform.php';}\
                    \n\t\t\telse{include __DIR__ . '/templates/dashboard.php';}\
                \n\t\t}\
            \n\t?>\
        \n\t</body>\
        \n</html>\
        \n<script src='<?= JS_PATH ?>custom.js'></script>\
    ",
    "templates/loginform.php":"<form method='post' action='login' id='login-form' name='login-form'>\
            \n\t<div class='form-group'>\
                \n\t\t<label for='username'><?= USERNAME_LABEL ?></label>\
                \n\t\t<input type='text' id='username' name='username' required>\
            \n\t</div>\
            \n\t<div class='form-group'>\
                \n\t\t<label for='password'><?= PASSWORD_LABEL ?></label>\
                \n\t\t<input type='password' id='password' name='password' required>\
            \n\t</div>\
            \n\t<button type='submit' class='login-btn' id='login-btn'><?= LOGIN_BUTTON_TEXT ?></button>\
            \n\t<button type='reset' class='login-btn' id='reset-btn'><?= RESET_BUTTON_TEXT ?></button>\
            \n\t<button type='button' class='login-btn' id='signin-btn'><?= SIGNIN_INSTR_LABEL ?></button>\
        \n</form>\
    ",
    "templates/dashboard.php":"<?php require_once __DIR__ . '/../check_session.php'; ?>\
        \n<div class='dashboard-container'>\
            \n\t<div class='dashboard-header'>\
                \n\t\t<div class='dashboard-title'>\
                    \n\t\t\tDashboard\
                \n\t\t</div>\
                \n\t\t<div class='dashboard-logout'>\
                    \n\t\t\t<a href='logout'>Logout</a>\
                \n\t\t</div>\
            \n\t</div>\
            \n\t<div class='dashboard-container'>\
                \n\t\tYou Logged In!\
            \n\t</div>\
        \n</div>\
    ",
    "templates/signinform.php":"<?php\
        \n$signin_act = $_POST['signin-field'] ?? false;\
        \nif ($signin_act) {\
            \n\t// $set_user_msg = $manager->set_user($signin_json);\
            \n\t?><h2>Memorizzando ... </h2><?php\
        \n} else {\
        ?>\
            \n\t<form method='post' id='login-form' name='login-form' action='signin'>\
                \n\t\t<div class='form-group'>\
                    \n\t\t\t<label for='username'><?= USERNAME_LABEL ?></label>\
                    \n\t\t\t<input type='text' id='username' name='username' required>\
                \n\t\t</div>\
                \n\t\t<div class='form-group'>\
                    \n\t\t\t<label for='email'><?= EMAIL_LABEL ?></label>\
                    \n\t\t\t<input type='text' id='email' name='email'>\
                \n\t\t</div>\
                \n\t\t<div class='form-group'>\
                    \n\t\t\t<label for='password'><?= PASSWORD_LABEL ?></label>\
                    \n\t\t\t<input type='password' id='password' name='password' required>\
                \n\t\t</div>\n\
                \n\t\t<input type='hidden' id='signin-field' name='signin-field' value='1'>\n\
                \n\t\t<button type='submit' class='login-btn' id='signin-act-btn'><?= SIGNIN_BUTTON_TEXT ?></button>\
                \n\t\t<button type='reset' class='login-btn' id='reset-btn'><?= RESET_BUTTON_TEXT ?></button>\
                \n\t\t<button type='button' class='login-btn' id='undo-btn'><?= UNDO_BUTTON_TEXT ?></button>\
            \n\t</form>\
        \n<?php\
        \n}\
        \n?>\
    ",
    "logout.php":"<?php\
        \nsession_unset();\
        \nsession_destroy();\
        \nheader('Location: ./');\
    ",
    "check_session.php":"<?php\
            \nif (session_status() === PHP_SESSION_NONE) {\
                \n\tsession_start();\
            \n}\n\
            \nfunction check_auth()\
            \n{\
                \n\tif (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {\
                    \n\t\tsession_unset();\
                    \n\t\tsession_destroy();\
                    \n\t\theader('Location: '.ROOT_PATH.'');\
                    \n\t\texit;\
                \n\t}\
            \n}\n\
            \ncheck_auth();\
    ",
    "css/custom.css":"",
    "js/custom.js":"$('#signin-btn').on('click', function () {\
          \n\t$('#login-form').attr('action', 'signin');\
          \n\t$('#username').removeAttr('required');\
          \n\t$('#password').removeAttr('required');\
          \n\t$('#login-form').submit();\
        \n});\n\
        \n$('#undo-btn').on('click', function () {\
          \n\tdocument.location.href = 'login';\
        \n});\
    ",
    "DB/db.sql":"CREATE DATABASE login;\
    \nUSE login;\
    \nCREATE TABLE users(id INT PRIMARY KEY AUTO_INCREMENT, profile_id int, username varchar(50), password_hash varchar(255), email varchar(100), created_at timestamp NOT NULL DEFAULT current_timestamp(), updated_at timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp());\
    ",
}

def folder_creation():
    folderName = ""
    while folderName == "":
        os.system("cls")
        folderName = input("Type in the name of the folder to create: ")

    print(f"\n\n\t\t> ' ***** ROOT folder creation *****\n")
    os.makedirs(folderName, exist_ok=True)
    print(f"\t> '{folderName}' folder creation ... ", end="")
    os.chdir(f"{folderName}")
    print("DONE")

    return folderName


def work_folders_creation(folderName):
    print(f"\n\n\t\t> ' ***** Work folder creation *****\n")
    for folder in project_folders:
        print(f"\t> '{folderName}/{folder}' folder creation ... ", end="")
        os.makedirs(f"{folder}", exist_ok=True)
        print("DONE")

def work_files_creation(folderName):
    print(f"\n\n\t\t> ' ***** Work files creation *****\n")
    db_name = folderName.lower()
    for fn, fc in file_body_content.items():
        print(f"\t> '{fn}' file creation ... ", end="")

        if fn == "config/config.php":
            filecontent = "<?php\
            \n\t//	DB constants\
            \n\t$env = ($_SERVER['HTTP_HOST'] !== 'localhost') ? 'remote' : $_SERVER['HTTP_HOST'];\
                \
            \n\t$dbConst = [\
                \n\t\t'localhost' => [\
                    \n\t\t\t'host' => 'localhost',\
                    \n\t\t\t'dbname' => '"+db_name+"',\
                    \n\t\t\t'user' => 'root',\
                    \n\t\t\t'pwd' => ''\
                \n\t\t],\
                \n\t\t'remote' => [\
                    \n\t\t\t'host' => '',\
                    \n\t\t\t'dbname' => '',\
                    \n\t\t\t'user' => '',\
                    \n\t\t\t'pwd' => ''\
                \n\t\t],\
            \n\t];\
            \n\tdefine('DB_HOST', $dbConst['' . $env . '']['host']);\
            \n\tdefine('DB_NAME', $dbConst['' . $env . '']['dbname']);\
            \n\tdefine('DB_USER', $dbConst['' . $env . '']['user']);\
            \n\tdefine('DB_PWD', $dbConst['' . $env . '']['pwd']);\
                \
            \n\t//  path constants\
            \n\tdefine('ROOT_PATH', './');\
            \n\tdefine('CSS_PATH', ROOT_PATH . 'css/');\
            \n\tdefine('JS_PATH', ROOT_PATH . 'js/');\
                \
            \n\t// other constants\
            \n\tdefine('WEBSITE_TITLE', 'Login App');\
            \n\tdefine('USERNAME_LABEL', 'Username');\
            \n\tdefine('EMAIL_LABEL', 'Email');\
            \n\tdefine('PASSWORD_LABEL', 'Password');\
            \n\tdefine('LOGIN_BUTTON_TEXT', 'Login');\
            \n\tdefine('RESET_BUTTON_TEXT', 'Reset');\
            \n\tdefine('SIGNIN_BUTTON_TEXT', 'Sign in!');\
            \n\tdefine('SIGNIN_INSTR_LABEL', 'Sign in!');\
            \n\tdefine('UNDO_BUTTON_TEXT', 'Undo');\
        "
        else:
            filecontent = fc
            #   filecontent = fc.strip()
        
        with open(f"{fn}", "w") as f:
            f.write(f"{filecontent}")

        print("DONE")

def files_strip():
    for fn, fc in file_body_content.items():
        pass

def folder_management(folderName):
    print(f"\n\t> Current Path: {os.getcwd()}")
    print(f"\t> Folder Content: {os.listdir()}")
    print(f"\n\n\t\t> ' ***** App Run Link *****\n")
    print(f"\n\t> Open App in browser at http://localhost/WWW/PHP/{folderName}/")
    print(f"\n\t> If DB {folderName.lower()} is not present, load file 'DB/db.sql' in PHPMyAdmin\n\n")

    if delete_dir_choice := input(f"\n\nIf App is not worth anymore, you can delete it now.\nDelete {folderName} folder? (Y/n)  > ") == "Y":
        folder_removal(folderName)

    print(f"\n\nThank you!\n\n")

def folder_removal(folderName):
    currentDir = os.getcwd()
    if str(currentDir.find(folderName)) != '-1':
        os.chdir("../")
    if os.path.exists(folderName) and os.path.isdir(folderName):
        print(f"\n\t> Removal of folder '{folderName}' ... ", end="")
        shutil.rmtree(f"{folderName}")
        print("DONE\n\n")
    else:
        print(f"\n\t> Removal Failed: folder '{folderName}' is NOT present\n\n")

def project_creation():
    folderName = folder_creation()
    work_folders_creation(folderName)
    work_files_creation(folderName)
    files_strip()
    folder_management(folderName)

def project_removal():
    projectList = list(os.listdir())
    projectName = ""
    dir_count = project_list(projectList)
    if dir_count > 0:
        while not (projectName in projectList):
            os.system("cls")
            for project in projectList:
                if os.path.isdir(project):
                    print(f"\t - {project}")
            projectName = input("\n\tName of the project to delete > ")
        folder_removal(projectName)
    else:
        print(f"\n\t> Project folder is EMPTY - Nothing to delete\n\n")

def project_list(projectList):
    dir_count = 0
    for project in projectList:
        if os.path.isdir(project):
            dir_count += 1
    return dir_count

def main():
    projectList = list(os.listdir())
    opChoice = ""
    while not (opChoice in ["D", "C"]):
        os.system("cls")
        dir_count = project_list(projectList)
        opChoice = input("\n\t\t> Delete ( D ) or Create New ( C ) project ? > ")
    if opChoice == 'C':
        project_creation()
    else:
        project_removal()

if __name__ == "__main__":
    main()


