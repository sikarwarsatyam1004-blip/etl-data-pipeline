import os


BASE_PATH = "airflow/dags"


def test_dag_file_exists():
    assert os.path.exists(
        f"{BASE_PATH}/customer_orders_etl_dag.py"
    )


def test_transform_file_exists():
    assert os.path.exists(
        f"{BASE_PATH}/transform_data.py"
    )


def test_quality_check_exists():
    assert os.path.exists(
        f"{BASE_PATH}/data_quality_check.py"
    )


def test_load_file_exists():
    assert os.path.exists(
        f"{BASE_PATH}/load_data.py"
    )


def test_verify_file_exists():
    assert os.path.exists(
        f"{BASE_PATH}/verify_data.py"
    )