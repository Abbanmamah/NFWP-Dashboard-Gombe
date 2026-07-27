import os
import json
import sqlite3
import requests
from datetime import datetime

from utils.kobo_config import *

from utils.github_upload import upload_file

DB = "data/nfwp.db"
SYNC_FILE = "data/last_sync.json"

MEMBERSHIP_UPDATE_FILE = "data/membership_updates.json"
SAVINGS_UPDATE_FILE = "data/savings_updates.json"

PAGE_SIZE = 100


def load_last_sync():
    if not os.path.exists(SYNC_FILE):
        return {
            "membership": "",
            "savings": "",
            "membership_added": 0,
            "savings_added": 0
        }

    with open(SYNC_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last_sync(sync_data):
    with open(SYNC_FILE, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=4)


def save_updates(filename, records):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            records,
            f,
            indent=4,
            ensure_ascii=False
        )


def insert_records(table, records):

    conn = sqlite3.connect(DB, timeout=30)
    cursor = conn.cursor()

    added = 0

    try:

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

    finally:
        conn.close()

    return added


def sync_asset(server, asset_id, token, table, last_sync=""):

    url = f"{server}/api/v2/assets/{asset_id}/data/"

    headers = {
        "Authorization": f"Token {token}"
    }

    start = 0
    total_added = 0
    all_new_records = []

    while True:

        params = {
            "limit": PAGE_SIZE,
            "start": start
        }

        if last_sync:
            params["query"] = json.dumps({
                "_submission_time": {
                    "$gt": last_sync
                }
            })

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        page = response.json().get("results", [])

        if not page:
            break

        all_new_records.extend(page)

        added = insert_records(table, page)

        total_added += added

        print(
            f"{table}: downloaded {len(page)} records, added {added}"
        )

        if len(page) < PAGE_SIZE:
            break

        start += PAGE_SIZE

    return total_added, all_new_records


def sync_kobo():

    sync_info = load_last_sync()

    membership_added, membership_records = sync_asset(
        KOBO_SERVER,
        MEMBERSHIP_ASSET_ID,
        KOBO_API_TOKEN,
        "membership",
        sync_info.get("membership", "")
    )

    savings_added, savings_records = sync_asset(
        KOBO_SERVER,
        SAVINGS_ASSET_ID,
        KOBO_API_TOKEN,
        "savings",
        sync_info.get("savings", "")
    )

    # Save update files locally
    save_updates(
        MEMBERSHIP_UPDATE_FILE,
        membership_records
    )

    save_updates(
        SAVINGS_UPDATE_FILE,
        savings_records
    )

    # Upload update files to GitHub
    upload_file(
        MEMBERSHIP_UPDATE_FILE,
        "updates/membership_updates.json"
    )

    upload_file(
        SAVINGS_UPDATE_FILE,
        "updates/savings_updates.json"
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