import pandas as pd
import numpy as np
import re

INPUT = "../data/raw/cloud_case_study_dataset.csv"
OUTPUT = "../data/cleaned/cleaned_dataset.csv"

df = pd.read_csv(INPUT)

# --------------------------------------------------
# 1. Account normalization + master mapping
# --------------------------------------------------

df["Account"] = df["Account"].astype(str).str.strip().str.upper()
df["Account"] = df["Account"].str.replace("-", "", regex=False)

account_map = {
    "ACCT001": "ACCT-001",
    "ACCT002": "ACCT-002",
    "ACCT003": "ACCT-003"
}

df["Account"] = df["Account"].replace(account_map)

# --------------------------------------------------
# 2. Timestamp normalization (UTC with offset parsing)
# --------------------------------------------------

df["TS"] = pd.to_datetime(df["TS"], errors="coerce", utc=True)

median_ts = df["TS"].dropna().median()
df["TS"] = df["TS"].fillna(median_ts)

# --------------------------------------------------
# 3. Service/SKU canonical naming
# --------------------------------------------------

df["Service"] = (
    df["Service"]
    .astype(str)
    .str.strip()
    .str.lower()
)

service_catalog = {
    "compute": "Compute",
    "storage": "Storage",
    "database": "Database",
    "ai": "AI",
    "networking": "Networking"
}

df["Service"] = df["Service"].replace(service_catalog)

df["SKU"] = (
    df["SKU"]
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace("_", "-", regex=False)
)

# --------------------------------------------------
# 4. Usage unit normalization → seconds
# --------------------------------------------------

df["Usage"] = pd.to_numeric(df["Usage"], errors="coerce")

df["Unit"] = df["Unit"].astype(str).str.lower()

unit_map = {
    "sec": "seconds",
    "second": "seconds",
    "seconds": "seconds",
    "min": "minutes",
    "minute": "minutes",
    "minutes": "minutes",
    "hr": "hours",
    "hour": "hours",
    "hours": "hours"
}

df["Unit"] = df["Unit"].replace(unit_map)

df["Usage_seconds"] = np.where(
    df["Unit"] == "hours", df["Usage"] * 3600,
    np.where(
        df["Unit"] == "minutes", df["Usage"] * 60,
        df["Usage"]
    )
)

# --------------------------------------------------
# 5. Cost currency normalization
# --------------------------------------------------

df["Cost"] = df["Cost"].astype(str)

