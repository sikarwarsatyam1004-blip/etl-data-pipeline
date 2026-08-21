import pandas as pd


def test_cleaned_orders_exists():

    df = pd.read_csv(
        "data/processed/cleaned_orders.csv"
    )

    assert len(df) > 0


def test_required_columns():

    df = pd.read_csv(
        "data/processed/cleaned_orders.csv"
    )

    required_columns = [
        "order_id",
        "order_date",
        "order_status",
        "quantity",
        "unit_price",
        "total_amount"
    ]

    for column in required_columns:
        assert column in df.columns


def test_no_duplicate_records():

    df = pd.read_csv(
        "data/processed/cleaned_orders.csv"
    )

    assert df.duplicated().sum() == 0