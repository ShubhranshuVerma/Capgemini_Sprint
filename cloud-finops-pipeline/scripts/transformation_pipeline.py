import pandas as pd
import numpy as np

INPUT = "../data/cleaned/cleaned_dataset.csv"
OUT = "../data/transformed/"

df = pd.read_csv(INPUT)
df["TS"] = pd.to_datetime(df["TS"])

# 1. Daily & monthly cost/usage cubes

daily_cube = df.groupby([df["TS"].dt.date, "Service", "SKU", "Region"]).agg(Cost_INR=("Cost_INR","sum"),Usage_seconds=("Usage_seconds","sum")).reset_index()

monthly_cube = df.groupby([df["TS"].dt.to_period("M"), "Service", "SKU", "Region"]).agg(Cost_INR=("Cost_INR","sum"),Usage_seconds=("Usage_seconds","sum")).reset_index()

# 2. Chargeback / showback

chargeback = df.groupby(["Department","Project"])["Cost_INR"].sum().reset_index()

# 3. Reserved / savings plan utilization

ri_utilization = df.groupby("Purchase_Type").size().reset_index(name="count")

# 4. Idle / rightsizing recommendations

rightsizing = df[df["Idle_Resource"] == True]

# 5. SRE KPIs (SLA attainment)

sre_kpis = df.groupby("Service")["SLA_Event"].value_counts().unstack(fill_value=0)

# 6. Incident MTTR / MTTA

incident = df.groupby("Incident_ID")["TS"].agg(["min","max"]).reset_index()

incident["MTTR_minutes"] = (incident["max"] - incident["min"]).dt.total_seconds()/60

# 7. Cost anomaly features

anomalies = df[df["Spike_Flag"] == True]

# 8. Unit cost normalization

df["Unit_Cost"] = df["Cost_INR"] / df["Usage_seconds"].replace(0,np.nan)

unit_cost = df.groupby("Service")["Unit_Cost"].mean().reset_index()

# 9. Carbon footprint estimates

df["carbon"] = df["Usage_seconds"] * 0.0000002

carbon = df.groupby(["Region","Service"])["carbon"].sum().reset_index()

# 10. Cost forecast (trend)

forecast = df.groupby(df["TS"].dt.month)["Cost_INR"].sum().reset_index()

# 11. Tag completeness scorecards

tag_score = pd.DataFrame({"Tag":["Tag_Owner","Tag_Env"],
                          "Missing_Count":[(df["Tag_Owner"]=="unknown").sum(),(df["Tag_Env"]=="unknown").sum()]
})

# 12. FinOps KPIs

finops_kpis = df.groupby("Service")["Cost_INR"].sum().reset_index()

# 13. Optimization backlog

optimization_backlog = df[df["Idle_Resource"] == True]

# 14. Benchmark comparison

benchmark = df.groupby("Service")["Cost_INR"].mean().reset_index()

# 15. Support ticket topics

ticket_topics = df.groupby("Ticket_ID").size().reset_index(name="count")

# 16. Churn signals

churn = df.groupby("Account")["Usage_seconds"].mean().reset_index()

# 17. Unit economics

unit_economics = df.groupby("Service")["Cost_INR"].sum().reset_index()

# 18. Multi-cloud view

multi_cloud = df.groupby("Region")["Cost_INR"].sum().reset_index()

# 19 Security Event Correlation with Costs

# filter only security events
security_events = df[df["SLA_Event"] != "NONE"]

# count events
security_counts = security_events.groupby(["Region","Service"]).size().reset_index(name="Security_Event_Count")

# compute cost by region/service
cost_summary = df.groupby(["Region","Service"])["Cost_INR"].sum().reset_index()

# join both
security_cost_correlation = pd.merge(security_counts,cost_summary,on=["Region","Service"],how="left")

# 20. Public dashboard extracts

dashboard_extract = df[["Account","Service","Cost_INR","Region","TS"]]


daily_cube.to_csv(OUT+"daily_cost_cube.csv",index=False)
monthly_cube.to_csv(OUT+"monthly_cost_cube.csv",index=False)
chargeback.to_csv(OUT+"chargeback.csv",index=False)
ri_utilization.to_csv(OUT+"ri_utilization.csv",index=False)
rightsizing.to_csv(OUT+"rightsizing.csv",index=False)
incident.to_csv(OUT+"incident_metrics.csv",index=False)
anomalies.to_csv(OUT+"anomaly_spikes.csv",index=False)
unit_cost.to_csv(OUT+"unit_cost_metrics.csv",index=False)
carbon.to_csv(OUT+"carbon_estimates.csv",index=False)
forecast.to_csv(OUT+"cost_forecast.csv",index=False)
tag_score.to_csv(OUT+"tag_scorecards.csv",index=False)
finops_kpis.to_csv(OUT+"finops_kpis.csv",index=False)
optimization_backlog.to_csv(OUT+"optimization_backlog.csv",index=False)
benchmark.to_csv(OUT+"benchmark.csv",index=False)
ticket_topics.to_csv(OUT+"ticket_topics.csv",index=False)
churn.to_csv(OUT+"churn_signals.csv",index=False)
unit_economics.to_csv(OUT+"unit_economics.csv",index=False)
multi_cloud.to_csv(OUT+"multi_cloud_view.csv",index=False)
security_cost_correlation.to_csv(OUT + "security_correlation.csv",index=False)
dashboard_extract.to_csv(OUT+"dashboard_extract.csv",index=False)

print("All 20 transformation scenarios executed successfully.")