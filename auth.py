import json
import hashlib
import os

# Persistent folder in AppData
APP_DIR = os.path.join(os.environ["APPDATA"], "SafeNotes")
os.makedirs(APP_DIR, exist_ok=True)

USER_FILE = os.path.join(APP_DIR, "users.json")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USER_FILE):
        return {"users": {}}

    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {"users": {}}


def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)


def user_exists(username):
    data = load_users()
    return username in data["users"]


def register_user(username, password):
    data = load_users()
    data["users"][username] = hash_password(password)
    save_users(data)


def verify_user(username, password):
    data = load_users()
    return data["users"].get(username) == hash_password(password)
