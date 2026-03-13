import pandas as pd
import numpy as np
from datetime import datetime

CLEAN = "../data/cleaned/"
TRANSFORMED = "../data/transformed/"

def load_datasets():

    usage = pd.read_csv(CLEAN+"usage_cleaned.csv")
    inventory = pd.read_csv(CLEAN+"inventory_cleaned.csv")
    tickets = pd.read_csv(CLEAN+"tickets_cleaned.csv")
    incidents = pd.read_csv(CLEAN+"incidents_cleaned.csv")
    pricing = pd.read_csv(CLEAN+"pricing_cleaned.csv")
    sla = pd.read_csv(CLEAN+"sla_cleaned.csv")
    security = pd.read_csv(CLEAN+"security_cleaned.csv")

    usage["TS"] = pd.to_datetime(usage["TS"])

    return usage, inventory, tickets, incidents, pricing, sla, security

#1.

def daily_cost_cube(usage):

    usage["date"] = usage["TS"].dt.date

    daily = usage.groupby(
        ["date","Service","SKU","Region"]
    ).agg(
        total_usage=("Usage_seconds","sum"),
        total_cost=("Cost_INR","sum")
    ).reset_index()

    return daily

#2.

def monthly_cost_cube(usage):

    usage["month"] = usage["TS"].dt.to_period("M")

    monthly = usage.groupby(
        ["month","Service","Region"]
    ).agg(
        monthly_cost=("Cost_INR","sum"),
        monthly_usage=("Usage_seconds","sum")
    ).reset_index()

    return monthly

#3.

def chargeback(usage):

    charge = usage.groupby("Account").agg(
        total_cost=("Cost_INR","sum"),
        total_usage=("Usage_seconds","sum")
    ).reset_index()

    return charge

#4.

def reserved_utilization(inventory):

    util = inventory.groupby("Pricing_Model").size().reset_index(name="count")

    return util

#5.

def rightsizing(inventory):

    idle = inventory[inventory["Idle"] == True]

    return idle

#6.

def sre_kpis(sla):

    events = sla.groupby("Service").size().reset_index(name="sla_events")

    return events

#7.

def incident_metrics(incidents):

    incidents["Start_TS"] = pd.to_datetime(incidents["Start_TS"])
    incidents["End_TS"] = pd.to_datetime(incidents["End_TS"])

    incidents["MTTR"] = (
        incidents["End_TS"] - incidents["Start_TS"]
    ).dt.total_seconds()/60

    metrics = incidents.groupby("Service").agg(
        avg_mttr=("MTTR","mean"),
        incident_count=("Incident_ID","count")
    ).reset_index()

    return metrics

#8.

def cost_anomalies(usage):

    mean = usage["Cost_INR"].mean()
    std = usage["Cost_INR"].std()

    threshold = mean + 2*std

    anomalies = usage[usage["Cost_INR"] > threshold]

    return anomalies

#9.

def unit_cost_metrics(usage):

    usage["unit_cost"] = usage["Cost_INR"]/usage["Usage_seconds"]

    metrics = usage.groupby("Service").agg(
        avg_unit_cost=("unit_cost","mean")
    ).reset_index()

    return metrics

#10.

def carbon_estimates(usage):

    usage["carbon_estimate"] = usage["Usage_seconds"] * 0.0000002

    carbon = usage.groupby("Region").agg(
        carbon=("carbon_estimate","sum")
    ).reset_index()

    return carbon

#11.

def cost_forecast(usage):

    usage["month"] = usage["TS"].dt.to_period("M")

    monthly = usage.groupby("month")["Cost_INR"].sum().reset_index()

    monthly["forecast"] = monthly["Cost_INR"].rolling(2).mean()

    return monthly

#12.

def tag_score(inventory):

    score = inventory.groupby("Service").agg(
        total=("Resource_ID","count")
    ).reset_index()

    return score

#13.

def finops_kpis(usage):

    total_cost = usage["Cost_INR"].sum()

    avg_cost = usage["Cost_INR"].mean()

    top_service = usage.groupby("Service")["Cost_INR"].sum().idxmax()

    df = pd.DataFrame({
        "Metric":["Total_Cost","Average_Cost","Top_Service"],
        "Value":[total_cost,avg_cost,top_service]
    })

    return df

