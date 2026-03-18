import sqlite3
import pandas as pd
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
OUTPUT_PATH = os.path.join(BASE_DIR, "output_pandas.csv")

def run_pandas_script():
    conn = None

    try:
        logging.info("Starting Pandas solution process...")

        # Check DB existence
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database not found at: {DB_PATH}")

        logging.info(f"Connecting to database: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)

    
        # Load Tables
        logging.info("Reading tables into DataFrames...")

        customers = pd.read_sql("SELECT * FROM Customer", conn)
        orders = pd.read_sql("SELECT * FROM Orders", conn)
        items = pd.read_sql("SELECT * FROM Items", conn)
        sales = pd.read_sql("SELECT * FROM Sales", conn)

        logging.info(f"Customers rows: {len(customers)}")
        logging.info(f"Orders rows: {len(orders)}")
        logging.info(f"Items rows: {len(items)}")
        logging.info(f"Sales rows: {len(sales)}")

        conn.close()

        # Transformations
        logging.info("Merging tables...")

        df = (
            sales
            .merge(orders, on="order_id", how="left")
            .merge(customers, on="customer_id", how="left")
            .merge(items, on="item_id", how="left")
        )

        logging.info(f"Data after merge: {df.shape}")

        # Filter age
        logging.info("Filtering customers aged 18–35...")
        df = df[(df["age"] >= 18) & (df["age"] <= 35)]
        logging.info(f"Rows after age filter: {len(df)}")

        # Remove NULL quantity
        logging.info("Removing NULL quantities...")
        df = df[df["quantity"].notna()]
        logging.info(f"Rows after NULL filter: {len(df)}")

        # Aggregation
        logging.info("Aggregating quantities...")

        result = (
            df.groupby(
                ["customer_id", "age", "item_name"],
                as_index=False
            )["quantity"]
            .sum()
        )

        logging.info(f"Rows after aggregation: {len(result)}")

        # Remove zero values
        result = result[result["quantity"] > 0]

        # Convert to int
        result["quantity"] = result["quantity"].astype(int)

        # Rename columns
        result.columns = ["Customer", "Age", "Item", "Quantity"]

        # Save Output
        logging.info(f"Writing output to CSV: {OUTPUT_PATH}")

        result.to_csv(OUTPUT_PATH, sep=";", index=False)

        logging.info("Pandas CSV generated successfully.")

    except FileNotFoundError as e:
        logging.error(e)

    except pd.errors.DatabaseError as e:
        logging.error(f"Pandas DB error: {e}")

    except KeyError as e:
        logging.error(f"Column missing: {e}")

    except IOError as e:
        logging.error(f"File write error: {e}")

    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

        logging.info("Pandas solution process completed.")

if __name__ == "__main__":
    run_pandas_script()
