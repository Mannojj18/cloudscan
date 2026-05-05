import boto3
from datetime import datetime, timedelta, timezone


def get_cpu_average(instance_id, region):
    cw = boto3.client("cloudwatch", region_name=region)

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)

    try:
        response = cw.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "cpu_avg",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/EC2",
                            "MetricName": "CPUUtilization",
                            "Dimensions": [
                                {"Name": "InstanceId", "Value": instance_id}
                            ],
                        },
                        "Period": 3600,   # ✅ hourly data
                        "Stat": "Average",
                    },
                    "ReturnData": True,
                }
            ],
            StartTime=start,
            EndTime=end
        )

        results = response.get("MetricDataResults", [])

        if not results or not results[0].get("Values"):
            return 0

        values = results[0]["Values"]

        return round(sum(values) / len(values), 2)

    except Exception as e:
        print(f"[CPU ERROR] {instance_id} ({region}): {e}")
        return 0