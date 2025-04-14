
# 🔐 Secure Data Vault – Streamlit App

A user-friendly encryption system built using **Python, Streamlit**, and **Fernet encryption** to securely store and retrieve sensitive data. This app includes authentication, password hashing, encrypted storage, admin dashboard, and beautiful UI.

---

## 🌟 Features

- 🔑 **User Authentication (Register / Login / Logout)**
- 🧠 **Password Hashing using `hashlib` (SHA-256)**
- 🔐 **Fernet Symmetric Encryption** (from `cryptography`)
- 📂 **Store Sensitive Data** using a custom passkey
- 🔍 **Retrieve Data** with decryption and failed attempt lock
- 📋 **User Dashboard** to view and manage stored entries
- 🧹 **Clear Individual Data** or perform **Admin Master Reset**
- 🗂️ **Import / Export JSON Data**
- 🎨 Custom UI with images, sidebar tools, and page backgrounds

---

## 🚀 How It Works

### 🔑 Password Security

- User passwords are **hashed using SHA-256** before saving (no plain text).
- Users are authenticated based on stored hash.

### 🛡️ Encryption System

- Uses **Fernet symmetric encryption** to encrypt user text.
- The encryption key is stored in `secret.key` and loaded at runtime.

### 🔒 Access Control

- 3 failed attempts to decrypt data locks the user out (requires re-login).
- Only logged-in users can store/retrieve data.
- Admin-only access to global data reset and viewing all records.

---

## 🧾 File Structure

```
secure-data-vault/
│
├── app.py                    # Main Streamlit app
├── secret.key                # Fernet encryption key (auto-generated)
│
├── logic/
│   ├── auth.py               # Registration, Login, Session Management
│   └── encryption.py         # Hashing & Fernet Encryption/Decryption
│
├── storage/
│   └── database.py           # Load/Store/Reset JSON Data
│
├── utils/
│   └── helpers.py            # Export/Import utility functions
│
├── assets/                   # UI images for pages & sidebar
│
├── users.json                # Stores registered users (hashed)
├── data.json                 # Encrypted data records
├── requirements.txt          # Streamlit, cryptography, pandas
└── README.md                 # This file
```

---

## 🧪 Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

### `requirements.txt`:

```txt
streamlit
cryptography
pandas
```

---

## 🖼️ UI Preview

| Page            | Preview                          |
|-----------------|----------------------------------|
| Home            | Info + Background image 🏠        |
| Register/Login  | Auth system with secure flow 🔐   |
| Store Data      | Encrypt and save text 📂          |
| Dashboard       | Manage your entries 📊           |
| Retrieve Data   | Decrypt using your passkey 🧠     |
| Admin Tools     | Master reset, global view 🧹      |

---

## ⚙️ Admin Functionality

- Login with username: `admin` and the registered password
- Access tools like:
  - 🔁 Master Reset All User Data
  - 📋 View All Stored Records (DataFrame)

---

## 📂 Data Security Approach

| Item              | Protection                        |
|-------------------|------------------------------------|
| User Password     | SHA-256 Hashed via `hashlib` 🔒     |
| Stored Data       | Fernet Encrypted using `secret.key`🛡️|
| Authentication    | Session state in Streamlit ✅       |

---

## ✨ Future Improvements

- 📅 Add timestamp for each entry
- 📊 Data Visualization (charts for usage)
- 📁 Upload/Download Encrypted Files
- 🧠 Add 2FA or email OTP for admin access

---

## 🙌 Built With

- [Streamlit](https://streamlit.io/)
- [Python Cryptography](https://cryptography.io/en/latest/)
- [Pandas](https://pandas.pydata.org/)

---

## 📢 Live Demo

👉 [Secure Data Vault Live on Streamlit](https://zi-security-vault.streamlit.app/)

