import pandas as pd


daily = pd.read_csv("data/transformed/daily_cost_cube.csv")
monthly = pd.read_csv("data/transformed/monthly_cost_cube.csv")
chargeback = pd.read_csv("data/transformed/chargeback.csv")
utilization = pd.read_csv("data/transformed/reserved_utilization.csv")
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


# 1 Daily cube
def test_daily_cube():
    assert "total_cost" in daily.columns


# 2 Monthly cube
def test_monthly_cube():
    assert "monthly_cost" in monthly.columns


# 3 Chargeback
def test_chargeback_accounts():
    assert chargeback.shape[0] > 0


# 4 Reserved utilization
def test_utilization():
    assert "count" in utilization.columns


# 5 Rightsizing
def test_rightsizing():
    assert rightsizing.shape[0] >= 0


# 6 SRE KPIs
def test_sre_kpis():
    assert "sla_events" in sre.columns


# 7 MTTR metrics
def test_mttr():
    assert "avg_mttr" in incidents.columns


# 8 Anomaly detection
def test_anomalies():
    assert anomalies.shape[0] >= 1


# 9 Unit cost metrics
def test_unit_cost():
    assert "avg_unit_cost" in unit.columns


# 10 Carbon estimates
def test_carbon():
    assert carbon["carbon"].sum() > 0


# 11 Cost forecast
def test_forecast():
    assert "forecast" in forecast.columns


# 12 Tag scorecards
def test_tags():
    assert tags.shape[0] > 0


# 13 FinOps KPIs
def test_finops():
    assert finops.shape[0] >= 1


# 14 Optimization backlog
def test_backlog():
    assert backlog.shape[0] >= 0


# 15 Benchmark comparison
def test_benchmark():
    assert benchmark.shape[0] == 2


# 16 Ticket topics
def test_ticket_topics():
    assert topics.shape[0] > 0


# 17 Churn signals
def test_churn():
    assert churn.shape[0] > 0


# 18 Unit economics
def test_unit_economics():
    assert economics.shape[0] > 0


# 19 Multi-cloud view
def test_multi_cloud():
    assert cloud.shape[0] > 0


# 20 Security correlation
def test_security():
    assert security.shape[0] > 0