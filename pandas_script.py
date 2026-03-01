import sqlite3
import pandas as pd
import os

def run_pandas_script():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "database.db")
        output_path = os.path.join(base_dir, "pandas_output.csv")

        conn = sqlite3.connect(db_path)

        # Read tables
        customers = pd.read_sql("SELECT * FROM Customer", conn)
        orders = pd.read_sql("SELECT * FROM Orders", conn)
        items = pd.read_sql("SELECT * FROM Items", conn)
        sales = pd.read_sql("SELECT * FROM Sales", conn)

        conn.close()

        # Join tables
        df = (
            sales
            .merge(orders, on="order_id", how="left")
            .merge(customers, on="customer_id", how="left")
            .merge(items, on="item_id", how="left")
        )

        # Filter age group
        df = df[(df["age"] >= 18) & (df["age"] <= 35)]

        # Ignore NULL quantities (not purchased)
        df = df[df["quantity"].notna()]

        # Aggregate quantities
        result = (
            df.groupby(
                ["customer_id", "age", "item_name"],
                as_index=False
            )["quantity"]
            .sum()
        )

        # Remove zero totals
        result = result[result["quantity"] > 0]

        # Convert to int
        result["quantity"] = result["quantity"].astype(int)

        # Rename columns to match spec
        result.columns = ["Customer", "Age", "Item", "Quantity"]

        # Save CSV
        result.to_csv(output_path, sep=";", index=False)

        print("Pandas CSV generated successfully.")

    except Exception as e:
        print("Error in Pandas solution:", e)

if __name__ == "__main__":
    run_pandas_script()
