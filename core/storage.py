import os
import json
import hashlib
from cryptography.fernet import Fernet
from core.encryption import get_fernet

VAULT_FILE = "vault.dat"
MASTER_FILE = "vault.enc"

def hash_master_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def store_master_hash(password: str):
    hashed = hash_master_password(password)
    with open(MASTER_FILE, "w") as f:
        json.dump({"master_hash": hashed}, f)

def verify_master_password(password: str) -> bool:
    if not os.path.exists(MASTER_FILE):
        return False
    try:
        with open(MASTER_FILE, "r") as f:
            data = json.load(f)
        stored_hash = data.get("master_hash")
        return hash_master_password(password) == stored_hash
    except Exception as e:
        print(f"Error verifying master password: {e}")
        return False

def load_data(fernet: Fernet):
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return {}

def save_data(fernet: Fernet, data: dict):
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)