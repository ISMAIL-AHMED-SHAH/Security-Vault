# logic/encryption.py
import hashlib
from cryptography.fernet import Fernet

# 🔑 Static Fernet Key (in real-world, store securely)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(cipher_text):
    try:
        return cipher.decrypt(cipher_text.encode()).decode()
    except Exception as e:
        return None
