# app.py
import streamlit as st
import pandas as pd
from logic.encryption import hash_passkey, encrypt_data, decrypt_data
from logic.auth import init_auth_state, reset_attempts, reset_data, register_user, login_user
from storage.database import store_entry, retrieve_entry, load_data, clear_user_data
from utils.helpers import export_data, import_data

# --- Init ---
st.set_page_config(page_title="🔐 Secure Data Vault", layout="centered")
init_auth_state()

# --- Sidebar Navigation ---
st.sidebar.title("🔐 Secure Data Vault")
menu = ["Home", "Register", "Login", "Dashboard", "Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("🔍 Navigate", menu)

# --- Logout ---
if st.session_state.get("is_logged_in"):
    if st.sidebar.button("🚪 Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.is_authenticated = False
        st.success("✅ Logged out successfully!")

    # --- Admin Sidebar Tools ---
    if st.session_state.get("username") == "admin":
        st.sidebar.success("🔐 Logged in as Admin")
        st.sidebar.markdown("### 🧹 Admin Tools")

        if st.sidebar.button("🧹 Master Reset All Data"):
            confirm = st.sidebar.checkbox("✅ Yes, I confirm full data reset")
            if confirm:
                reset_data()
                st.sidebar.success("✅ All data has been wiped.")
            else:
                st.sidebar.warning("☝️ Please confirm before resetting.")

        if st.sidebar.checkbox("📋 View All Stored Entries (admin only)"):
            data = load_data()
            if data:
                df = pd.DataFrame(data).T
                st.sidebar.dataframe(df[["owner", "encrypted_text"]])
            else:
                st.sidebar.info("No entries found.")

# --- Export / Import ---
st.sidebar.markdown("### 📤 Export / Import")
if st.sidebar.button("📤 Export Data"):
    path = export_data()
    st.sidebar.success(f"Exported to {path}")

uploaded = st.sidebar.file_uploader("📁 Import JSON Data", type=["json"])
if uploaded:
    import_data(uploaded.name)
    st.sidebar.success("✅ Data imported!")

# --- HOME ---
if choice == "Home":
    st.title("🔐 Secure Data Encryption System")
    st.markdown("""
    - Encrypt & store secret data with a passkey.  
    - Decrypt only with the correct key.  
    - App clears after 3 failed attempts.
    """)

# --- REGISTER ---
elif choice == "Register":
    st.subheader("🆕 Register")
    new_user = st.text_input("Choose Username")
    new_pass = st.text_input("Choose Password", type="password")
    if st.button("Register"):
        if new_user and new_pass:
            if register_user(new_user, new_pass):
                st.success("✅ Registered successfully! You can now log in.")
            else:
                st.warning("⚠️ Username already exists.")
        else:
            st.warning("⚠️ All fields are required!")

# --- LOGIN ---
elif choice == "Login":
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, pw):
            st.session_state.is_logged_in = True
            st.session_state.username = user
            st.session_state.rerun_triggered = False
            st.session_state.failed_attempts = 0
            if user == "admin":
                st.session_state.is_authenticated = True  # Needed for admin views
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid credentials.")

# --- DASHBOARD ---
elif choice == "Dashboard":
    if st.session_state.get("is_logged_in"):
        st.subheader(f"👋 Welcome, {st.session_state.get('username')}")
        data = load_data()
        user_entries = {
            k: v for k, v in data.items()
            if v.get("owner") == st.session_state.get("username")
        }

        if user_entries:
            df = pd.DataFrame(user_entries).T
            st.dataframe(df[["encrypted_text"]])

            if st.button("🧹 Clear My Data"):
                clear_user_data(st.session_state["username"])
                st.success("✅ Your data has been cleared.")
                st.rerun()
        else:
            st.info("📭 Your dashboard is empty. Nothing to show.")
    else:
        st.warning("🚫 You must log in to access your dashboard.")

# --- STORE DATA ---
elif choice == "Store Data":
    if not st.session_state.get("is_logged_in"):
        st.warning("🚫 You must log in to store data.")
        st.stop()

    st.subheader("📂 Store Secure Data")
    username = st.session_state.get("username", "")
    st.markdown(f"👤 Logged in as: `{username}`")
    data = st.text_area("🔐 Enter Sensitive Data")
    passkey = st.text_input("🔑 Create a Passkey", type="password")

    if st.button("💾 Encrypt & Store"):
        if data and passkey:
            encrypted = encrypt_data(data)
            hashed = hash_passkey(passkey)
            store_entry(username, encrypted, hashed)
            st.success("✅ Data stored securely.")
            st.code(encrypted)
        else:
            st.warning("All fields are required!")

# --- RETRIEVE DATA ---
elif choice == "Retrieve Data":
    if not st.session_state.get("is_logged_in"):
        st.warning("🚫 You must log in to retrieve data.")
        st.stop()

    st.subheader("🔍 Retrieve Your Data")

    if st.session_state.get("failed_attempts", 0) >= 3 and not st.session_state.get("is_authenticated", False):
        if not st.session_state.get("rerun_triggered", False):
            st.session_state.rerun_triggered = True
            st.warning("🔒 Too many failed attempts. Redirecting to Login...")
            st.rerun()
        else:
            st.warning("🔐 Locked! Please go to Login Page to reauthorize.")
            st.stop()

    encrypted_text = st.text_area("🔒 Paste Encrypted Text")
    passkey = st.text_input("🔑 Enter Your Passkey", type="password")

    if st.button("🔓 Decrypt"):
        if encrypted_text and passkey:
            hashed = hash_passkey(passkey)
            entry = retrieve_entry(encrypted_text, hashed)

            if entry:
                decrypted = decrypt_data(encrypted_text)
                if decrypted:
                    st.success("✅ Decryption Successful")
                    st.code(decrypted)
                    reset_attempts()
                else:
                    st.error("❌ Decryption failed! Encrypted data or passkey may be incorrect.")
            else:
                st.session_state.failed_attempts += 1
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect credentials! Attempts left: {remaining}")
                if remaining == 0:
                    st.warning("🔐 Locked out! Please reauthorize.")
        else:
            st.warning("Both fields are required!")
