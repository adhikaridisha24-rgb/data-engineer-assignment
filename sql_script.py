import sqlite3
import csv
import logging
import os
import sys

LOG_FILE = "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
OUTPUT_FILE = os.path.join(BASE_DIR, "output_sql.csv")

SQL_QUERY = """
SELECT
    c.customer_id   AS Customer,
    c.age           AS Age,
    i.item_name     AS Item,
    CAST(SUM(s.quantity) AS INTEGER) AS Quantity
FROM Sales s
JOIN Orders o   ON s.order_id = o.order_id
JOIN Customer c ON o.customer_id = c.customer_id
JOIN Items i    ON s.item_id = i.item_id
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
    conn = None

    try:
        logging.info("Starting SQL solution process...")

        # Check if DB exists
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database not found at path: {DB_PATH}")

        logging.info(f"Connecting to database: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        logging.info("Executing SQL query...")
        cursor.execute(SQL_QUERY)

        rows = cursor.fetchall()
        logging.info(f"Query executed successfully. Rows fetched: {len(rows)}")

        if not rows:
            logging.warning("No data returned from query.")

        logging.info(f"Writing results to CSV: {OUTPUT_FILE}")

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Customer", "Age", "Item", "Quantity"])
            writer.writerows(rows)

        logging.info("CSV file generated successfully.")

    except sqlite3.OperationalError as e:
        logging.error(f"SQL error occurred: {e}")

    except FileNotFoundError as e:
        logging.error(e)

    except IOError as e:
        logging.error(f"File write error: {e}")

    except Exception as e:
        logging.exception(f"Unexpected error occurred: {e}")

    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

        logging.info("SQL solution process completed.")


if __name__ == "__main__":
    run_sql_solution()
