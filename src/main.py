import subprocess
import sys
import logging

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    logging.info("ETL pipeline started")

    print("\n===== ETL PIPELINE STARTED =====")

    print("\n1. Transforming data...")
    subprocess.run(
        [sys.executable, "src/transform_data.py"],
        check=True
    )
    logging.info("Transformation completed")

    print("\n2. Verifying data...")
    subprocess.run(
        [sys.executable, "src/verify_data.py"],
        check=True
    )
    logging.info("Data verification completed")

    print("\n3. Loading data into PostgreSQL...")
    subprocess.run(
        [sys.executable, "src/load_data.py"],
        check=True
    )
    logging.info("Data loaded into PostgreSQL successfully")

    logging.info("ETL pipeline completed successfully")

    print("\n===== ETL PIPELINE COMPLETED SUCCESSFULLY =====")

except Exception as error:
    logging.exception("ETL pipeline failed")
    print(f"\nETL PIPELINE FAILED: {error}")
    sys.exit(1)