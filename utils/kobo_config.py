import os
from dotenv import load_dotenv

load_dotenv()

KOBO_SERVER = os.getenv("KOBO_SERVER")
KOBO_API_TOKEN = os.getenv("KOBO_API_TOKEN")

MEMBERSHIP_ASSET_ID = os.getenv("MEMBERSHIP_ASSET_ID")
SAVINGS_ASSET_ID = os.getenv("SAVINGS_ASSET_ID")