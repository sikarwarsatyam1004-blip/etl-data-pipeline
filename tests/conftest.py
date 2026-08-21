import os
import json
import pandas as pd
import pytest


@pytest.fixture(scope="session", autouse=True)
def create_test_data():

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "order_date": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03"
            ],
            "order_status": [
                "Completed",
                "Completed",
                "Shipped"
            ],
            "quantity": [1, 2, 3],
            "unit_price": [100, 200, 300],
            "total_amount": [
                100,
                400,
                900
            ]
        }
    )

    df.to_csv(
        "data/processed/cleaned_orders.csv",
        index=False
    )


    metrics = {
        "input_rows": 3,
        "rows_after_deduplication": 3,
        "valid_rows": 3,
        "rejected_rows": 0,
        "loaded_rows": 3
    }


    with open(
        "data/processed/etl_metrics.json",
        "w"
    ) as file:
        json.dump(metrics, file)


    quality = {
        "null_check_status": "PASS",
        "duplicate_check_status": "PASS",
        "schema_check_status": "PASS"
    }


    with open(
        "data/processed/data_quality_report.json",
        "w"
    ) as file:
        json.dump(quality, file)