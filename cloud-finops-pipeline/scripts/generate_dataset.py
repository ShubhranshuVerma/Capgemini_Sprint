import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

OUTPUT_PATH = "../data/raw/"

os.makedirs(OUTPUT_PATH, exist_ok=True)

def random_timestamp():
    base = datetime(2026,1,1)
    delta = timedelta(minutes=random.randint(0,500000))
    ts = base + delta

    formats = [
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        ts.strftime("%Y/%m/%d %H:%M"),
        ts.strftime("%Y-%m-%d %H:%M+00:00")
    ]

    return random.choice(formats)


rows = []

services = ["Compute","Storage","Database","AI","Networking"]

skus = ["VM-std_4","VM-STD-4","vm_std_4","STORAGE-prem","DB-gp_2"]

regions = ["ap-south 1","ap-south-1","AP-SOUTH-1","us-east 1"]

units = ["sec","seconds","min","hr"]

accounts = [" acct-001 ","ACCT-002","acct-003","ACCT-004"]

tickets = ["t-77","T-12","t-33","T-45"]

for i in range(800):

    rows.append({
        "Usage_ID": f"U{6000+i}",
        "Account": random.choice(accounts),
        "TS": random_timestamp(),
        "Service": random.choice(services),
        "SKU": random.choice(skus),
        "Usage": random.randint(100,20000),
        "Unit": random.choice(units),
        "Cost": f"₹ {round(random.uniform(10,2000),2)}",
        "Region": random.choice(regions),
        "Ticket_ID": random.choice(tickets)
    })

usage_df = pd.DataFrame(rows)

usage_df.to_csv(OUTPUT_PATH+"usage_raw.csv",index=False)

inventory = []

for i in range(400):

    inventory.append({
        "Resource_ID": f"R{i}",
        "Account": random.choice(accounts),
        "Service": random.choice(services),
        "Region": random.choice(["ap-south-1","us-east-1"]),
        "Instance_Type": random.choice(["t2.micro","m5.large","c5.xlarge"]),
        "Pricing_Model": random.choice(["OnDemand","Reserved","Spot"]),
        "Created_TS": random_timestamp(),
        "Status": random.choice(["running","stopped"])
    })

pd.DataFrame(inventory).to_csv(
    OUTPUT_PATH+"resource_inventory.csv",
    index=False
)

pricing = []

for sku in ["VM-STD-4","STORAGE-PREM","DB-GP-2"]:

    pricing.append({
        "SKU": sku,
        "Service": "Compute",
        "Region": "ap-south-1",
        "Price_per_unit": round(random.uniform(0.01,0.5),4),
        "Currency": "INR",
        "Effective_Date": "2026-01-01"
    })

pd.DataFrame(pricing).to_csv(
    OUTPUT_PATH+"pricing_catalog.csv",
    index=False
)


tickets_meta = []

for i in range(100):

    tickets_meta.append({
        "Ticket_ID": f"T-{i}",
        "Severity": random.choice(["low","medium","high"]),
        "Issue_Type": random.choice(["billing","outage","performance"]),
        "Description": "Customer reported issue with service",
        "Created_TS": random_timestamp()
    })

pd.DataFrame(tickets_meta).to_csv(
    OUTPUT_PATH+"tickets_metadata.csv",
    index=False
)

incidents = []

for i in range(50):

    start = datetime(2026,1,1) + timedelta(days=random.randint(1,100))
    end = start + timedelta(minutes=random.randint(10,200))

    incidents.append({
        "Incident_ID": f"I{i}",
        "Service": random.choice(services),
        "Region": "ap-south-1",
        "Start_TS": start,
        "End_TS": end,
        "Severity": random.choice(["sev1","sev2","sev3"])
    })

pd.DataFrame(incidents).to_csv(
    OUTPUT_PATH+"incidents.csv",
    index=False
)

sla = []

for i in range(50):

    sla.append({
        "Event_ID": f"S{i}",
        "Service": random.choice(services),
        "Region": "ap-south-1",
        "Event_TS": random_timestamp(),
        "Event_Type": random.choice(["downtime","degraded"])
    })

pd.DataFrame(sla).to_csv(
    OUTPUT_PATH+"sla_events.csv",
    index=False
)


security = []

for i in range(120):

    security.append({
        "Event_ID": f"E{i}",
        "Account": random.choice(accounts),
        "Service": random.choice(services),
        "Region": random.choice(["ap-south-1","us-east-1"]),
        "Event_TS": random_timestamp(),
        "Severity": random.choice(["low","medium","high"])
    })

pd.DataFrame(security).to_csv(
    OUTPUT_PATH+"security_events.csv",
    index=False
)

print("All datasets generated successfully")