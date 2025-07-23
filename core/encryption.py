import hashlib
import base64
from cryptography.fernet import Fernet

def derive_key(master_password: str) -> bytes:
    sha = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def get_fernet(master_password: str) -> Fernet:
    return Fernet(derive_key(master_password))