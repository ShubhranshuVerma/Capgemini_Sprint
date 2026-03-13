import pandas as pd

def test_usage_dataset_exists():
    df = pd.read_csv("data/raw/usage_raw.csv")
    assert df.shape[0] > 0


def test_usage_dataset_columns():
    df = pd.read_csv("data/raw/usage_raw.csv")

    expected = [
        "Usage_ID",
        "Account",
        "TS",
        "Service",
        "SKU",
        "Usage",
        "Unit",
        "Cost",
        "Region",
        "Ticket_ID"
    ]

    for col in expected:
        assert col in df.columns