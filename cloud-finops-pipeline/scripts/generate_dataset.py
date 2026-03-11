import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

NUM_ROWS = 1000
OUTPUT_FILE = "../data/raw/cloud_usage_raw.csv"

services = ["Compute", "Storage", "Database", "AI", "Networking"]

sku_variants = [
    "VM-std_4", "VM-STD-4", "vm_std_4",
    "STORAGE-prem", "storage-PREM",
    "DB-gp_2", "db-GP-2"
]

regions = [
    "ap-south 1",
    "ap-south-1",
    "AP-SOUTH-1",
    "us-east 1",
    "us-east-1"
]

units = ["sec", "seconds", "min", "hr"]

accounts = [
    " acct-001 ",
    "ACCT-001",
    "acct-002 ",
    " ACCT-003",
    "acct-004"
]

tickets = ["t-77", "T-77", "t-12", "T-45", "t-99"]

def random_timestamp():

    base = datetime(2026, 3, 1)
    delta = timedelta(minutes=random.randint(0, 100000))
    ts = base + delta

    formats = [
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        ts.strftime("%Y/%m/%d %H:%M"),
        ts.strftime("%Y-%m-%d %H:%M+00:00")
    ]

    return random.choice(formats)


def random_cost():

    cost = round(random.uniform(10, 2000), 2)

    formats = [
        f"₹ {cost}",
        f"{cost}",
        f"₹{cost}"
    ]

    return random.choice(formats)


def random_usage():

    val = random.randint(100, 20000)

    if random.random() < 0.3:
        return f"{val:,}"

    return val

rows = []

for i in range(NUM_ROWS):

    usage_id = f"U{6000+i}"

    row = {
        "Usage_ID": usage_id,
        "Account": random.choice(accounts),
        "TS": random_timestamp(),
        "Service": random.choice(services),
        "SKU": random.choice(sku_variants),
        "Usage": random_usage(),
        "Unit": random.choice(units),
        "Cost": random_cost(),
        "Region": random.choice(regions),
        "Ticket_ID": random.choice(tickets)
    }

    rows.append(row)

for _ in range(20):
    rows.append(random.choice(rows))

df = pd.DataFrame(rows)

df.to_csv(OUTPUT_FILE, index=False)

print("Dataset generated successfully!")
print("Rows:", len(df))
print("Saved to:", OUTPUT_FILE)