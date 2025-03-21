import sqlite3

DB_NAME = "fdam_database.db"

# ✅ Establish SQLite Connection
sqlite_conn = sqlite3.connect(DB_NAME, check_same_thread=False)
sqlite_cursor = sqlite_conn.cursor()

def initialize_db():
    try:
        sqlite_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            balance REAL DEFAULT 1000,
            last_login TEXT
        )
        """)

        sqlite_cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            fraud_status TEXT DEFAULT 'pending'
        )
        """)

        sqlite_cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            report_reason TEXT NOT NULL,
            reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )
        """)

        sqlite_conn.commit()
        print("✅ SQLite Database Initialized Successfully!")

    except Exception as e:
        print(f"❌ Error Initializing Database: {e}")

# Call the function to ensure the database is created on startup
initialize_db()
