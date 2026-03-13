import pandas as pd
import numpy as np
import re
from datetime import timedelta

RAW = "../data/raw/"
CLEAN = "../data/cleaned/"

def load_datasets():

    usage = pd.read_csv(RAW+"usage_raw.csv")
    inventory = pd.read_csv(RAW+"resource_inventory.csv")
    tickets = pd.read_csv(RAW+"tickets_metadata.csv")
    incidents = pd.read_csv(RAW+"incidents.csv")
    pricing = pd.read_csv(RAW+"pricing_catalog.csv")
    sla = pd.read_csv(RAW+"sla_events.csv")
    security = pd.read_csv(RAW+"security_events.csv")

    return usage, inventory, tickets, incidents, pricing, sla, security

#1.

def clean_accounts(df):
    df["Account"] = df["Account"].str.strip().str.upper()
    return df

#2.

def normalize_timestamp(df, column):

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce",
        utc=True,
        format="mixed"
    )

    return df

#3.

def normalize_service(df):

    df["Service"] = (
        df["Service"]
        .str.strip()
        .str.title()
    )

    return df

#4.

def normalize_sku(df):

    df["SKU"] = (
        df["SKU"]
        .str.upper()
        .str.replace("_","-",regex=False)
    )

    return df

#5.

def normalize_usage(df):

    df["Usage"] = df["Usage"].astype(str).str.replace(",","")
    df["Usage"] = df["Usage"].astype(float)

    def convert(row):

        unit = str(row["Unit"]).lower()

        if "sec" in unit:
            return row["Usage"]

        if "min" in unit:
            return row["Usage"] * 60

        if "hr" in unit:
            return row["Usage"] * 3600

        return row["Usage"]

    df["Usage_seconds"] = df.apply(convert, axis=1)

    return df

#6.

def normalize_cost(df):

    df["Cost_INR"] = (
        df["Cost"]
        .astype(str)
        .str.replace("₹","",regex=False)
        .str.replace(",","",regex=False)
        .astype(float)
    )

    return df

#7.

def normalize_region(df):

    df["Region"] = (
        df["Region"]
        .str.lower()
        .str.replace(" ","-",regex=False)
    )

    return df

#8.

def remove_duplicates(df):

    return df.drop_duplicates(
        subset=["Account","TS","SKU"]
    )

#9.


def tag_free_tier(df):

    df["Free_Tier"] = df["Cost_INR"] == 0

    return df

#10.

def detect_spikes(df):

    mean = df["Usage_seconds"].mean()
    std = df["Usage_seconds"].std()

    threshold = mean + 2*std

    df["Spike_Flag"] = df["Usage_seconds"] > threshold

    return df

#11.

def normalize_tags(df):

    df["Service"] = df["Service"].str.title()
    df["Region"] = df["Region"].str.lower()

    return df

#12.

def validate_resource_ids(df):

    df["Valid_Resource"] = df["Resource_ID"].str.startswith("R")

    return df

#13.

def mask_pii(df):

    df["Description"] = df["Description"].str.replace(
        r"\b\d{10}\b",
        "[MASKED]",
        regex=True
    )

    return df

#14.

def prepare_incidents(df):

    df["Start_TS"] = pd.to_datetime(df["Start_TS"],utc=True)
    df["End_TS"] = pd.to_datetime(df["End_TS"],utc=True)

    df["Duration_minutes"] = (
        df["End_TS"] - df["Start_TS"]
    ).dt.total_seconds()/60

    return df

#15.

def version_pricing(df):

    df["Effective_Date"] = pd.to_datetime(df["Effective_Date"])

    df = df.sort_values("Effective_Date")

    return df

#16.

def normalize_currency(df):

    df["Currency"] = df["Currency"].str.upper()

    return df

#17.

def detect_idle(df):

    df["Idle"] = df["Status"].str.lower() == "stopped"

    return df

#18.

def normalize_pricing_model(df):

    df["Pricing_Model"] = df["Pricing_Model"].str.lower()

    return df

#19.

def normalize_sla(df):

    df["Event_TS"] = pd.to_datetime(
        df["Event_TS"],
        errors="coerce",
        utc=True,
        format="mixed"
    )

    return df

#20.

def correct_time_skew(df):

    df["Event_TS"] = pd.to_datetime(
        df["Event_TS"],
        errors="coerce",
        utc=True,
        format="mixed"
    )

    return df

def run_pipeline():

    usage, inventory, tickets, incidents, pricing, sla, security = load_datasets()

    usage = clean_accounts(usage)
    usage = normalize_service(usage)
    usage = normalize_sku(usage)
    usage = normalize_usage(usage)
    usage = normalize_cost(usage)
    usage = normalize_region(usage)

    usage = normalize_timestamp(usage,"TS")

    usage = remove_duplicates(usage)

    usage = tag_free_tier(usage)
    usage = detect_spikes(usage)

    inventory = clean_accounts(inventory)
    inventory = normalize_tags(inventory)
    inventory = validate_resource_ids(inventory)
    inventory = detect_idle(inventory)
    inventory = normalize_pricing_model(inventory)

    tickets = mask_pii(tickets)

    incidents = prepare_incidents(incidents)

    pricing = version_pricing(pricing)
    pricing = normalize_currency(pricing)

    sla = normalize_sla(sla)

    security = correct_time_skew(security)

    usage_clean = usage[
        [
        "Usage_ID",
        "Account",
        "TS",
        "Service",
        "SKU",
        "Usage_seconds",
        "Cost_INR",
        "Region",
        "Ticket_ID",
        "Spike_Flag"
        ]
    ]

    usage_clean.to_csv(CLEAN+"usage_cleaned.csv",index=False)

    inventory.to_csv(CLEAN+"inventory_cleaned.csv",index=False)
    tickets.to_csv(CLEAN+"tickets_cleaned.csv",index=False)
    incidents.to_csv(CLEAN+"incidents_cleaned.csv",index=False)
    pricing.to_csv(CLEAN+"pricing_cleaned.csv",index=False)
    sla.to_csv(CLEAN+"sla_cleaned.csv",index=False)
    security.to_csv(CLEAN+"security_cleaned.csv",index=False)

    print("All 20 cleaning scenarios executed successfully")


if __name__ == "__main__":
    run_pipeline()

