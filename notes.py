import json
import os

# Persistent folder in AppData
APP_DIR = os.path.join(os.environ["APPDATA"], "SafeNotes")
os.makedirs(APP_DIR, exist_ok=True)

NOTES_FILE = os.path.join(APP_DIR, "notes.json")


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return {}

    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_notes(data):
    with open(NOTES_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_user_notes(username):
    data = load_notes()
    return data.get(username, [])


def add_note(username, title, content):
    data = load_notes()

    if username not in data:
        data[username] = []

    # If note with same title exists, update it instead of adding duplicate
    for note in data[username]:
        if note["title"] == title:
            note["content"] = content
            save_notes(data)
            return

    data[username].append({
        "title": title,
        "content": content
    })

    save_notes(data)


def delete_note(username, index):
    data = load_notes()
    if username in data and 0 <= index < len(data[username]):
        data[username].pop(index)
        save_notes(data)
