from utils.kobo_config import *
from utils.kobo_sync import download_kobo_data

membership = download_kobo_data(
    KOBO_SERVER,
    MEMBERSHIP_ASSET_ID,
    KOBO_API_TOKEN,
)

print(f"Membership Records: {len(membership)}")

savings = download_kobo_data(
    KOBO_SERVER,
    SAVINGS_ASSET_ID,
    KOBO_API_TOKEN,
)

print(f"Savings Records: {len(savings)}")