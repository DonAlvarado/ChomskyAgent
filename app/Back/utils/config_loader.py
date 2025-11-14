import json
import os

CONFIG_PATH = "app/Front/resources/config.json"

def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
