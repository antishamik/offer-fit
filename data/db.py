import sqlite3
from sqlite3 import Error



# SQLite database connection
db_file = "event_database.db"

# Create SQLite table if not exists
def create_table():
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                customer_id INTEGER,
                event_type TEXT,
                timestamp TEXT,
                email_id INTEGER,
                clicked_link TEXT,
                product_id INTEGER,
                amount REAL
            )
        ''')

        connection.commit()
        cursor.close()

    except Error as e:
        print(f"Error creating table: {e}")