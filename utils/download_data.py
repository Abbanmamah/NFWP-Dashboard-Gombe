import json
from utils.kobo_api import get_submissions
from config.forms import (
    OLD_MEMBERSHIP,
    NEW_MEMBERSHIP,
    OLD_SAVINGS,
    NEW_SAVINGS,
)

print("Downloading Membership Forms...")

old_members = get_submissions(OLD_MEMBERSHIP)
new_members = get_submissions(NEW_MEMBERSHIP)

print("Downloading Savings Forms... (This may take several minutes)")

old_savings = get_submissions(OLD_SAVINGS)
new_savings = get_submissions(NEW_SAVINGS)

print("Saving data...")

with open("data/membership.json", "w", encoding="utf-8") as f:
    json.dump(old_members + new_members, f)

with open("data/savings.json", "w", encoding="utf-8") as f:
    json.dump(old_savings + new_savings, f)

print("✅ Data saved successfully!")