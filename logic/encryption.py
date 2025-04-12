import hashlib
from cryptography.fernet import Fernet
from utils.key import generate_key, load_key

# 🔐 Generate the key once if not exists
generate_key()

# 🔑 Load the existing key
cipher = Fernet(load_key())

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(cipher_text):
    try:
        return cipher.decrypt(cipher_text.encode()).decode()
    except Exception:
        return None
