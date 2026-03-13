import pandas as pd
import numpy as np

INPUT = "../data/raw/cloud_case_study_dataset.csv"
OUTPUT = "../data/cleaned/cleaned_dataset.csv"

df = pd.read_csv(INPUT)

# 1 Account normalization
df["Account"] = df["Account"].astype(str).str.strip().str.upper()
df["Account"] = df["Account"].replace("NAN","UNKNOWN")

# 2 Timestamp normalization to UTC
df["TS"] = pd.to_datetime(df["TS"], errors="coerce", utc=True)
median_ts = df["TS"].dropna().median()
df["TS"] = df["TS"].fillna(median_ts)

# 3 Service canonical naming
df["Service"] = df["Service"].astype(str).str.title()

# SKU canonical naming
df["SKU"] = df["SKU"].astype(str).str.upper().str.replace("_","-")

# 4 Usage normalization
df["Usage"] = pd.to_numeric(df["Usage"], errors="coerce")
df["Usage"] = df["Usage"].fillna(df["Usage"].median())

df["Unit"] = df["Unit"].astype(str).str.lower()

def normalize_usage(row):
    u = row["Usage"]

    if row["Unit"] == "hours":
        return u * 3600

    if row["Unit"] == "minutes":
        return u * 60

    return u

df["Usage_seconds"] = df.apply(normalize_usage, axis=1)

# 5 Cost normalization
df["Cost"] = df["Cost"].astype(str)
df["Cost"] = df["Cost"].str.replace("$","",regex=False)
df["Cost"] = df["Cost"].str.replace("₹","",regex=False)
df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
df["Cost"] = df["Cost"].fillna(df["Cost"].median())

# 6 Region normalization
df["Region"] = df["Region"].astype(str).str.lower().str.replace(" ","-")

# 7 Duplicate detection
df["Duplicate_Flag"] = df.duplicated(subset=["Account","TS","SKU"])
df = df.drop_duplicates(subset=["Account","TS","SKU"])

# 8 Free tier adjustment
df.loc[df["Free_Tier_Flag"] == True, "Cost"] = 0

# 9 Usage spike detection
mean_usage = df["Usage_seconds"].mean()
std_usage = df["Usage_seconds"].std()
df["Spike_Flag"] = df["Usage_seconds"] > (mean_usage + 2 * std_usage)

# 10 Tag normalization
df["Tag_Owner"] = df["Tag_Owner"].astype(str).str.lower()
df["Tag_Env"] = df["Tag_Env"].astype(str).str.lower()

df["Tag_Owner"] = df["Tag_Owner"].replace("nan","unknown")
df["Tag_Env"] = df["Tag_Env"].replace("nan","unknown")

df["Tag_Owner_Missing"] = df["Tag_Owner"] == "unknown"
df["Tag_Env_Missing"] = df["Tag_Env"] == "unknown"

# 11 Resource ID validation
df["Resource_ID"] = df["Resource_ID"].fillna("UNKNOWN")
df["Resource_ID_Valid"] = df["Resource_ID"].str.startswith("R")

# Resource inventory mapping simulation
df["Resource_Type"] = df["SKU"].str.split("-").str[0]

# 12 PII masking
df["Ticket_Text"] = df["Ticket_Text"].str.replace(
    r"\b\d{10}\b",
    "[MASKED_PHONE]",
    regex=True
)

df["Ticket_Text"] = df["Ticket_Text"].str.replace(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "[MASKED_EMAIL]",
    regex=True
)

# 13 Incident linkage
df["Incident_ID"] = df["Incident_ID"].fillna("NONE")
df["Incident_Linked"] = df["Incident_ID"] != "NONE"

# 14 SKU price version validation
df["Price_Version"] = df["Price_Version"].fillna("v1")
df["Price_Version_Valid"] = df["Price_Version"].isin(["v1","v2","v3"])

# 15 FX conversion
df["FX_Rate"] = pd.to_numeric(df["FX_Rate"], errors="coerce")
df["FX_Rate"] = df["FX_Rate"].fillna(80)

df["Cost_INR"] = (df["Cost"] * df["FX_Rate"]).round(2)

# 16 Idle resource detection
df["Idle_Resource"] = df["Usage_seconds"] < 600

# 17 Pricing normalization
df["Pricing_Type"] = df["Pricing_Type"].astype(str).str.lower()

# 18 Cost allocation validation
df["Department"] = df["Department"].fillna("unknown")
df["Project"] = df["Project"].fillna("unknown")

df["Cost_Allocation_Valid"] = df["Department"] != "unknown"

# 19 SLA normalization
df["SLA_Event"] = df["SLA_Event"].fillna("NONE")

# 20 Log skew correction
df["Log_Skew_Seconds"] = pd.to_numeric(df["Log_Skew_Seconds"], errors="coerce")
df["Log_Skew_Seconds"] = df["Log_Skew_Seconds"].fillna(0)

df["TS"] = df["TS"] - pd.to_timedelta(df["Log_Skew_Seconds"], unit="s")

df.to_csv(OUTPUT,index=False)

print("Cleaning pipeline completed successfully")

# ----------------------------
# Final standardized dataset
# ----------------------------

final_columns = [
    "Usage_ID",
    "Account",
    "TS",
    "Service",
    "SKU",
    "Usage_seconds",
    "Cost_INR",
    "Region",
    "Ticket_ID"
]

final_df = df[final_columns].copy()

# rename TS → TS_UTC as required by case study
final_df = final_df.rename(columns={"TS": "TS_UTC"})

final_df.to_csv("../data/cleaned/final_cleaned_dataset.csv", index=False)

print("Final standardized dataset exported")