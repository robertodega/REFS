import os
import subprocess, os
import secrets
from pathlib import Path

def clear_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)     

def print_header():
    clear_screen()
    print("====================================")
    print("     Python Secret Key Generator    ")
    print("====================================")

def script_start():
    print_header()
    
def secret_key_generation(choice):
    secret_key = ""
    if choice == 1:
        secret_key = f"{secrets.token_hex(32)} ( whith encryption format token_hex(32) )"
    elif choice == 2:
        secret_key = f"{secrets.token_urlsafe(32)} ( whith encryption format token_urlsafe(32) )"
    return secret_key

def main():
    secret_key = ""
    while True:
        script_start()
        choice = input("\n\n\tFor which situation is Secret Key needed? (or 0 to exit):\n\n\t\t> 1) SESSION Key or API\n\n\t\t> 2) Password Reset or URL parameters\n\n\t\t> ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                print("Exiting...")
                break
            
            if 1 <= choice <= 2:
                secret_key = secret_key_generation(choice)
                break
        else:
            print("Please enter a valid number.")
    
    if secret_key:
        print(f"\n\nSecret Key:\t{secret_key}\n\n")
    else:
        print(f"\n\nNo Secret Key has been generated\n\n")

if __name__ == "__main__":
    main()
