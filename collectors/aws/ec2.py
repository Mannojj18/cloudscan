
import boto3
from concurrent.futures import ThreadPoolExecutor

def fetch_region(region):
    ec2 = boto3.client("ec2", region_name=region)
    output = []

    try:
        response = ec2.describe_instances()

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):

                tags = {
                    t["Key"]: t["Value"]
                    for t in instance.get("Tags", [])
                }

                output.append({
                    "instance_id": instance.get("InstanceId"),
                    "instance_type": instance.get("InstanceType"),
                    "launch_time": str(instance.get("LaunchTime")),
                    "region": region,
                    "name": tags.get("Name", "Unnamed"),
                    "owner": tags.get("Owner", "unknown"),
                    "environment": tags.get("Environment", "unknown")
                })

    except Exception:
        return []

    return output

def fetch_ec2_instances():
    session = boto3.session.Session()
    # regions = session.get_available_regions("ec2")
    regions = ["eu-north-1"]

    output = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(fetch_region, regions)

    for result in results:
        output.extend(result)

    return output
