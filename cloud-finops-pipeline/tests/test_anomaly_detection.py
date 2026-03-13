import pandas as pd


def test_anomaly_dataset_not_empty():

    df = pd.read_csv("data/transformed/anomaly_spikes.csv")

    assert df.shape[0] > 0


def test_anomaly_columns_exist():

    df = pd.read_csv("data/transformed/anomaly_spikes.csv")

    assert "Cost_INR" in df.columns
    assert "Usage" in df.columns


def test_anomaly_cost_spikes():

    df = pd.read_csv("data/transformed/anomaly_spikes.csv")

    assert df["Cost_INR"].max() > df["Cost_INR"].mean()