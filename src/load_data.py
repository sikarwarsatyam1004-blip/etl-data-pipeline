import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

csv_file = "data/processed/cleaned_orders.csv"

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

except Exception as error:
    connection.rollback()

    print("Data load failed!")
    print(error)

    raise

finally:
    cursor.close()
    connection.close()