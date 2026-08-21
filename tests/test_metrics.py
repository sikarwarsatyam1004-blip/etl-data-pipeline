import json


def test_etl_metrics():

    with open(
        "data/processed/etl_metrics.json"
    ) as file:

        metrics = json.load(file)


    assert metrics["input_rows"] > 0
    assert metrics["valid_rows"] > 0
    assert metrics["loaded_rows"] > 0


def test_quality_report():

    with open(
        "data/processed/data_quality_report.json"
    ) as file:

        report = json.load(file)


    assert report["null_check_status"] == "PASS"
    assert report["duplicate_check_status"] == "PASS"
    assert report["schema_check_status"] == "PASS"
    