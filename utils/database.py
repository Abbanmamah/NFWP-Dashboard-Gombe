import os
import requests

DB_PATH = "data/nfwp.db"

DB_URL = "https://drive.google.com/uc?export=download&id=1QpryP5qrpO76ih3ztKMmGOq36VmCAU_H"

def ensure_database():

    if os.path.exists(DB_PATH):
        return

    os.makedirs("data", exist_ok=True)

    response = requests.get(DB_URL)

    response.raise_for_status()

    with open(DB_PATH, "wb") as f:
        f.write(response.content)