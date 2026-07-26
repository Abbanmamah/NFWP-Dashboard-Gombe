import json


def merge_records(old_records, new_records, key="_uuid"):
    """
    Merge old JSON data with new Kobo data without duplicates.
    """

    existing = {
        record.get(key): record
        for record in old_records
        if record.get(key)
    }

    for record in new_records:
        record_key = record.get(key)

        if record_key not in existing:
            old_records.append(record)

    return old_records


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)