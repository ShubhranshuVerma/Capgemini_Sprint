import pandas as pd
import random
from datetime import datetime, timedelta, timezone

rows = 10000

services = ["Compute","Storage","Database","AI","Networking"]

regions = [
    "US East 1",
    "us-east-1",
    "ap south 1",
    "eu-west-1"
]

units = ["hours","minutes","seconds"]

pricing_types = ["on-demand","reserved","spot"]

purchase_types = ["reserved","spot","on-demand"]

departments = ["Engineering","Finance","Sales","Research",None]

projects = ["Project-A","Project-B","Project-C",None]

owners = ["alice","bob","charlie","david",None]

envs = ["prod","dev","test",None]

currencies = ["USD","EUR","INR"]

severity_levels = ["LOW","MEDIUM","HIGH",None]

# timezone offsets
timezones = [
    timezone.utc,
    timezone(timedelta(hours=5,minutes=30)),
    timezone(timedelta(hours=-4)),
    timezone(timedelta(hours=1)),
    timezone(timedelta(hours=9))
]

start = datetime(2026,1,1)

data = []

for i in range(rows):

    tz = random.choice(timezones)

    ts = start + timedelta(minutes=random.randint(0,500000))

    ts = ts.replace(tzinfo=tz)

    usage = random.uniform(1,500)

    if random.random() < 0.03:
        usage *= 20

    cost = usage * random.uniform(0.2,2)

    data.append({

        "Usage_ID": f"U{i}",

        # account variations
        "Account": random.choice([
            "acct-001",
            "ACCT-002",
            " acct003 ",
            "acct001"
        ]),

        # timestamp variations
        "TS": random.choice([
            ts.isoformat(),
            ts.strftime("%Y/%m/%d %H:%M"),
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            "2026/03/10 25:05"
        ]),

        "Service": random.choice(services),

        # inconsistent SKU naming
        "SKU": random.choice([
            "vm_std_4",
            "VM-STD-4",
            "db_gp_2",
            "DB-GP-2"
        ]),

        "Usage": round(usage,2),

        "Unit": random.choice(units),

        # cost with symbols
        "Cost": random.choice([
            f"${round(cost,2)}",
            f"₹{round(cost,2)}",
            f"{round(cost,2)}"
        ]),

        "Currency": random.choice(currencies),

        "Region": random.choice(regions),

        "Free_Tier_Flag": random.choice([True,False]),

        "Tag_Owner": random.choice(owners),

        "Tag_Env": random.choice(envs),

        # resource ids valid and invalid
        "Resource_ID": random.choice([
            f"R{random.randint(1000,9999)}",
            f"resource-{random.randint(1000,9999)}"
        ]),

        "Ticket_ID": f"T-{random.randint(1,200)}",

        "Ticket_Text": random.choice([
            f"Customer phone {random.randint(6000000000,9999999999)} reported outage",
            "User email john@example.com cannot login",
            "Customer reported latency issue"
        ]),

        "Severity": random.choice(severity_levels),

        "Incident_ID": random.choice([
            f"I-{random.randint(1,100)}",
            None
        ]),

        "Price_Version": random.choice(["v1","v2","v3",None]),

        "Pricing_Type": random.choice(pricing_types),

        "Purchase_Type": random.choice(purchase_types),

        "Department": random.choice(departments),

        "Project": random.choice(projects),

        "SLA_Event": random.choice([
            "NONE",
            "OUTAGE",
            "DEGRADED"
        ]),

        "Log_Skew_Seconds": random.choice([
            random.randint(0,120),
            None
        ]),

        "FX_Rate": random.uniform(70,90)
    })

df = pd.DataFrame(data)

# create duplicate rows intentionally
df = pd.concat([df, df.sample(200)])

df.to_csv("../data/raw/cloud_case_study_dataset.csv", index=False)

print("Dataset generated successfully")