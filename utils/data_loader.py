import sqlite3
import json

DB = "data/nfwp.db"


def load_membership_data():

    print("Loading membership from SQLite...")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM membership")

    rows = cursor.fetchall()

    conn.close()

    membership = [
        json.loads(row[0])
        for row in rows
    ]

    print(f"Loaded {len(membership):,} membership records")

    return membership


def load_savings_data():

    print("Loading savings from SQLite...")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM savings")

    rows = cursor.fetchall()

    conn.close()

    savings = [
        json.loads(row[0])
        for row in rows
    ]

    print(f"Loaded {len(savings):,} savings records")

    return savings