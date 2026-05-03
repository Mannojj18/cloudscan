
from collectors.aws.ec2 import fetch_ec2_instances
from analyzer.waste_engine import analyze_instances
from reports.json_export import export_json
from storage.postgres_store import save_scan

def run_scan():
    instances = fetch_ec2_instances()
    findings = analyze_instances(instances)

    export_json(findings)
    save_scan(findings)
