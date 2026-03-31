mkdir osbackup \
&& cd osbackup \
&& touch const.py functions.py app.py

- nano const.py

        rootFolder = "/home/roby/"
        containers = ["Multimedia", "Home"]
        foldersDebian = ["Documenti", "Immagini", "Musica"]
        foldersUbuntu = ["Documents", "Pictures", "Music"]
        support_disk_list = ["1", "2", "0"]
        support_disk_dict = {"1": "Toshiba", "2": "Hamlet"}
        support_disk_limit = {"Toshiba": 3, "Hamlet": 1}
        thunderbirdDebianPath = "/home/roby/.thunderbird/"
        thunderbirdUbuntuPath = "/home/roby/.var/app/org.mozilla.Thunderbird/.thunderbird"
        wwwPath = "/opt/lampp/htdocs/WWW/"

        separator = 40 * "*"
        title = " PYTHON OSBACKUP Utility "
        header = separator + title + separator
        goodbyeLabel = "\n\nThank you and goodbye!\n\n"
        supportChoiceLabel = (
            "\n\nChoose your disk ( 0 to exit ):\n\n\t1\tToshiba\n\t2\tHamlet\n\n\t> "
        )


- nano functions.py

        import os
        import shutil
        import datetime, time
        import const


        def clear_screen():
            os.system("cls" if os.name == "nt" else "clear")


        def print_goodbye():
            print(f"{const.goodbyeLabel}")


        def print_eleapsed_time(starttime, endtime, last=""):
            elapsed_minutes = int((endtime - starttime) / 60)
            if last:
                end_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(
                    f"\n\n{const.separator}\n >>> End time: {end_time} ( {elapsed_minutes} minutes )\n{const.separator}\n"
                )
            else:
                print(f" Done ( {elapsed_minutes} minutes ) ", end="")


        def print_header():
            clear_screen()
            print(f"{const.header}")


        def support_choice():
            while (
                support_disk := input(const.supportChoiceLabel)
            ) not in const.support_disk_list:
                print_header()
            if support_disk == "0":
                print_goodbye()
                exit(0)
            else:
                support_disk_name = const.support_disk_dict[support_disk]

            return support_disk_name


        def remove_old_backups(support_disk_name):
            remove_start_time = time.time()
            disk_limit = const.support_disk_limit[support_disk_name]
            support_disk_path_root = f"/media/roby/" + support_disk_name
            if not os.path.exists(support_disk_path_root):
                print(f"\n\t> Disk {support_disk_path_root} is NOT plugged in\n")
                exit(1)

            start_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n{const.separator}\n >>> Start time: {start_time}\n{const.separator}")

            support_disk_path = f"" + support_disk_path_root + "/HDBACKUP"
            if not os.path.exists(support_disk_path):
                print(f"\n\t> Creating {support_disk_path}...", end="")
                os.makedirs(support_disk_path)
            support_content = os.listdir(support_disk_path)
            present_folders_number = len(support_content)
            folders_to_delete = present_folders_number - disk_limit + 1

            if folders_to_delete:
                for i in range(folders_to_delete):
                    dir_to_remove = os.path.join(support_disk_path, support_content[i])
                    if os.path.isdir(dir_to_remove):
                        print(f"\n\t> Removing folder: {dir_to_remove} ... ", end="")
                        shutil.rmtree(dir_to_remove)
                        print("Done", end="")

                print(f"\n\t> Total old backup folders removal", end="")
                print_eleapsed_time(remove_start_time, time.time())

            return support_disk_path


        def folder_creation(support_disk_path):
            os.chdir(support_disk_path)
            print(f"\n\t> Navigated to {support_disk_path}", end="")

            backup_dir_name = datetime.datetime.now().strftime("%Y_%m_%d")
            backup_dir_path = os.path.join(support_disk_path, backup_dir_name)
            if not os.path.exists(backup_dir_path):
                os.makedirs(backup_dir_path)
                print(f"\n\t> Created new directory '{backup_dir_name}'", end="")

                os.chdir(backup_dir_path)
                print(f"\n\t> Navigated to {backup_dir_path}", end="")

            return backup_dir_path


        def folder_copy(backup_dir_path):
            folder_copy_start_time = time.time()

            if os.path.exists(const.rootFolder + const.foldersDebian[0]):
                ref_folders = const.foldersDebian
            else:
                ref_folders = const.foldersUbuntu

            for folder in ref_folders:  #   Documenti, Immagini, Musica
                folder_copy_time = time.time()
                print(f"\n\t> Copying {folder} ...", end="")
                shutil.copytree(
                    os.path.join(const.rootFolder, folder),
                    os.path.join(backup_dir_path, folder),
                )
                print_eleapsed_time(folder_copy_time, time.time())

            if os.path.exists(const.wwwPath):  #   WWW
                www_copy_time = time.time()
                print(f"\n\t> Copying WWW ...", end="")
                shutil.copytree(
                    os.path.join(const.wwwPath),
                    os.path.join(backup_dir_path, "WWW"),
                )
                print_eleapsed_time(www_copy_time, time.time())

            print(f"\n\t> Total folder copy", end="")
            print_eleapsed_time(folder_copy_start_time, time.time())

            return ref_folders


        def container_fill(ref_folders, backup_dir_path):
            container_fill_start_time = time.time()

            for container in const.containers:
                os.makedirs(container)
                print(f"\n\t> Created new container '{container}'", end="")

            print(f"\n\t> Moving '{ref_folders[1]}' to 'Multimedia' container", end="")
            shutil.move(  #   Multimedia
                os.path.join(backup_dir_path, ref_folders[1]),
                os.path.join(backup_dir_path, "Multimedia", ref_folders[1]),
            )
            print(f" Done", end="")

            print(f"\n\t> Moving '{ref_folders[2]}' to 'Multimedia' container", end="")
            shutil.move(  #   Multimedia
                os.path.join(backup_dir_path, ref_folders[2]),
                os.path.join(backup_dir_path, "Multimedia", ref_folders[2]),
            )
            print(f" Done", end="")

            print(f"\n\t> Copying '.bash_aliases' to 'Home' container", end="")
            shutil.copy(  #   bash_aliases
                os.path.join(const.rootFolder, ".bash_aliases"),
                os.path.join(backup_dir_path, "Home", ".bash_aliases"),
            )
            print(f" Done", end="")

            #   Thunderbird
            if os.path.exists(const.thunderbirdDebianPath):
                thunderbird_path = const.thunderbirdDebianPath
            else:
                thunderbird_path = const.thunderbirdUbuntuPath

            # continue_tag = input(
            #     f"\n\t> Please close Thunderbird app. Hit any button to continue..."
            # )
            # if continue_tag is not None:
            thuderbird_start_time = time.time()
            print(f"\n\t> Copying '.Thunderbird' to 'Home' container", end="")
            os.system("cp -r " + thunderbird_path + " " + backup_dir_path + "/Home")
            print_eleapsed_time(thuderbird_start_time, time.time())

            print(f"\n\t> Total containers fill", end="")
            print_eleapsed_time(container_fill_start_time, time.time())


- nano app.py

        import functions
        import time

        if __name__ == "__main__":

            start_time = time.time()

            functions.print_header()
            support_disk_name = functions.support_choice()
            support_disk_path = functions.remove_old_backups(support_disk_name)
            backup_dir_path = functions.folder_creation(support_disk_path)
            ref_folders = functions.folder_copy(backup_dir_path)
            functions.container_fill(ref_folders, backup_dir_path)
            functions.print_eleapsed_time(start_time, time.time(), True)
            functions.print_goodbye()



- python3 app.py

