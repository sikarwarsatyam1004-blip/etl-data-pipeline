# Customer Orders ETL Pipeline with Apache Airflow

![ETL Pipeline CI](https://github.com/sikarwarsatyam1004-blip/etl-data-pipeline/actions/workflows/ci.yml/badge.svg)

## Project Overview

This project implements an end-to-end **Data Engineering ETL pipeline** using **Python, Apache Airflow, Docker, and PostgreSQL**.

The pipeline ingests raw customer order data, performs data cleaning and validation, executes data quality checks, loads processed data into PostgreSQL, and sends automated Slack notifications with execution metrics.

---

## Architecture

```text
                    Raw Data
                        |
                        v
        customer_orders_raw_100k.csv
                        |
                        v
                Apache Airflow DAG
                        |
        --------------------------------
        |                              |
        v                              v
 transform_data.py              verify_data.py
        |
        v
 cleaned_orders.csv
 rejected_orders.csv
        |
        v
 data_quality_check.py
        |
        v
 data_quality_report.json
        |
        v
 load_data.py
        |
        v
 PostgreSQL Database
        |
        v
 Slack Monitoring Alerts
```

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | ETL processing and data validation |
| Apache Airflow | Workflow orchestration and scheduling |
| Docker | Containerized execution environment |
| PostgreSQL | Data storage |
| Pandas | Data transformation |
| Slack Webhook | Pipeline monitoring and alerts |
| Git | Version control |


## Project Workflow

The pipeline follows this workflow:

### 1. Data Extraction

The pipeline reads raw customer order data from:

```text
data/raw/customer_orders_raw_100k.csv
```

The dataset contains:

- Customer information
- Order details
- Payment information
- Product information
- Transaction details


### 2. Data Transformation

File:

```text
transform_data.py
```

The transformation process includes:

- Removing duplicate records
- Handling missing values
- Validating email formats
- Validating age ranges
- Validating quantity values
- Validating pricing fields
- Standardizing order status
- Recalculating total amounts
- Separating valid and rejected records

Generated outputs:

```text
data/processed/

cleaned_orders.csv
rejected_orders.csv
```


### 3. Data Quality Checks

File:

```text
data_quality_check.py
```

Implemented validations:

- Row count validation
- Null percentage checks
- Duplicate record checks
- Schema validation

Generated report:

```text
data_quality_report.json
```


### 4. Data Loading

File:

```text
load_data.py
```

The pipeline loads validated records into PostgreSQL.

Database:

```text
PostgreSQL → etl_project → orders table
```


### 5. Monitoring and Alerts

After every DAG execution:

- Success metrics are sent to Slack
- Failure notifications are triggered
- ETL execution statistics are tracked


## Airflow DAG Details

DAG Name:

```text
customer_orders_etl_pipeline
```

Schedule:

```text
Daily at 08:00 AM IST
```

Executor:

```text
CeleryExecutor
```

The DAG contains the following tasks:

```text
transform_data
        |
        v
verify_data
        |
        v
data_quality_check
        |
        v
load_data
```

### Task Description

| Task | Description |
|------|-------------|
| transform_data | Cleans raw customer order data and creates processed datasets |
| verify_data | Validates cleaned data before loading |
| data_quality_check | Performs row count, null, duplicate, and schema validation |
| load_data | Loads validated records into PostgreSQL |

### Airflow Features Used

- DAG scheduling
- Task dependencies
- Retry mechanism
- Task failure callbacks
- Slack notifications
- Execution monitoring


## Data Quality Results

The pipeline performs automated data quality validation before loading data into PostgreSQL.

### Validation Checks

| Check | Description | Result |
|-------|-------------|--------|
| Row Count Validation | Ensures processed data contains records | PASS |
| Null Percentage Check | Validates missing values are within acceptable limits | PASS |
| Duplicate Check | Ensures duplicate records are removed | PASS |
| Schema Validation | Confirms required columns are available | PASS |

### Latest Pipeline Metrics

| Metric | Count |
|--------|-------|
| Input Records | 100,000 |
| Records After Deduplication | 98,000 |
| Valid Records | 97,469 |
| Rejected Records | 531 |
| Loaded Records | 97,469 |

Generated reports:

```text
data/processed/

etl_metrics.json
data_quality_report.json
```


## Slack Monitoring Alerts

The pipeline integrates with Slack using Incoming Webhooks for real-time monitoring.

Notifications are automatically sent after DAG execution.

### Success Notification

Example:

```text
✅ Airflow DAG Completed Successfully

DAG: customer_orders_etl_pipeline

📊 ETL Metrics

Input Rows: 100000
Rows After Deduplication: 98000
Valid Rows: 97469
Rejected Rows: 531
Loaded Rows: 97469

🔍 Data Quality Report

Row Count Check: PASS
Null Check: PASS
Duplicate Check: PASS
Schema Check: PASS

Status: SUCCESS
```

### Failure Notification

Example:

```text
🚨 Airflow Task Failed

DAG:
customer_orders_etl_pipeline

Task:
transform_data

Run ID:
manual__xxxx

Try Number:
3
```

Slack alerts provide:

- Pipeline success confirmation
- Failure notifications
- ETL execution metrics
- Data quality validation status


## Project Structure

```
etl-pipeline/

├── airflow/
│   ├── dags/
│   │   ├── customer_orders_etl_dag.py
│   │   ├── transform_data.py
│   │   ├── verify_data.py
│   │   ├── data_quality_check.py
│   │   └── load_data.py
│   │
│   ├── docker-compose.yaml
│   ├── config/
│   ├── logs/
│   └── plugins/
│
├── data/
│   ├── raw/
│   │   └── customer_orders_raw_100k.csv
│   │
│   └── processed/
│       ├── cleaned_orders.csv
│       ├── rejected_orders.csv
│       ├── etl_metrics.json
│       └── data_quality_report.json
│
├── README.md
├── requirements.txt
└── .gitignore
```


## Running the Project

### Prerequisites

Install:

- Docker Desktop
- Python 3.x
- Git


### Start Airflow Environment

Navigate to the Airflow directory:

```bash
cd airflow
```

Start the containers:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```


### Access Airflow UI

Open:

```text
http://localhost:8080
```

Login:

```text
Username: airflow
Password: airflow
```


### Run the ETL Pipeline

From the Airflow UI:

1. Open DAGs
2. Select:

```text
customer_orders_etl_pipeline
```

3. Click:

```text
Trigger DAG
```


### Stop Environment

To stop Airflow:

```bash
docker compose down
```


## Future Improvements

The following enhancements can be added to further improve this project:

- Add Power BI or Tableau dashboard for analytics visualization
- Add automated unit testing for ETL functions
- Add CI/CD pipeline using GitHub Actions
- Deploy Airflow and PostgreSQL on cloud platforms (AWS/GCP/Azure)
- Add data lineage tracking
- Integrate Great Expectations for advanced data quality validation
- Add monitoring dashboards using Grafana and Prometheus
- Add incremental data loading instead of full refresh
- Add metadata tracking for pipeline executions
