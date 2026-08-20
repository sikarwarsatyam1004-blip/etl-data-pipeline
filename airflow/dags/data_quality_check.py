import pandas as pd
import json
import sys


file_path = "/opt/airflow/data/processed/cleaned_orders.csv"

report_path = "/opt/airflow/data/processed/data_quality_report.json"


required_columns = [
    "order_id",
    "order_date",
    "order_status",
    "quantity",
    "unit_price",
    "total_amount"
]


df = pd.read_csv(file_path)


quality_report = {}


row_count = len(df)

quality_report["row_count"] = {
    "value": row_count,
    "status": "PASS" if row_count > 0 else "FAIL"
}


null_percentage = (
    df.isnull()
    .mean()
    .mul(100)
    .round(2)
    .to_dict()
)

quality_report["null_percentage"] = null_percentage

quality_report["null_check_status"] = (
    "FAIL"
    if any(value > 5 for value in null_percentage.values())
    else "PASS"
)


duplicate_count = int(df.duplicated().sum())

quality_report["duplicate_count"] = duplicate_count

quality_report["duplicate_check_status"] = (
    "FAIL"
    if duplicate_count > 0
    else "PASS"
)


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

quality_report["missing_columns"] = missing_columns

quality_report["schema_check_status"] = (
    "FAIL"
    if missing_columns
    else "PASS"
)


with open(report_path, "w") as file:
    json.dump(
        quality_report,
        file,
        indent=4
    )


print(json.dumps(quality_report, indent=4))


if "FAIL" in [
    quality_report["row_count"]["status"],
    quality_report["null_check_status"],
    quality_report["duplicate_check_status"],
    quality_report["schema_check_status"]
]:
    print("Data quality checks failed")
    sys.exit(1)


print("Data quality checks passed")