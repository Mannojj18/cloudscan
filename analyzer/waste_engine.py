from datetime import datetime, timezone
from metrics.cpu_metrics import get_cpu_average
from pricing.aws_pricing_api import get_live_price
from analytics.trend_engine import fetch_trend


def analyze_instances(instances):
    findings = []

    for instance in instances:

        # --- Parse launch time ---
        try:
            launch = datetime.fromisoformat(
                instance["launch_time"].replace("Z", "+00:00")
            )
        except Exception:
            launch = datetime.now(timezone.utc)

        # --- Age calculation ---
        age_hours = (
            datetime.now(timezone.utc) - launch
        ).total_seconds() / 3600

        # --- CPU usage ---
        cpu = get_cpu_average(
            instance["instance_id"],
            instance["region"]
        )

        # --- Real-time cost ---
        cost = get_live_price(
            instance["instance_type"],
            launch
        )

        # --- Trend ---
        trend = fetch_trend(instance["instance_id"])

        # --- Risk Engine (Industry Style) ---

        # CPU score
        if cpu < 2:
            cpu_score = 1
        elif cpu < 5:
            cpu_score = 0.7
        elif cpu < 20:
            cpu_score = 0.3
        else:
            cpu_score = 0

        # Age score
        if age_hours > 72:
            age_score = 1
        elif age_hours > 24:
            age_score = 0.6
        else:
            age_score = 0.2

        # Cost score
        if cost > 50:
            cost_score = 1
        elif cost > 20:
            cost_score = 0.7
        elif cost > 5:
            cost_score = 0.4
        else:
            cost_score = 0.1

        # Trend score
        if trend == "Increasing":
            trend_score = 1
        elif trend == "Stable":
            trend_score = 0.5
        else:
            trend_score = 0.2

        # Ownership score
        owner = instance.get("owner", "unknown")
        if owner == "unknown":
            ownership_score = 1
        else:
            ownership_score = 0.2

        # --- Final risk score ---
        risk_score = (
            cpu_score * 0.4 +
            age_score * 0.2 +
            cost_score * 0.2 +
            trend_score * 0.1 +
            ownership_score * 0.1
        )

        # --- Risk label ---
        if age_hours < 24:
            risk = "New"
        elif risk_score > 0.75:
            risk = "High"
        elif risk_score > 0.4:
            risk = "Medium"
        else:
            risk = "Low"

        # --- Optional: confidence ---
        confidence = round(risk_score * 100, 2)

        findings.append({
            "instance_id": instance["instance_id"],
            "name": instance["name"],
            "cpu_avg": cpu,
            "monthly_cost": cost,
            "trend": trend,
            "risk": risk,
            "confidence": confidence,
            "owner": owner,
            "age_hours": round(age_hours, 2)
        })

    return findings