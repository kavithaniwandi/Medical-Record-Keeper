from record_manager import load_records, save_records, add_record, delete_record, search_records
from datetime import datetime

def input_record():
    record = {}
    record['date'] = input("Enter date (YYYY-MM-DD): ")
    record['type'] = input("Type (checkup/medication/prescription): ")
    record['description'] = input("Description: ")
    record['doctor'] = input("Doctor's name (optional): ")
    return record

def display_records(records):
    if not records:
        print("No records found.")
        return
    for i, record in enumerate(records):
        print(f"\nRecord #{i+1}")
        for key, value in record.items():
            print(f"{key.capitalize()}: {value}")

def main():
    records = load_records()

    while True:
        print("\nCaremint - Medical Record Keeper")
        print("1. Add record")
        print("2. View all records")
        print("3. Search records")
        print("4. Delete a record")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            new_record = input_record()
            add_record(records, new_record)
            print("✅ Record added.")
        elif choice == '2':
            display_records(records)
        elif choice == '3':
            keyword = input("Enter keyword to search: ")
            results = search_records(records, keyword)
            display_records(results)
        elif choice == '4':
            display_records(records)
            try:
                index = int(input("Enter record number to delete: ")) - 1
                if delete_record(records, index):
                    print("✅ Record deleted.")
                else:
                    print("⚠️ Invalid number.")
            except ValueError:
                print("❌ Please enter a valid number.")
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
