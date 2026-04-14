# Password Manager

Password Manager is a simple password manager built with Python and a graphical user interface using `tkinter`.
The application allows you to store account data, encrypt the password vault, generate random passwords, and edit or copy stored account information.

## Features

- Master password login and vault unlock
- Encrypted vault storage using `cryptography.Fernet`
- Save account entries with fields: account name, login, email, site URL, description, and password
- Generate strong passwords with uppercase, lowercase, numbers, and symbol options
- Edit and delete saved accounts
- Search accounts by name, email, URL, description, or password
- Copy account details to the clipboard

## Project Structure

- `main.py` — application entry point
- `core/` — application logic
  - `encryption.py` — key derivation and `Fernet` factory functions
  - `storage.py` — master password handling, loading and saving encrypted data
  - `password_generator.py` — password generator module
  - `error_codes.py` — error code constants and messages
- `ui/` — user interface
  - `gui.py` — main GUI window and user interaction logic
  - `images/` — graphical assets used in the interface
- `db/` — storage directory for encrypted data
  - `vault.enc` — file containing the master password hash
  - `vault.dat` — file containing the encrypted account vault (created on first run)

## Requirements

- Python 3.8 or newer
- `tkinter` (included with most Python installations)
- `cryptography`
- `Pillow`

## Installation

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install cryptography pillow
```

## Running the App

Start the application with:

```bash
python main.py
```

## Usage

1. Enter a master password to unlock the app.
2. If `db/vault.enc` does not exist or no master password is stored, the app will offer to create a new vault using the provided password.
3. Add account details in the `Add Account` tab.
4. Browse saved accounts in the `Accounts` tab.
5. Generate strong passwords in the `Generate Password` tab.
6. Use `Logout` to return to the unlock screen.

## Security

- The master password is stored as a SHA-256 hash in `db/vault.enc`.
- Account data is encrypted using a key derived from the master password and stored in `db/vault.dat`.

## Notes

- The UI uses an image asset at `ui/images/unlock.png` for the unlock button.
- If the vault files are corrupted, the application will attempt to handle errors and show a warning.


