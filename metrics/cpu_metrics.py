
import boto3
from datetime import datetime, timedelta, timezone

def get_cpu_average(instance_id, region):
    cw = boto3.client("cloudwatch", region_name=region)

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)

    try:
        response = cw.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name":"InstanceId","Value":instance_id}],
            StartTime=start,
            EndTime=end,
            Period=86400,
            Statistics=["Average"]
        )

        points = response.get("Datapoints", [])

        if not points:
            return 0

        return round(
            sum(p["Average"] for p in points)/len(points),
            2
        )

    except Exception:
        return 0
