import pandas as pd


daily = pd.read_csv("data/transformed/daily_cost_cube.csv")
monthly = pd.read_csv("data/transformed/monthly_cost_cube.csv")
chargeback = pd.read_csv("data/transformed/chargeback.csv")
reserved = pd.read_csv("data/transformed/reserved_utilization.csv")
rightsizing = pd.read_csv("data/transformed/rightsizing.csv")
sre = pd.read_csv("data/transformed/sre_kpis.csv")
incidents = pd.read_csv("data/transformed/incident_metrics.csv")
anomalies = pd.read_csv("data/transformed/anomaly_spikes.csv")
unit = pd.read_csv("data/transformed/unit_cost_metrics.csv")
carbon = pd.read_csv("data/transformed/carbon_estimates.csv")
forecast = pd.read_csv("data/transformed/cost_forecast.csv")
tags = pd.read_csv("data/transformed/tag_scorecards.csv")
finops = pd.read_csv("data/transformed/finops_kpis.csv")
backlog = pd.read_csv("data/transformed/optimization_backlog.csv")
benchmark = pd.read_csv("data/transformed/benchmark.csv")
topics = pd.read_csv("data/transformed/ticket_topics.csv")
churn = pd.read_csv("data/transformed/churn_signals.csv")
economics = pd.read_csv("data/transformed/unit_economics.csv")
cloud = pd.read_csv("data/transformed/multi_cloud_view.csv")
security = pd.read_csv("data/transformed/security_correlation.csv")


# 1 Daily cost cube
def test_daily_cost_cube():
    assert daily.shape[0] > 0
    assert "Cost_INR" in daily.columns


# 2 Monthly cost cube
def test_monthly_cost_cube():
    assert monthly.shape[0] > 0


# 3 Chargeback
def test_chargeback():
    assert chargeback.shape[0] > 0
    assert "Department" in chargeback.columns


# 4 Reserved utilization
def test_reserved_utilization():
    assert reserved.shape[0] > 0
    assert "count" in reserved.columns


# 5 Rightsizing recommendations
def test_rightsizing():
    assert rightsizing.shape[0] >= 0


# 6 SRE KPIs
def test_sre_kpis():
    assert sre.shape[0] > 0


# 7 Incident metrics
def test_incident_metrics():
    assert incidents.shape[0] > 0


# 8 Anomaly detection
def test_anomaly_spikes():
    assert anomalies.shape[0] > 0


# 9 Unit cost metrics
def test_unit_cost_metrics():
    assert unit.shape[0] > 0


# 10 Carbon estimates
def test_carbon_estimates():
    assert carbon["carbon"].sum() > 0


# 11 Cost forecast
def test_cost_forecast():
    assert forecast.shape[0] > 0


# 12 Tag scorecards
def test_tag_scorecards():
    assert tags.shape[0] >= 0


# 13 FinOps KPIs
def test_finops_kpis():
    assert finops.shape[0] > 0


# 14 Optimization backlog
def test_optimization_backlog():
    assert backlog.shape[0] >= 0


# 15 Benchmark comparison
def test_benchmark():
    assert benchmark.shape[0] > 0


# 16 Ticket topics
def test_ticket_topics():
    assert topics.shape[0] > 0


# 17 Churn signals
def test_churn_signals():
    assert churn.shape[0] > 0


# 18 Unit economics
def test_unit_economics():
    assert economics.shape[0] > 0


# 19 Multi-cloud view
def test_multi_cloud_view():
    assert cloud.shape[0] > 0


# 20 Security correlation
def test_security_correlation():
    assert security.shape[0] > 0