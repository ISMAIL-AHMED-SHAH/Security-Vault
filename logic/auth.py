import json
import os
import hashlib

USER_FILE = "users.json"

def hash_pass(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def register_user(username, password):
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    if username in users:
        return False  # user already exists

    users[username] = hash_pass(password)
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
    return True

def login_user(username, password):
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    return users.get(username) == hash_pass(password)

def init_auth_state():
    import streamlit as st
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False

def reset_attempts():
    import streamlit as st
    st.session_state.failed_attempts = 0

def reset_data():
    import os
    for file in ["data.json", "users.json"]:
        if os.path.exists(file):
            os.remove(file)
