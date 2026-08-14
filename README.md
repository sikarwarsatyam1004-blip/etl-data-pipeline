# ETL Data Pipeline

A production-style ETL (Extract, Transform, Load) pipeline built using Python, Pandas, and PostgreSQL.

The pipeline processes a raw customer orders dataset containing 100,000 records, performs data cleaning and validation, separates invalid records, and loads validated data into PostgreSQL.

## Pipeline Overview

Raw CSV
↓
Extract
↓
Transform & Clean
↓
Data Validation
↓
Valid / Rejected Records
↓
PostgreSQL

## Technologies Used

- Python
- Pandas
- PostgreSQL
- psycopg2
- python-dotenv
- pgAdmin 4
- Git


## Project Structure

```text
etl-pipeline/
├── data/
│   ├── raw/
│   │   └── customer_orders_raw_100k.csv
│   └── processed/
│       ├── cleaned_orders.csv
│       └── rejected_orders.csv
├── logs/
│   └── pipeline.log
├── src/
│   ├── inspect_data.py
│   ├── transform_data.py
│   ├── verify_data.py
│   ├── load_data.py
│   └── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md


## Pipeline Components

- `inspect_data.py` - Profiles the raw dataset, including missing values, duplicates, columns, and data types.
- `transform_data.py` - Cleans, validates, transforms, and separates valid and rejected records.
- `verify_data.py` - Performs final quality checks on processed data.
- `load_data.py` - Loads validated records into PostgreSQL using a transaction with commit and rollback protection.
- `main.py` - Runs the complete ETL pipeline in the correct sequence.




## Data Quality and Transformation Rules

The transformation stage applies multiple data-quality checks before loading records into PostgreSQL.

- Removes duplicate records.
- Handles missing email, city, state, age, unit price, payment method, and total amount values.
- Validates email addresses using a regular expression.
- Validates age and handles values outside the accepted range.
- Validates quantity and corrects invalid quantities.
- Validates unit prices to prevent invalid negative values.
- Validates discount percentages.
- Converts `order_date` into a proper datetime format and identifies invalid dates.
- Standardizes inconsistent order statuses such as `Complete` and `SHIPPED`.
- Recalculates `total_amount` using:

  `quantity × unit_price × (1 - discount_pct / 100)`

- Separates records that cannot safely pass validation into a rejected dataset.
- Adds a rejection reason to rejected records.

## Processing Results

Starting dataset:

- Raw records: **100,000**
- Duplicate records removed: **2,000**
- Records after duplicate removal: **98,000**
- Rejected records: **531**
- Valid records: **97,469**
- Final PostgreSQL records: **97,469**

Rejected records currently include:

- **411** records with invalid order dates.
- **120** records with invalid order statuses.

The rejected records are stored separately in `data/processed/rejected_orders.csv` for investigation instead of being silently discarded.



## PostgreSQL Loading

Validated records are loaded into the PostgreSQL `orders` table.

The load process uses a full-refresh strategy:

1. Connect to PostgreSQL.
2. Start a database transaction.
3. Truncate existing records from the `orders` table.
4. Load the latest cleaned dataset using PostgreSQL `COPY`.
5. Commit the transaction if loading succeeds.
6. Roll back the transaction if loading fails.

This prevents partial or corrupted loads and makes the pipeline safe to rerun.

## Environment Variables

Database credentials are stored in a `.env` file instead of being hardcoded in Python.

Example:

```text
DB_HOST=localhost
DB_NAME=etl_project
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

The `.env` file is excluded from Git using `.gitignore`.

## Installation

Create and activate a Python virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL database:

```text
etl_project
```

Create the `orders` table before running the pipeline.

## Running the Pipeline

Run the complete ETL pipeline from the project root:

```bash
python src/main.py
```

The pipeline automatically executes:

```text
transform_data.py
        ↓
verify_data.py
        ↓
load_data.py
        ↓
PostgreSQL
```

A successful run ends with:

```text
===== ETL PIPELINE COMPLETED SUCCESSFULLY =====
```

## Logging

Pipeline execution events are written to:

```text
logs/pipeline.log
```

The log records timestamps, successful processing stages, and pipeline failures for troubleshooting.