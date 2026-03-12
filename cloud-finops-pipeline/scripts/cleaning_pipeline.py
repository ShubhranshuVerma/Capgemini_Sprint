import pandas as pd
import numpy as np
import re

INPUT_FILE = "../data/raw/cloud_usage_raw.csv"
OUTPUT_FILE = "../data/cleaned/cloud_usage_cleaned.csv"

df = pd.read_csv(INPUT_FILE)


def clean_account(account):
    if pd.isna(account):
        return account
    account = account.strip().upper()
    return account


def normalize_ticket(ticket):
    if pd.isna(ticket):
        return ticket
    return ticket.strip().upper()


def normalize_region(region):
    if pd.isna(region):
        return region

    region = region.lower().strip()

    region = region.replace(" ", "-")

    mapping = {
        "ap-south-1": "ap-south-1",
        "ap-south-1": "ap-south-1",
        "us-east-1": "us-east-1"
    }

    return mapping.get(region, region)


def normalize_sku(sku):
    if pd.isna(sku):
        return sku

    sku = sku.upper()

    sku = sku.replace("_", "-")

    return sku


def clean_usage(val):
    if pd.isna(val):
        return val

    val = str(val).replace(",", "")

    return float(val)


def convert_to_seconds(usage, unit):

    if pd.isna(usage):
        return usage

    unit = str(unit).lower()

    if "sec" in unit:
        return usage

    if "min" in unit:
        return usage * 60

    if "hr" in unit:
        return usage * 3600

    return usage


def clean_cost(cost):

    if pd.isna(cost):
        return cost

    cost = str(cost)

    cost = re.sub(r"[₹,]", "", cost)

    return float(cost)


def normalize_timestamp(ts):

    try:
        return pd.to_datetime(ts, utc=True)
    except:
        return pd.NaT


df["Account"] = df["Account"].apply(clean_account)

df["Ticket_ID"] = df["Ticket_ID"].apply(normalize_ticket)

df["Region"] = df["Region"].apply(normalize_region)

df["SKU"] = df["SKU"].apply(normalize_sku)

df["Usage"] = df["Usage"].apply(clean_usage)

df["Usage_seconds"] = df.apply(
    lambda x: convert_to_seconds(x["Usage"], x["Unit"]),
    axis=1
)

df["Cost_INR"] = df["Cost"].apply(clean_cost)

df["TS_UTC"] = df["TS"].apply(normalize_timestamp)


df = df.drop_duplicates(
    subset=["Account", "TS", "SKU"]
)


mean_usage = df["Usage_seconds"].mean()
std_usage = df["Usage_seconds"].std()

threshold = mean_usage + (3 * std_usage)

df["Spike_Flag"] = df["Usage_seconds"] > threshold

df["Idle_Flag"] = df["Usage_seconds"] < 10

clean_df = df[
    [
        "Usage_ID",
        "Account",
        "TS_UTC",
        "Service",
        "SKU",
        "Usage_seconds",
        "Cost_INR",
        "Region",
        "Ticket_ID",
    ]
]

clean_df.to_csv(OUTPUT_FILE, index=False)

print("Cleaning pipeline complete")
print("Saved cleaned dataset:", OUTPUT_FILE)