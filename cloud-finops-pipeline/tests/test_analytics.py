def test_dashboard_files_exist():

    files = [

        "dashboards/output/cost_trend.png",
        "dashboards/output/monthly_service_cost.png",
        "dashboards/output/chargeback.png",
        "dashboards/output/cost_anomalies.png",
        "dashboards/output/carbon_region.png",
        "dashboards/output/unit_cost.png",
        "dashboards/output/mttr_metrics.png",
        "dashboards/output/ticket_topics.png",
        "dashboards/output/security_events.png",
        "dashboards/output/cost_forecast.png"

    ]

    for f in files:

        with open(f, "rb") as file:
            assert file is not None