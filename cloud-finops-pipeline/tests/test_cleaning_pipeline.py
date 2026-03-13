import pandas as pd


usage = pd.read_csv("data/cleaned/usage_cleaned.csv")
inventory = pd.read_csv("data/cleaned/inventory_cleaned.csv")
tickets = pd.read_csv("data/cleaned/tickets_cleaned.csv")
incidents = pd.read_csv("data/cleaned/incidents_cleaned.csv")
pricing = pd.read_csv("data/cleaned/pricing_cleaned.csv")
sla = pd.read_csv("data/cleaned/sla_cleaned.csv")
security = pd.read_csv("data/cleaned/security_cleaned.csv")


# 1 Account normalization
def test_account_uppercase():
    assert usage["Account"].str.isupper().all()


# 2 Timestamp normalization
def test_timestamp_parsed():
    assert pd.to_datetime(usage["TS"], errors="coerce").notnull().all()


# 3 Service normalization
def test_service_format():
    assert usage["Service"].str[0].str.isupper().all()


# 4 SKU canonical naming
def test_sku_uppercase():
    assert usage["SKU"].str.isupper().all()


# 5 Usage unit normalization
def test_usage_seconds_positive():
    assert (usage["Usage_seconds"] >= 0).all()


# 6 Currency normalization
def test_cost_numeric():
    assert usage["Cost_INR"].dtype != object


# 7 Region normalization
def test_region_format():
    assert usage["Region"].str.contains("-").all()


# 8 Duplicate removal
def test_no_duplicates():
    duplicates = usage.duplicated(subset=["Account","TS","SKU"])
    assert duplicates.sum() == 0


# 9 Spike detection
def test_spike_column_exists():
    assert "Spike_Flag" in usage.columns


# 10 Tag normalization
def test_inventory_service_format():
    assert inventory["Service"].notnull().all()


# 11 Resource ID validation
def test_resource_id_format():
    assert inventory["Resource_ID"].str.startswith("R").all()


# 12 PII masking
def test_ticket_masking():
    assert tickets["Description"].str.contains("[MASKED]").any()


# 13 Incident timestamps
def test_incident_times():
    assert pd.to_datetime(incidents["Start_TS"]).notnull().all()


# 14 Pricing effective date
def test_pricing_date():
    assert pd.to_datetime(pricing["Effective_Date"]).notnull().all()


# 15 Currency normalization
def test_currency_uppercase():
    assert pricing["Currency"].str.isupper().all()


# 16 Idle resource detection
def test_idle_column():
    assert "Idle" in inventory.columns


# 17 Pricing model normalization
def test_pricing_model_lowercase():
    assert inventory["Pricing_Model"].str.islower().all()


# 18 Cost validation
def test_cost_positive():
    assert (usage["Cost_INR"] >= 0).all()


# 19 SLA timestamp normalization
def test_sla_timestamp():
    assert pd.to_datetime(sla["Event_TS"], errors="coerce").notnull().all()


# 20 Log time skew correction
def test_security_timestamp():
    assert pd.to_datetime(security["Event_TS"], errors="coerce").notnull().all()