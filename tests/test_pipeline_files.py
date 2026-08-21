import os


def test_dag_file_exists():
    assert os.path.exists(
        "airflow/dags/customer_orders_etl_dag.py"
    )


def test_transform_file_exists():
    assert os.path.exists(
        "airflow/dags/transform_data.py"
    )


def test_quality_check_exists():
    assert os.path.exists(
        "airflow/dags/data_quality_check.py"
    )


def test_load_file_exists():
    assert os.path.exists(
        "airflow/dags/load_data.py"
    )