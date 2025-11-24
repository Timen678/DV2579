import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect("computer_store.db")  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()

schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price INTEGER,
    image TEXT
);
"""

cursor.executescript(schema)
conn.commit()

populate_tables = """
INSERT INTO TABLE 

"""

conn.close()