import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT = "./output/"

sns.set(style="whitegrid")

# -----------------------------
# Load transformed datasets
# -----------------------------

daily = pd.read_csv("../data/transformed/daily_cost_cube.csv")
monthly = pd.read_csv("../data/transformed/monthly_cost_cube.csv")
chargeback = pd.read_csv("../data/transformed/chargeback.csv")
anomaly = pd.read_csv("../data/transformed/anomaly_spikes.csv")
unit_cost = pd.read_csv("../data/transformed/unit_cost_metrics.csv")
carbon = pd.read_csv("../data/transformed/carbon_estimates.csv")
incident = pd.read_csv("../data/transformed/incident_metrics.csv")

# -----------------------------
# 1 Daily Cost Trend
# -----------------------------

daily["TS"] = pd.to_datetime(daily["TS"])

plt.figure(figsize=(10,5))
sns.lineplot(data=daily, x="TS", y="Cost_INR")
plt.title("Daily Cost Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "daily_cost_trend.png")
plt.close()

# -----------------------------
# 2 Monthly Cost by Service
# -----------------------------

plt.figure(figsize=(10,5))
sns.barplot(data=monthly, x="TS", y="Cost_INR")
plt.title("Monthly Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "monthly_cost.png")
plt.close()

# -----------------------------
# 3 Department Chargeback
# -----------------------------

plt.figure(figsize=(10,5))
sns.barplot(data=chargeback, x="Department", y="Cost_INR")
plt.title("Department Chargeback")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "chargeback.png")
plt.close()

# -----------------------------
# 4 Cost Anomaly Detection
# -----------------------------

plt.figure(figsize=(8,5))
sns.scatterplot(data=anomaly, x="Usage_seconds", y="Cost_INR")
plt.title("Cost Anomaly Detection")
plt.tight_layout()
plt.savefig(OUTPUT + "cost_anomalies.png")
plt.close()

# -----------------------------
# 5 Unit Cost Metrics
# -----------------------------

plt.figure(figsize=(8,5))
sns.barplot(data=unit_cost, x="Service", y="Unit_Cost")
plt.title("Unit Cost by Service")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT + "unit_cost.png")
plt.close()

# -----------------------------
# 6 Carbon Emissions by Region
# -----------------------------

plt.figure(figsize=(8,5))
sns.barplot(data=carbon, x="Region", y="carbon")
plt.title("Carbon Emissions by Region")
plt.tight_layout()
plt.savefig(OUTPUT + "carbon_emissions.png")
plt.close()

# -----------------------------
# 7 MTTR Metrics
# -----------------------------

plt.figure(figsize=(10,5))
sns.barplot(data=incident, x="Incident_ID", y="MTTR_minutes")
plt.title("Incident MTTR")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(OUTPUT + "mttr_metrics.png")
plt.close()

print("Dashboard charts generated successfully")