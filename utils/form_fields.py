from utils.kobo_api import get_submissions
from config.forms import OLD_SAVINGS

records = get_submissions(OLD_SAVINGS, limit=1)

if records:
    with open("old_savings_fields.txt", "w", encoding="utf-8") as f:
        for field in records[0].keys():
            f.write(field + "\n")

    print("✅ Old Savings fields exported successfully!")
else:
    print("❌ No records found.")