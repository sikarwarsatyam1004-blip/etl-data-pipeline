import os
import json
import pandas as pd
import psycopg2

csv_file = "/opt/airflow/data/processed/cleaned_orders.csv"
metrics_file = "/opt/airflow/data/processed/etl_metrics.json"

df = pd.read_csv(csv_file)

print("Rows ready to load:")
print(df.shape)

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

print("Connected to PostgreSQL successfully!")


cursor = connection.cursor()

try:
    cursor.execute("TRUNCATE TABLE orders;")

    print("Existing orders cleared.")

    with open(csv_file, "r", encoding="utf-8") as file:
        cursor.copy_expert(
            """
            COPY orders 
            FROM STDIN
            WITH CSV HEADER
            """,
            file
        )

    connection.commit()

    print("Data loaded successfully!")

    loaded_rows = len(df)

    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as file:
            metrics = json.load(file)
    else:
        metrics = {}

    metrics["loaded_rows"] = loaded_rows

    with open(metrics_file, "w") as file:
        json.dump(metrics, file, indent=4)

    print(f"Loaded rows: {loaded_rows}")

except Exception as error:
    connection.rollback()

    print("Data load failed!")
    print(error)

    raise

finally:
    cursor.close()
    connection.close()