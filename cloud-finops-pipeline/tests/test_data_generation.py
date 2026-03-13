import pandas as pd


def test_dataset_exists():

    df = pd.read_csv("data/raw/cloud_case_study_dataset.csv")

    assert df.shape[0] > 0


def test_dataset_columns():

    df = pd.read_csv("data/raw/cloud_case_study_dataset.csv")

    expected = [

        "Usage_ID","Account","TS","Service","SKU","Usage","Unit",
        "Cost","Currency","Region","Free_Tier_Flag","Tag_Owner",
        "Tag_Env","Resource_ID","Ticket_ID","Ticket_Text",
        "Incident_ID","Price_Version","Pricing_Type","Department",
        "Project","SLA_Event","Log_Skew_Seconds","FX_Rate",
        "Purchase_Type","Anomaly_Flag","Duplicate_Flag",
        "Cost_Allocation_Valid"

    ]

    for col in expected:
        assert col in df.columns