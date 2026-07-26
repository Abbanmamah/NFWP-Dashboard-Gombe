import sqlite3
import json

DB = "data/nfwp.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS membership (
    id TEXT PRIMARY KEY,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS savings (
    id TEXT PRIMARY KEY,
    data TEXT
)
""")

# Import membership
print("Loading membership.json...")

with open("data/membership.json", "r", encoding="utf-8") as f:
    membership = json.load(f)

added = 0

for record in membership:
    record_id = record.get("_id") or record.get("_uuid")

    if record_id:
        cursor.execute(
            """
            INSERT OR REPLACE INTO membership
            VALUES (?,?)
            """,
            (
                str(record_id),
                json.dumps(record)
            )
        )
        added += 1

print(f"Imported {added:,} membership records")

# Import savings
print("Loading savings.json...")

with open("data/savings.json", "r", encoding="utf-8") as f:
    savings = json.load(f)

added = 0

for record in savings:
    record_id = record.get("_id") or record.get("_uuid")

    if record_id:
        cursor.execute(
            """
            INSERT OR REPLACE INTO savings
            VALUES (?,?)
            """,
            (
                str(record_id),
                json.dumps(record)
            )
        )
        added += 1

print(f"Imported {added:,} savings records")

conn.commit()
conn.close()

print("✅ SQLite database created successfully!")