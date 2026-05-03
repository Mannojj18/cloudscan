import typer
import json
from pathlib import Path


def explain_command(instance_id: str):
    report = Path("reports/output/report.json")

    if not report.exists():
        typer.echo("Run scan first.")
        return

    data = json.loads(report.read_text())

    for item in data:
        if item["instance_id"] == instance_id:

            typer.echo(f"""
Instance: {item['name']}
CPU Avg: {item['cpu_avg']}
Cost: ${item['monthly_cost']}
Trend: {item.get('trend', 'N/A')}
Risk: {item['risk']}
""")
            return

    typer.echo("Instance not found.")