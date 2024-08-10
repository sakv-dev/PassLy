import os
import subprocess
import sys
import random
import string
import cryptography.fernet as cf
import stdiomask
from datetime import datetime
import pyfiglet

# Couleurs ANSI
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generate_master_password():
    try:
        key = cf.Fernet.generate_key()
        with open('master.key', 'wb') as master_password_writer:
            master_password_writer.write(key)
    except Exception as e:
        print(f"{Colors.FAIL}Error generating master password: {e}{Colors.ENDC}")
        sys.exit()

def load_master_password():
    try:
        return open('./master.key', 'rb').read()
    except Exception as e:
        print(f"{Colors.FAIL}Error loading master password: {e}{Colors.ENDC}")
        sys.exit()

def create_vault():
    try:
        vault = open('./vault.txt', 'wb')
        vault.close()
    except Exception as e:
        print(f"{Colors.FAIL}Error creating vault: {e}{Colors.ENDC}")
        sys.exit()

def encrypt_data(data):
    try:
        f = cf.Fernet(load_master_password())
        with open('./vault.txt', 'rb') as vault_reader:
            encrypted_data = vault_reader.read()
        if not encrypted_data:
            return f.encrypt(data.encode())
        else:
            decrypted_data = f.decrypt(encrypted_data).decode()
            # Ajout de la nouvelle entrée correctement formatée
            new_data = decrypted_data.strip() + "\n---\n" + data.strip()
            return f.encrypt(new_data.encode())
    except Exception as e:
        print(f"{Colors.FAIL}Error encrypting data: {e}{Colors.ENDC}")
        sys.exit()

def decrypt_data(encrypted_data):
    try:
        f = cf.Fernet(load_master_password())
        return f.decrypt(encrypted_data)
    except Exception as e:
        print(f"{Colors.FAIL}Error decrypting data: {e}{Colors.ENDC}")
        sys.exit()

def append_new_password():
    print()
    name = input(f"{Colors.OKGREEN}Please enter a name for this entry > {Colors.ENDC}")
    user_name = input(f"{Colors.OKGREEN}Please enter a username > {Colors.ENDC}")
    password = stdiomask.getpass(prompt=f"{Colors.OKGREEN}Please enter the password > {Colors.ENDC}", mask='*')
    website = input(f"{Colors.OKGREEN}Please enter the website link > {Colors.ENDC}")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at = created_at
    print()
    
    entry = (
        f"{Colors.OKCYAN}Name:{Colors.ENDC} {name}\n"
        f"{Colors.OKCYAN}Username:{Colors.ENDC} {user_name}\n"
        f"{Colors.OKCYAN}Password:{Colors.ENDC} {password}\n"
        f"{Colors.OKCYAN}Website:{Colors.ENDC} {website}\n"
        f"{Colors.OKCYAN}Created At:{Colors.ENDC} {created_at}\n"
        f"{Colors.OKCYAN}Updated At:{Colors.ENDC} {updated_at}"
    )
    
    encrypted_data = encrypt_data(entry)
    try:
        with open("./vault.txt", 'wb') as vault_writer:
            vault_writer.write(encrypted_data)
    except Exception as e:
        print(f"{Colors.FAIL}Error saving data: {e}{Colors.ENDC}")
        sys.exit()

def read_passwords():
    try:
        with open('vault.txt', 'rb') as passwords_reader:
            encrypted_data = passwords_reader.read()
        print()
        print(decrypt_data(encrypted_data).decode())
    except Exception as e:
        print(f"{Colors.FAIL}Error reading passwords: {e}{Colors.ENDC}")
        sys.exit()

def search_password_by_name(name_to_search):
    try:
        with open('vault.txt', 'rb') as passwords_reader:
            encrypted_data = passwords_reader.read()
        decrypted_data = decrypt_data(encrypted_data).decode()

        # Split the decrypted data into individual entries
        entries = decrypted_data.split("\n---\n")  # Using the separator to split records
        found_entries = []

        # Normalize the name_to_search by stripping spaces and converting to lowercase
        normalized_name_to_search = name_to_search.strip().lower()

        for entry in entries:
            lines = entry.split("\n")
            for line in lines:
                if line.startswith("Name: "):
                    # Normalize the name in the entry for comparison
                    entry_name = line[6:].strip().lower()
                    if entry_name == normalized_name_to_search:
                        found_entries.append(entry)
                        break  # Stop searching once the correct entry is found

        if found_entries:
            print("\n---\n".join(found_entries))
        else:
            print(f"{Colors.WARNING}No credentials found with the name '{name_to_search}'.{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.FAIL}Error searching passwords: {e}{Colors.ENDC}")
        sys.exit()

def generate_new_password(password_length):
    random_string = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(random_string) for i in range(password_length))
    print()
    print(f'{Colors.OKBLUE}Here is your new password: {new_password}{Colors.ENDC}')
    
# Main Program
subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

logo = pyfiglet.figlet_format("PassLy", font="slant")
print(logo)
print(f'{Colors.FAIL}Created by Stalka https://github.com/sakv-dev')
print(f"{Colors.BOLD}{Colors.OKGREEN}Welcome to your password manager!{Colors.ENDC}")
print()

while True:
    if os.path.exists('./vault.txt') and os.path.exists('./master.key'):
        print(f'{Colors.OKBLUE}' + '-' * 50 + f'{Colors.ENDC}')
        print(f'{Colors.OKGREEN}Choose one of the following options:{Colors.ENDC}')
        print(f'{Colors.OKCYAN}1- Save credentials{Colors.ENDC}')
        print(f'{Colors.OKCYAN}2- Generate a new password{Colors.ENDC}')
        print(f'{Colors.OKCYAN}3- Display all stored info{Colors.ENDC}')
        print(f'{Colors.OKCYAN}4- Search for specific credentials{Colors.ENDC}')
        print(f'{Colors.FAIL}0- Quit the program{Colors.ENDC}')
        print(f'{Colors.OKBLUE}' + '-' * 50 + f'{Colors.ENDC}')
        
        user_choice = input(f"{Colors.BOLD}What would you like to do? (1/2/3/4/0) {Colors.ENDC}")
        
        if user_choice == '1':
            append_new_password()
        elif user_choice == '2':
            password_length = input(f"{Colors.OKGREEN}What length do you want for the password? {Colors.ENDC}")
            if password_length.isdigit():
                generate_new_password(int(password_length))
            else:
                print(f"{Colors.FAIL}Please enter a number next time!{Colors.ENDC}")
        elif user_choice == '3':
            read_passwords()
        elif user_choice == '4':
            name_to_search = input(f"{Colors.OKGREEN}Please enter the name of the credentials to search for > {Colors.ENDC}")
            search_password_by_name(name_to_search)
        elif user_choice == '0':
            print(f"{Colors.FAIL}Exiting the program. Goodbye!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}The selected option does not exist{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Generating a master password and vault{Colors.ENDC}")
        generate_master_password()
        create_vault()
        print(f"{Colors.OKGREEN}Generation completed, please restart the program.{Colors.ENDC}")
