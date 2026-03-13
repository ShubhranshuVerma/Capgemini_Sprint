import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

TRANSFORMED = "../data/transformed/"
OUTPUT = "./output/"

def load_data():

    daily = pd.read_csv(TRANSFORMED+"daily_cost_cube.csv")
    monthly = pd.read_csv(TRANSFORMED+"monthly_cost_cube.csv")
    charge = pd.read_csv(TRANSFORMED+"chargeback.csv")
    anomalies = pd.read_csv(TRANSFORMED+"anomaly_spikes.csv")
    carbon = pd.read_csv(TRANSFORMED+"carbon_estimates.csv")
    unit = pd.read_csv(TRANSFORMED+"unit_cost_metrics.csv")
    incidents = pd.read_csv(TRANSFORMED+"incident_metrics.csv")
    topics = pd.read_csv(TRANSFORMED+"ticket_topics.csv")
    security = pd.read_csv(TRANSFORMED+"security_correlation.csv")
    forecast = pd.read_csv(TRANSFORMED+"cost_forecast.csv")

    return daily, monthly, charge, anomalies, carbon, unit, incidents, topics, security, forecast

def plot_cost_trend(daily):

    plt.figure(figsize=(10,6))

    sns.lineplot(
        data=daily,
        x="date",
        y="total_cost"
    )

    plt.title("Daily Cloud Cost Trend")

    plt.xticks(rotation=45)

    plt.savefig(OUTPUT+"cost_trend.png")

    plt.close()

def plot_monthly_cost(monthly):

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=monthly,
        x="Service",
        y="monthly_cost"
    )

    plt.title("Monthly Cost by Service")

    plt.savefig(OUTPUT+"monthly_service_cost.png")

    plt.close()

def plot_chargeback(charge):

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=charge,
        x="Account",
        y="total_cost"
    )

    plt.title("Chargeback by Account")

    plt.xticks(rotation=45)

    plt.savefig(OUTPUT+"chargeback.png")

    plt.close()

def plot_anomalies(anomalies):
    print("Number of anomalies:", len(anomalies))
    if anomalies.empty:
        print("No anomalies found")
        return

    plt.figure(figsize=(8,6))

    sns.scatterplot(
        data=anomalies,
        x="Usage_seconds",
        y="Cost_INR",
        hue="Service"
    )

    plt.title("Cost Anomaly Detection")

    plt.savefig(OUTPUT+"cost_anomalies.png")

    plt.close()

def plot_carbon(carbon):

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=carbon,
        x="Region",
        y="carbon"
    )

    plt.title("Carbon Footprint by Region")

    plt.savefig(OUTPUT+"carbon_region.png")

    plt.close()

def plot_unit_cost(unit):

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=unit,
        x="Service",
        y="avg_unit_cost"
    )

    plt.title("Average Unit Cost per Service")

    plt.savefig(OUTPUT+"unit_cost.png")

    plt.close()

def plot_incidents(incidents):

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=incidents,
        x="Service",
        y="avg_mttr"
    )

    plt.title("Average MTTR by Service")

    plt.savefig(OUTPUT+"mttr_metrics.png")

    plt.close()

def plot_ticket_topics(topics):

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=topics,
        x="Issue_Type",
        y="count"
    )

    plt.title("Support Ticket Topics")

    plt.savefig(OUTPUT+"ticket_topics.png")

    plt.close()

def plot_security(security):

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=security,
        x="Severity",
        y="event_count"
    )

    plt.title("Security Event Severity Distribution")

    plt.savefig(OUTPUT+"security_events.png")

    plt.close()

def plot_forecast(forecast):

    plt.figure(figsize=(10,6))

    sns.lineplot(
        data=forecast,
        x="month",
        y="Cost_INR",
        label="Actual"
    )

    sns.lineplot(
        data=forecast,
        x="month",
        y="forecast",
        label="Forecast"
    )

    plt.title("Cloud Cost Forecast")

    plt.xticks(rotation=45)

    plt.savefig(OUTPUT+"cost_forecast.png")

    plt.close()

def run_dashboard():

    daily, monthly, charge, anomalies, carbon, unit, incidents, topics, security, forecast = load_data()

    plot_cost_trend(daily)
    plot_monthly_cost(monthly)
    plot_chargeback(charge)
    plot_anomalies(anomalies)
    plot_carbon(carbon)
    plot_unit_cost(unit)
    plot_incidents(incidents)
    plot_ticket_topics(topics)
    plot_security(security)
    plot_forecast(forecast)

    print("Dashboard charts generated successfully")

if __name__ == "__main__":
    run_dashboard()