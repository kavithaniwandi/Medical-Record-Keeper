import json
from datetime import datetime

DATA_FILE = "data.json"

def load_records():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_records(records):
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=4)

def add_record(records, record):
    records.append(record)
    save_records(records)

def delete_record(records, index):
    if 0 <= index < len(records):
        records.pop(index)
        save_records(records)
        return True
    return False

def search_records(records, keyword):
    return [r for r in records if keyword.lower() in r['type'].lower() or keyword.lower() in r['description'].lower()]
