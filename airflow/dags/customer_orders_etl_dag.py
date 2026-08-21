from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum
import os
import requests
import json


def task_failure_alert(context):
    task_instance = context["task_instance"]

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    message = {
        "text": (
            "🚨 Airflow Task Failed\n"
            f"DAG: {task_instance.dag_id}\n"
            f"Task: {task_instance.task_id}\n"
            f"Run ID: {context.get('run_id')}\n"
            f"Try Number: {task_instance.try_number}"
        )
    }

    response = requests.post(webhook_url, json=message, timeout=10)
    response.raise_for_status()
default_args = {
    "owner": "data_engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": task_failure_alert
}

def dag_success_alert(context):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    dag_run = context["dag_run"]

    metrics_file = "/opt/airflow/data/processed/etl_metrics.json"

    with open(metrics_file, "r") as file:
        metrics = json.load(file)

    quality_file = "/opt/airflow/data/processed/data_quality_report.json"

    with open(quality_file, "r") as file:
        quality = json.load(file)


    message = {
        "username": "Airflow ETL Alerts",
        "icon_emoji": ":white_check_mark:",
        "text": (
            "✅ Airflow DAG Completed Successfully\n\n"
            f"DAG: {dag_run.dag_id}\n"
            f"Run ID: {dag_run.run_id}\n\n"

            "📊 ETL Metrics\n"
            f"Input Rows: {metrics['input_rows']}\n"
            f"Rows After Deduplication: {metrics['rows_after_deduplication']}\n"
            f"Valid Rows: {metrics['valid_rows']}\n"
            f"Rejected Rows: {metrics['rejected_rows']}\n"
            f"Loaded Rows: {metrics['loaded_rows']}\n\n"

            "🔍 Data Quality Report\n"
            f"Row Count Check: {quality['row_count']['status']}\n"
            f"Null Check: {quality['null_check_status']}\n"
            f"Duplicate Check: {quality['duplicate_check_status']}\n"
            f"Schema Check: {quality['schema_check_status']}\n\n"

            "Status: SUCCESS"
        )
    }

    response = requests.post(
        webhook_url,
        json=message,
        timeout=10
    )

    response.raise_for_status()


with DAG(
    dag_id="customer_orders_etl_pipeline",
    default_args=default_args,
    description="Customer orders ETL pipeline",
    start_date=pendulum.datetime(
        2026, 8, 19,
        tz="Asia/Kolkata"
    ),
    schedule="0 8 * * *",
    catchup=False,
     on_success_callback=dag_success_alert
) as dag:

    transform_task = BashOperator(
        task_id="transform_data",
        bash_command="python /opt/airflow/dags/transform_data.py"
    )

    verify_task = BashOperator(
        task_id="verify_data",
        bash_command="python /opt/airflow/dags/verify_data.py"
    )
    quality_task = BashOperator(
    task_id="data_quality_check",
    bash_command="python /opt/airflow/dags/data_quality_check.py"
)

    load_task = BashOperator(
    task_id="load_data",
    bash_command="python /opt/airflow/dags/load_data.py",
    env={
        "DB_HOST": "{{ conn.postgres_etl.host }}",
        "DB_NAME": "{{ conn.postgres_etl.schema }}",
        "DB_USER": "{{ conn.postgres_etl.login }}",
        "DB_PASSWORD": "{{ conn.postgres_etl.password }}",
        "DB_PORT": "{{ conn.postgres_etl.port }}"
    },
    append_env=True
)


transform_task >> verify_task >> quality_task >> load_task
