import sqlite3
import csv

DB_PATH = "database.db"
OUTPUT_FILE = "output_sql.csv"

SQL_QUERY = """
SELECT
    c.customer_id   AS Customer,
    c.age           AS Age,
    i.item_name     AS Item,
    CAST(SUM(s.quantity) AS INTEGER) AS Quantity
FROM sales s
JOIN orders o   ON s.order_id = o.order_id
JOIN customer c ON o.customer_id = c.customer_id
JOIN items i    ON s.item_id = i.item_id
WHERE
    c.age BETWEEN 18 AND 35
    AND s.quantity IS NOT NULL
GROUP BY
    c.customer_id, c.age, i.item_name
HAVING
    SUM(s.quantity) > 0
ORDER BY
    c.customer_id, i.item_name;
"""

def run_sql_solution():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(SQL_QUERY)
        rows = cursor.fetchall()

        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Customer", "Age", "Item", "Quantity"])
            writer.writerows(rows)

        print("SQL solution CSV generated successfully.")

    except Exception as e:
        print("Error in SQL solution:", e)

    finally:
        conn.close()

if __name__ == "__main__":
    run_sql_solution()
