import os
from cryptography.fernet import Fernet

KEY_PATH = "secret.key"

def generate_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)

def load_key():
    return open(KEY_PATH, "rb").read()
