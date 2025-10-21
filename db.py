import json
DB_FILE = "products.json"

def load_products():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_products(products):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)
products = load_products()