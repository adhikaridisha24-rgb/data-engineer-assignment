import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER
)
""")

# Insert sample data
cursor.executemany(
    "INSERT INTO Customer VALUES (?, ?)",
    [(1, 21), (2, 23), (3, 35)]
)

cursor.executemany(
    "INSERT INTO Items VALUES (?, ?)",
    [(1, 'x'), (2, 'y'), (3, 'z')]
)

cursor.executemany(
    "INSERT INTO Orders VALUES (?, ?)",
    [
        (101, 1), (102, 1),
        (201, 2),
        (301, 3), (302, 3)
    ]
)

cursor.executemany(
    "INSERT INTO Sales VALUES (?, ?, ?, ?)",
    [
        (1, 101, 1, 5),
        (2, 102, 1, 5),
        (3, 101, 2, None),
        (4, 101, 3, None),
        (5, 201, 1, 1),
        (6, 201, 2, 1),
        (7, 201, 3, 1),
        (8, 301, 3, 1),
        (9, 302, 3, 1)
    ]
)

conn.commit()
conn.close()

print("Database and tables created successfully.")
