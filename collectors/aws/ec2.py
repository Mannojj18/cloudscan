import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_region(region):
    ec2 = boto3.client("ec2", region_name=region)
    output = []

    try:
        paginator = ec2.get_paginator("describe_instances")

        pages = paginator.paginate()
        for page in pages:
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):

                    tags = {
                        t["Key"]: t["Value"]
                        for t in instance.get("Tags", [])
                    }

                    output.append({
                        "instance_id": instance.get("InstanceId"),
                        "instance_type": instance.get("InstanceType"),
                        "launch_time": instance.get("LaunchTime").isoformat(),
                        "region": region,
                        "name": tags.get("Name", "Unnamed"),
                        "owner": tags.get("Owner", "unknown"),
                        "environment": tags.get("Environment", "unknown")
                    })

    except Exception as e:
        print(f"[ERROR] Region {region}: {e}")  # ✅ visible debugging

    return output


def fetch_ec2_instances():
    session = boto3.session.Session()

  
    regions = ["eu-north-1", "ap-south-1", "us-east-1"]  # Mumbai (safe region for you)

    output = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_region, r) for r in regions]

        for future in as_completed(futures):
            result = future.result()
            output.extend(result)

    return output