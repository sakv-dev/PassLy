Certainly! Here is the translation of your README into English:

# PassLy - Password Manager

## Description

**PassLy** is a simple and secure command-line (CLI) password manager. It allows you to store your credentials, generate strong passwords, and easily search for specific login information. The data is encrypted using the `cryptography.fernet` library.

## Features

- Generation of a secure master password to encrypt data.
- Saving credentials (name, username, password, website) in an encrypted vault.
- Generation of strong random passwords.
- Display of all stored credentials.
- Search for passwords by entry name.

## Installation

1. Clone the repository or download the project file.

   ```bash
   git clone https://github.com/sakv-dev/PassLy.git
   ```

2. Navigate to the project directory.

   ```bash
   cd PassLy
   ```

3. Install the required dependencies.

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If you don't have a `requirements.txt` file, here are the necessary dependencies you can install manually:

   ```bash
   pip install cryptography stdiomask pyfiglet
   ```

## Usage

1. Run the Python script to start the password manager.

   ```bash
   python3 passly.py
   ```

2. On the first run, a master password will be generated, and a vault will be created.

3. Follow the menu instructions to save credentials, generate new passwords, display stored information, or search for specific credentials.

## Example Commands

- Save credentials: choose option `1` in the main menu.
- Generate a new password: choose option `2`.
- Display all stored credentials: choose option `3`.
- Search for specific credentials by name: choose option `4`.
- Exit the program: choose option `0`.

## Note

The credentials are stored in an encrypted file named `vault.txt`, and the master password is stored in a `master.key` file. **Never share these files with others.**

## Author  
Created by Stalka. Find me on [GitHub](https://github.com/sakv-dev).