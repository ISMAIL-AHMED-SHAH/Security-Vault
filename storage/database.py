import json
import os

DATA_FILE = "storage/users.json"

# --- Load Data ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File exists but is empty or invalid JSON
        return {}

# --- Save Data ---
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Store Entry ---
def store_entry(username, encrypted_text, hashed_passkey):
    data = load_data()
    data[encrypted_text] = {
        "owner": username,
        "encrypted_text": encrypted_text,
        "passkey": hashed_passkey
    }
    save_data(data)

# --- Retrieve Entry ---
def retrieve_entry(encrypted_text, hashed_passkey):
    data = load_data()
    entry = data.get(encrypted_text)
    if entry and entry["passkey"] == hashed_passkey:
        return entry
    return None
