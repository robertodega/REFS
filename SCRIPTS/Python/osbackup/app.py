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
