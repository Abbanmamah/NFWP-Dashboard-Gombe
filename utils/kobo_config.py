import os
from dotenv import load_dotenv

load_dotenv()

# Kobo
KOBO_SERVER = os.getenv("KOBO_SERVER")
KOBO_API_TOKEN = os.getenv("KOBO_API_TOKEN")

MEMBERSHIP_ASSET_ID = os.getenv("MEMBERSHIP_ASSET_ID")
SAVINGS_ASSET_ID = os.getenv("SAVINGS_ASSET_ID")

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")