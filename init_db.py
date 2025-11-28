import sqlite3
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(
    filename = "database.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sqlite_trace")

conn = sqlite3.connect("computer_store.db")  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()

def sql_trace(statement):
    logger.debug("SQL TRACE: %s", statement)

conn.set_trace_callback(sql_trace)

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

hashed_pass = generate_password_hash("LIVERPOOL")
populate_tables = f"""
    INSERT INTO users (username, password) VALUES 
    ('admin', '{hashed_pass}');

    INSERT INTO products (product_name, price, image) VALUES 
    ('Wireless Mouse', 25, 'mouse.jpg'),
    ('Mechanical Keyboard', 79, 'keyboard.jpg'),
    ('USB-C Charger', 19, 'charger.jpg'),
    ('Bluetooth Headphones', 59, 'headset.jpg'),
    ('27-inch Monitor', 229, 'monitor.jpg'),
    ('Laptop Stand', 34, 'stand.jpg'),
    ('Webcam HD', 49, 'camera.jpg'),
    ('Gaming Chair', 199, 'chair.jpg'),
    ('External SSD 1TB', 129, 'ssd.jpg'),
    ('Portable Speaker', 45, 'speaker.jpg'),
    ('RAM', 150, 'ram.jpg'),
    ('CPU', 250, 'cpu.jpg');
"""
cursor.executescript(populate_tables)
conn.commit()

conn.close()