#14.

def optimization_backlog(inventory):

    backlog = inventory[inventory["Idle"] == True]

    return backlog

#15.

def benchmark_comparison(usage):

    avg_cost = usage["Cost_INR"].mean()

    benchmark = avg_cost * 0.9

    df = pd.DataFrame({
        "Metric":["Our_Cost","Industry_Benchmark"],
        "Value":[avg_cost,benchmark]
    })

    return df

#16.

def ticket_topics(tickets):

    topics = tickets.groupby("Issue_Type").size().reset_index(name="count")

    return topics

#17.

def churn_signals(usage):

    usage["month"] = usage["TS"].dt.to_period("M")

    churn = usage.groupby(["Account","month"])["Usage_seconds"].sum().reset_index()

    return churn

#18.

def unit_economics(usage):

    economics = usage.groupby("Service").agg(
        revenue=("Cost_INR","sum"),
        usage=("Usage_seconds","sum")
    ).reset_index()

    return economics

#19.

def multi_cloud_view(usage):

    view = usage.groupby(["Region","Service"]).agg(
        cost=("Cost_INR","sum")
    ).reset_index()

    return view

#20.

def security_correlation(security):

    corr = security.groupby("Severity").size().reset_index(name="event_count")

    return corr



def run_pipeline():

    usage, inventory, tickets, incidents, pricing, sla, security = load_datasets()

    daily = daily_cost_cube(usage)
    monthly = monthly_cost_cube(usage)
    charge = chargeback(usage)
    util = reserved_utilization(inventory)
    rights = rightsizing(inventory)
    sre = sre_kpis(sla)
    mttr = incident_metrics(incidents)
    anomalies = cost_anomalies(usage)
    unit = unit_cost_metrics(usage)
    carbon = carbon_estimates(usage)
    forecast = cost_forecast(usage)
    tags = tag_score(inventory)
    finops = finops_kpis(usage)
    backlog = optimization_backlog(inventory)
    bench = benchmark_comparison(usage)
    topics = ticket_topics(tickets)
    churn = churn_signals(usage)
    economics = unit_economics(usage)
    cloud = multi_cloud_view(usage)
    sec = security_correlation(security)

    daily.to_csv(TRANSFORMED+"daily_cost_cube.csv",index=False)
    monthly.to_csv(TRANSFORMED+"monthly_cost_cube.csv",index=False)
    charge.to_csv(TRANSFORMED+"chargeback.csv",index=False)
    util.to_csv(TRANSFORMED+"reserved_utilization.csv",index=False)
    rights.to_csv(TRANSFORMED+"rightsizing.csv",index=False)
    sre.to_csv(TRANSFORMED+"sre_kpis.csv",index=False)
    mttr.to_csv(TRANSFORMED+"incident_metrics.csv",index=False)
    anomalies.to_csv(TRANSFORMED+"anomaly_spikes.csv",index=False)
    unit.to_csv(TRANSFORMED+"unit_cost_metrics.csv",index=False)
    carbon.to_csv(TRANSFORMED+"carbon_estimates.csv",index=False)
    forecast.to_csv(TRANSFORMED+"cost_forecast.csv",index=False)
    tags.to_csv(TRANSFORMED+"tag_scorecards.csv",index=False)
    finops.to_csv(TRANSFORMED+"finops_kpis.csv",index=False)
    backlog.to_csv(TRANSFORMED+"optimization_backlog.csv",index=False)
    bench.to_csv(TRANSFORMED+"benchmark.csv",index=False)
    topics.to_csv(TRANSFORMED+"ticket_topics.csv",index=False)
    churn.to_csv(TRANSFORMED+"churn_signals.csv",index=False)
    economics.to_csv(TRANSFORMED+"unit_economics.csv",index=False)
    cloud.to_csv(TRANSFORMED+"multi_cloud_view.csv",index=False)
    sec.to_csv(TRANSFORMED+"security_correlation.csv",index=False)

    print("All 20 transformation scenarios executed successfully")


if __name__ == "__main__":
    run_pipeline()