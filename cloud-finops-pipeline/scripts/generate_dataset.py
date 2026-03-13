import pandas as pd
import random
from datetime import datetime, timedelta, timezone

rows = 10000

services = ["Compute","Storage","Database","AI","Networking"]
regions = ["us-east-1","eu-west-1","ap-south-1"]
units = ["hours","seconds","minutes"]
pricing_types = ["on-demand","reserved","spot"]

departments = ["Engineering","Finance","Sales","Research"]
projects = ["Project-A","Project-B","Project-C"]

owners = ["alice","bob","charlie","david",None]
envs = ["prod","dev","test",None]

currencies = ["USD","EUR","INR"]

# different timezone offsets
timezones = [
    timezone.utc,
    timezone(timedelta(hours=5, minutes=30)),   # India
    timezone(timedelta(hours=-4)),              # US East
    timezone(timedelta(hours=1)),               # Europe
    timezone(timedelta(hours=9))                # Japan
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

        "Account": random.choice([
            "acct-001",
            "ACCT-002",
            " acct-003 "
        ]),

        "TS": random.choice([
            ts.isoformat(),                  # timezone timestamp
            ts.strftime("%Y/%m/%d %H:%M"),   # messy timestamp
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            "2026/03/10 25:05"               # invalid
        ]),

        "Service": random.choice(services),

        "SKU": random.choice([
            "vm_std_4",
            "VM-STD-4",
            "db_gp_2"
        ]),

        "Usage": round(usage,2),

        "Unit": random.choice(units),

        "Cost": random.choice([
            f"${round(cost,2)}",
            f"₹{round(cost,2)}"
        ]),

        "Currency": random.choice(currencies),

        "Region": random.choice([
            "US East 1",
            "us-east-1",
            "ap south 1"
        ]),

        "Free_Tier_Flag": random.choice([True,False]),

        "Tag_Owner": random.choice(owners),

        "Tag_Env": random.choice(envs),

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

        "Incident_ID": random.choice([
            f"I-{random.randint(1,100)}",
            None
        ]),

        "Price_Version": random.choice(["v1","v2","v3"]),

        "Pricing_Type": random.choice(pricing_types),

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

        "FX_Rate": random.uniform(70,90),

        "Purchase_Type": random.choice([
            "reserved",
            "spot",
            "on-demand"
        ])
    })

df = pd.DataFrame(data)

# introduce duplicates
df = pd.concat([df, df.sample(200)])

df.to_csv("../data/raw/cloud_case_study_dataset.csv", index=False)

print("Dataset generated successfully")