import os
import json
import sqlite3
import requests
from datetime import datetime

from utils.kobo_config import *

DB = "data/nfwp.db"
SYNC_FILE = "data/last_sync.json"


def load_last_sync():
    if not os.path.exists(SYNC_FILE):
        return {
            "membership": "",
            "savings": ""
        }

    with open(SYNC_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last_sync(sync_data):
    with open(SYNC_FILE, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=4)


def download_kobo_data(server, asset_id, token, last_sync=""):

    url = f"{server}/api/v2/assets/{asset_id}/data/"

    headers = {
        "Authorization": f"Token {token}"
    }

    params = {}

    if last_sync:
        params["query"] = json.dumps({
            "_submission_time": {
                "$gt": last_sync
            }
        })

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    return response.json().get("results", [])


def insert_records(table, records):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    added = 0

    for record in records:

        record_id = (
            record.get("_uuid")
            or record.get("_id")
            or record.get("uuid")
        )

        if not record_id:
            continue

        cursor.execute(
            f"SELECT id FROM {table} WHERE id=?",
            (record_id,)
        )

        if cursor.fetchone():
            continue

        cursor.execute(
            f"""
            INSERT INTO {table}(id,data)
            VALUES(?,?)
            """,
            (
                record_id,
                json.dumps(record)
            )
        )

        added += 1

    conn.commit()
    conn.close()

    return added


def sync_kobo():

    sync_info = load_last_sync()

    new_membership = download_kobo_data(
        KOBO_SERVER,
        MEMBERSHIP_ASSET_ID,
        KOBO_API_TOKEN,
        sync_info["membership"]
    )

    new_savings = download_kobo_data(
        KOBO_SERVER,
        SAVINGS_ASSET_ID,
        KOBO_API_TOKEN,
        sync_info["savings"]
    )

    membership_added = insert_records(
        "membership",
        new_membership
    )

    savings_added = insert_records(
        "savings",
        new_savings
    )

    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    sync_data = {
        "membership": now,
        "savings": now,
        "membership_added": membership_added,
        "savings_added": savings_added
    }

    save_last_sync(sync_data)

    return sync_data