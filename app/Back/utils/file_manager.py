import os
import json

BASE_DIR = "app/Front/static/generated"

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def save_text(filename: str, text: str) -> str:
    ensure_dir(BASE_DIR)
    full = os.path.join(BASE_DIR, filename)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return full

def save_json(filename: str, data: dict) -> str:
    ensure_dir(BASE_DIR)
    full = os.path.join(BASE_DIR, filename)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return full

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
