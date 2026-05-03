
from datetime import datetime, timezone
from metrics.cpu_metrics import get_cpu_average
from pricing.aws_pricing_api import get_live_price
from analytics.trend_engine import fetch_trend

def analyze_instances(instances):
    findings = []

    for instance in instances:

        launch = datetime.fromisoformat(
            instance["launch_time"].replace("Z","+00:00")
        )

        age_hours = (
            datetime.now(timezone.utc) - launch
        ).total_seconds()/3600

        cpu = get_cpu_average(
            instance["instance_id"],
            instance["region"]
        )

        cost = get_live_price(instance["instance_type"])
        trend = fetch_trend(instance["instance_id"])

        if age_hours < 24:
            risk = "New"
        elif cpu < 2:
            risk = "High"
        elif cpu < 5:
            risk = "Medium"
        else:
            risk = "Low"

        findings.append({
            "instance_id": instance["instance_id"],
            "name": instance["name"],
            "cpu_avg": cpu,
            "monthly_cost": cost,
            "trend": trend,
            "risk": risk
        })

    return findings
