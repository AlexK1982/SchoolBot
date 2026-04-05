import json
import os


USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def set_user_class(user_id, class_name):
    users = load_users()
    users[str(user_id)] = {"class_name": class_name}
    save_users(users)


def get_user_class(user_id):
    users = load_users()
    user_data = users.get(str(user_id))

    if not user_data:
        return None

    return user_data.get("class_name")