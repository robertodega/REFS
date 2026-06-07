import os
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("====================================")
    print("     Python Script Launcher v1.0     ")
    print("====================================")

def script_start():
    print_header()
    print("\nAvailable scripts:\n\n")
    
    files = [p for p in Path('.').iterdir() if p.is_file()]
    file_count = 0
    for file in files:
        file_count += 1
        print(f"\t> [ {file_count} ] {file}")
    print("\n\t> [ 0 ] Exit\n")

def script_execution(file):

    while True:
        clear_screen()
        print_header()
        print(f"\nSelected script: {file}\n")
        op_choice = input("Type\n\n\t[ 1 ] for content READ\n\t[ 2 ] for content EXECUTION\n\n")
        
        if op_choice == '1':
            with open(file, 'r') as f:
                code = f.read()
                print(f"--- Content of {file} ---\n")
                print(code)
                continue_input = input("---Type any key to return to menu --- ")
                break

        elif op_choice == '2':
            print(f"Running {file}...\n")
            #   os.system(f'python "{file}"')                                       #   SCRIPT EXECUTION SECTION
            print("\nScript finished. Returning to menu...\n")
            continue_input = input("---Type any key to return to menu --- ")
            break

def main():
    while True:
        script_start()
        choice = input("Enter the number of the script to run (or 0 to exit): ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                print("Exiting...")
                break
            files = [p for p in Path('.').iterdir() if p.is_file()]
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                script_execution(selected_file)
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Please enter a valid number.")
    
    clear_screen()

if __name__ == "__main__":
    main()
