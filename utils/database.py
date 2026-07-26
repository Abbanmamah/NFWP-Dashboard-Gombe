import os
import requests

DB_PATH = "data/nfwp.db"

DB_URL = "https://github.com/Abbanmamah/NFWP-Dashboard-Gombe/releases/download/v1.0/nfwp.db"


def ensure_database():
    if os.path.exists(DB_PATH):
        return

    os.makedirs("data", exist_ok=True)

    print("Downloading database...")

    response = requests.get(DB_URL, stream=True)
    response.raise_for_status()

    with open(DB_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Database downloaded successfully.")