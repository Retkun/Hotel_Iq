import sqlite3

def inspect_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
        return

    print(f"\n📦 Database: {db_path}")
    print("=" * 60)

    for (table_name,) in tables:
        print(f"\n🗂️ Table: {table_name}")

        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        print(f"🔹 Columns: {', '.join(column_names)}")

        # Get number of rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        print(f"🔢 Number of rows: {row_count}")

        # Get last 2 rows
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY ROWID DESC LIMIT 2;")
        last_rows = cursor.fetchall()

        if last_rows:
            print("🧾 Last 2 rows:")
            for row in last_rows:
                print("   ", row)
        else:
            print("⚠️ Table is empty.")

    conn.close()

# Run the function
inspect_database("../hotels.db")
