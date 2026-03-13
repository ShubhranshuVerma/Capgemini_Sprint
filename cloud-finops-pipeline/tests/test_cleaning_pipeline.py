import pandas as pd

df = pd.read_csv("data/cleaned/cleaned_dataset.csv")


# 1 Account normalization
def test_account_uppercase():
    assert df["Account"].str.isupper().all()


# 2 Timestamp normalization
def test_timestamp_parsed():
    assert pd.to_datetime(df["TS"], errors="coerce").notnull().all()


# 3 Service normalization
def test_service_format():
    assert df["Service"].str[0].str.isupper().all()


# 4 SKU canonical naming
def test_sku_uppercase():
    assert df["SKU"].str.isupper().all()


# 5 Usage normalization
def test_usage_positive():
    assert (df["Usage"] >= 0).all()


# 6 Currency normalization
def test_cost_numeric():
    assert df["Cost"].dtype != object


# 7 Region normalization
def test_region_format():
    assert df["Region"].str.contains("-").all()


# 8 Duplicate detection
def test_duplicate_column():
    assert "Duplicate_Flag" in df.columns


# 9 Spike detection
def test_spike_column_exists():
    assert "Spike_Flag" in df.columns


# 10 Tag normalization
def test_tags_exist():
    assert df["Tag_Owner"].notnull().any()


# 11 Resource ID validation
def test_resource_id_format():
    assert df["Resource_ID"].notnull().all()


# 12 PII masking
def test_ticket_masking():
    assert df["Ticket_Text"].str.contains("MASKED").any()


# 13 Incident timestamps
def test_incident_exists():
    assert df["Incident_ID"].notnull().any()


# 14 Pricing version
def test_price_version():
    assert df["Price_Version"].notnull().all()


# 15 Currency normalization
def test_currency_uppercase():
    assert df["Currency"].str.isupper().all()


# 16 Idle resource detection
def test_idle_column():
    assert "Idle_Resource" in df.columns


# 17 Pricing model normalization
def test_pricing_model():
    assert df["Pricing_Type"].str.islower().all()


# 18 Cost validation
def test_cost_positive():
    assert (df["Cost_INR"] >= 0).all()


# 19 SLA event
def test_sla_event():
    assert df["SLA_Event"].notnull().all()


# 20 Log skew correction
def test_log_skew():
    assert df["Log_Skew_Seconds"].notnull().all()

