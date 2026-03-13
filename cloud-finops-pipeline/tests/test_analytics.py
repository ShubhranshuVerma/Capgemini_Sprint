def test_dashboard_files():

    files = [

        "dashboards/output/daily_cost_trend.png",
        "dashboards/output/monthly_cost.png",
        "dashboards/output/cost_anomalies.png"

    ]

    for f in files:
        open(f)