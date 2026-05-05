from datetime import datetime, timezone

#  Define pricing table here
PRICE_PER_HOUR = {
    "t3.micro": 0.012,
    "t3.small": 0.023,
    "t3.medium": 0.046
}


def get_live_price(instance_type, launch_time):
    price_per_hour = PRICE_PER_HOUR.get(instance_type, 0.02)

    now = datetime.now(timezone.utc)
    runtime_hours = (now - launch_time).total_seconds() / 3600

    return round(price_per_hour * runtime_hours, 2)