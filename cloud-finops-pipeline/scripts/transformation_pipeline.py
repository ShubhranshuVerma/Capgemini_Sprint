import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

INPUT="../data/cleaned/cleaned_dataset.csv"
OUT="../data/transformed/"

df=pd.read_csv(INPUT)

df["TS"]=pd.to_datetime(df["TS"])

# 1 Daily cube
daily=df.groupby(
[df["TS"].dt.date,"Service","Region"]
).agg(
Cost_INR=("Cost_INR","sum"),
Usage=("Usage_seconds","sum")
).reset_index()

daily.to_csv(OUT+"daily_cost_cube.csv",index=False)

# 2 Monthly cube
monthly=df.groupby(
[df["TS"].dt.to_period("M"),"Service"]
)["Cost_INR"].sum().reset_index()

monthly.to_csv(OUT+"monthly_cost_cube.csv",index=False)

# 3 Chargeback
chargeback=df.groupby(
["Department","Project"]
)["Cost_INR"].sum().reset_index()

chargeback.to_csv(OUT+"chargeback.csv",index=False)

# 4 Reserved utilization
reserved=df.groupby("Purchase_Type").size().reset_index(name="count")

reserved.to_csv(OUT+"reserved_utilization.csv",index=False)

# 5 Rightsizing
rightsizing=df[df["Idle_Resource"]==True]

rightsizing.to_csv(OUT+"rightsizing.csv",index=False)

# 6 SRE KPIs
sre=df.groupby("Service")["SLA_Event"].value_counts().unstack(fill_value=0)

sre.to_csv(OUT+"sre_kpis.csv")

# 7 MTTR
incident=df.groupby("Incident_ID")["TS"].agg(["min","max"]).reset_index()

incident["MTTR_minutes"]=(incident["max"]-incident["min"]).dt.total_seconds()/60

incident.to_csv(OUT+"incident_metrics.csv",index=False)

# 8 Anomaly detection
anomalies=df[df["Spike_Flag"]==True]

anomalies.to_csv(OUT+"anomaly_spikes.csv",index=False)

# 9 Unit cost
df["Unit_Cost"]=df["Cost_INR"]/df["Usage_seconds"].replace(0,np.nan)

unit=df.groupby("Service")["Unit_Cost"].mean().reset_index()

unit.to_csv(OUT+"unit_cost_metrics.csv",index=False)

# 10 Carbon
df["carbon"]=df["Usage_seconds"]*0.0000002

carbon=df.groupby("Region")["carbon"].sum().reset_index()

carbon.to_csv(OUT+"carbon_estimates.csv",index=False)

# 11 Forecast
forecast_df=df.groupby(df["TS"].dt.month)["Cost_INR"].sum().reset_index()

X=forecast_df[["TS"]]
y=forecast_df["Cost_INR"]

model=LinearRegression()
model.fit(X,y)

future=pd.DataFrame({"TS":[13,14,15]})
future["Cost_INR"]=model.predict(future)

forecast=pd.concat([forecast_df,future])

forecast.to_csv(OUT+"cost_forecast.csv",index=False)

# 12 Tag scorecards
tag_score=pd.DataFrame({

"Tag":["Owner","Env"],
"Missing":[
df["Tag_Owner_Missing"].sum(),
df["Tag_Env_Missing"].sum()
]

})

tag_score.to_csv(OUT+"tag_scorecards.csv",index=False)

# 13 FinOps KPIs
finops=df.groupby("Service")["Cost_INR"].sum().reset_index()

finops.to_csv(OUT+"finops_kpis.csv",index=False)

# 14 Optimization backlog
optimization=df[df["Idle_Resource"]==True]

optimization.to_csv(OUT+"optimization_backlog.csv",index=False)

# 15 Benchmark comparison
benchmark=df.groupby("Service")["Cost_INR"].mean().reset_index()

benchmark.to_csv(OUT+"benchmark.csv",index=False)

# 16 Ticket clustering
vectorizer=TfidfVectorizer(stop_words="english")

X=vectorizer.fit_transform(df["Ticket_Text"])

kmeans=KMeans(n_clusters=5,random_state=42)

df["Ticket_Topic"]=kmeans.fit_predict(X)

topics=df.groupby("Ticket_Topic").size().reset_index(name="count")

topics.to_csv(OUT+"ticket_topics.csv",index=False)

# 17 Churn signals
churn=df.groupby("Account")["Usage_seconds"].mean().reset_index()

churn.to_csv(OUT+"churn_signals.csv",index=False)

# 18 Unit economics
economics=df.groupby("Service")["Cost_INR"].sum().reset_index()

economics.to_csv(OUT+"unit_economics.csv",index=False)

# 19 Multi cloud view
cloud=df.groupby("Region")["Cost_INR"].sum().reset_index()

cloud.to_csv(OUT+"multi_cloud_view.csv",index=False)

# 20 Security correlation
security=df[df["SLA_Event"]!="NONE"]

security_summary=security.groupby(
["Region","Service"]
).size().reset_index(name="Security_Event_Count")

security_summary.to_csv(OUT+"security_correlation.csv",index=False)

print("Transformation pipeline completed successfully")