df["Cost"] = (
    df["Cost"]
    .str.replace("$", "", regex=False)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")

# --------------------------------------------------
# 6. Region normalization
# --------------------------------------------------

df["Region"] = (
    df["Region"]
    .astype(str)
    .str.lower()
    .str.replace(" ", "-", regex=False)
)

region_map = {
    "useast1": "us-east-1",
    "us-east1": "us-east-1",
    "apsouth1": "ap-south-1",
    "ap-south1": "ap-south-1"
}

df["Region"] = df["Region"].replace(region_map)

# --------------------------------------------------
# 7. Duplicate removal
# --------------------------------------------------

df["Duplicate_Flag"] = df.duplicated(["Account", "TS", "SKU"])
df = df.drop_duplicates(["Account", "TS", "SKU"])

# --------------------------------------------------
# 8. Free tier tagging
# --------------------------------------------------

df["Free_Tier_Flag"] = df["Free_Tier_Flag"].fillna(False)

df.loc[df["Free_Tier_Flag"] == True, "Cost"] = 0

# --------------------------------------------------
# 9. Spike detection
# --------------------------------------------------

mean_usage = df["Usage_seconds"].mean()
std_usage = df["Usage_seconds"].std()

df["Spike_Flag"] = df["Usage_seconds"] > (mean_usage + 2 * std_usage)

# --------------------------------------------------
# 10. Tag normalization
# --------------------------------------------------

df["Tag_Owner"] = df["Tag_Owner"].fillna("unknown").str.lower()
df["Tag_Env"] = df["Tag_Env"].fillna("unknown").str.lower()

# --------------------------------------------------
# 11. Resource ID validation + format normalization
# --------------------------------------------------

df["Resource_ID"] = df["Resource_ID"].fillna("UNKNOWN")

# remove prefixes like "resource-"
df["Resource_ID"] = (
    df["Resource_ID"]
    .astype(str)
    .str.upper()
    .str.replace("RESOURCE-", "", regex=False)
    .str.replace("R-", "", regex=False)
    .str.replace("R", "", regex=False)
)

# extract numeric part
df["Resource_ID"] = df["Resource_ID"].str.extract(r"(\d+)")

# rebuild standardized ID
df["Resource_ID"] = "R-" + df["Resource_ID"].fillna("0000")

# validation flag
df["Resource_ID_Valid"] = df["Resource_ID"].str.match(r"R-\d+")

# inventory mapping example
df["Resource_Type"] = df["SKU"].str.split("-").str[0]

# --------------------------------------------------
# 12. PII masking
# --------------------------------------------------

df["Ticket_Text"] = df["Ticket_Text"].fillna("no ticket")

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

df["Severity"] = df["Severity"].fillna("LOW")

# --------------------------------------------------
# 13. Incident linkage
# --------------------------------------------------

df["Incident_ID"] = df["Incident_ID"].fillna("NONE")

df["Incident_Linked"] = df["Incident_ID"] != "NONE"

# --------------------------------------------------
# 14. SKU price version validation
# --------------------------------------------------

df["Price_Version"] = df["Price_Version"].fillna("v1")

df["Price_Version_Valid"] = df["Price_Version"].isin(["v1", "v2", "v3"])

# --------------------------------------------------
# 15. Cross-account FX conversion
# --------------------------------------------------

df["FX_Rate"] = pd.to_numeric(df["FX_Rate"], errors="coerce")

df["FX_Rate"] = df["FX_Rate"].fillna(80)

df["Cost_INR"] = (df["Cost"] * df["FX_Rate"]).round(2)

# --------------------------------------------------
# 16. Idle resource detection
# --------------------------------------------------

df["Idle_Resource"] = df["Usage_seconds"] < 600

# --------------------------------------------------
# 17. Reserved / spot / on-demand normalization
# --------------------------------------------------

df["Pricing_Type"] = df["Pricing_Type"].astype(str).str.lower().str.strip()
df["Purchase_Type"] = df["Purchase_Type"].astype(str).str.lower().str.strip()

# --------------------------------------------------
# 18. Cost allocation validation
# --------------------------------------------------

df["Department"] = df["Department"].fillna("unknown")
df["Project"] = df["Project"].fillna("unknown")

df["Cost_Allocation_Valid"] = df["Department"] != "unknown"

# --------------------------------------------------
# 19. SLA event marking
# --------------------------------------------------

df["SLA_Event"] = df["SLA_Event"].fillna("NONE")

# --------------------------------------------------
# 20. Log skew correction
# --------------------------------------------------

df["Log_Skew_Seconds"] = pd.to_numeric(
    df["Log_Skew_Seconds"], errors="coerce"
)

df["Log_Skew_Seconds"] = df["Log_Skew_Seconds"].fillna(0)

df["TS"] = df["TS"] - pd.to_timedelta(df["Log_Skew_Seconds"], unit="s")

# --------------------------------------------------
# Save cleaned dataset
# --------------------------------------------------

df.to_csv(OUTPUT, index=False)

print("All 20 cleaning scenarios executed successfully.")

# --------------------------------------------------
# Final standardized dataset (case-study format)
# --------------------------------------------------

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

final_df = final_df.rename(columns={"TS": "TS_UTC"})

final_df.to_csv("../data/cleaned/final_cleaned_dataset.csv", index=False)

print("Final standardized dataset exported.")