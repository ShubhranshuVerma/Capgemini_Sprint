import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT = "./output/"

daily = pd.read_csv("../data/transformed/daily_cost_cube.csv")
monthly = pd.read_csv("../data/transformed/monthly_cost_cube.csv")
chargeback = pd.read_csv("../data/transformed/chargeback.csv")
anomaly = pd.read_csv("../data/transformed/anomaly_spikes.csv")
unit_cost = pd.read_csv("../data/transformed/unit_cost_metrics.csv")
carbon = pd.read_csv("../data/transformed/carbon_estimates.csv")
incident = pd.read_csv("../data/transformed/incident_metrics.csv")

# Daily cost trend
daily["TS"] = pd.to_datetime(daily["TS"])
daily_total = daily.groupby("TS")["Cost_INR"].sum().reset_index()

plt.figure(figsize=(10,5))
sns.lineplot(data=daily_total, x="TS", y="Cost_INR")
plt.title("Daily Cost Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "daily_cost_trend.png")
plt.close()

# Monthly cost
plt.figure(figsize=(10,5))
sns.barplot(data=monthly, x="TS", y="Cost_INR", hue="Service")
plt.title("Monthly Cost by Service")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "monthly_cost.png")
plt.close()

# Chargeback
plt.figure(figsize=(10,5))
sns.barplot(data=chargeback, x="Department", y="Cost_INR")
plt.title("Department Chargeback")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "chargeback.png")
plt.close()

# Anomaly detection
plt.figure(figsize=(8,5))
sns.scatterplot(data=anomaly, x="Usage_seconds", y="Cost_INR", hue="Service")
plt.title("Cost Anomalies")
plt.tight_layout()
plt.savefig(OUTPUT + "cost_anomalies.png")
plt.close()

# Unit cost
plt.figure(figsize=(8,5))
sns.barplot(data=unit_cost, x="Service", y="Unit_Cost")
plt.title("Unit Cost by Service")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "unit_cost.png")
plt.close()

# Carbon emissions
plt.figure(figsize=(8,5))
sns.barplot(data=carbon, x="Region", y="carbon")
plt.title("Carbon Emissions by Region")
plt.tight_layout()
plt.savefig(OUTPUT + "carbon_emissions.png")
plt.close()

# MTTR
incident = incident.sort_values("MTTR_minutes", ascending=False).head(20)

plt.figure(figsize=(10,5))
sns.barplot(data=incident, x="Incident_ID", y="MTTR_minutes")
plt.title("Top Incident MTTR")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(OUTPUT + "mttr_metrics.png")
plt.close()

print("Dashboard charts generated successfully")