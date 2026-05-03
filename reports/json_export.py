
import json
from pathlib import Path

def export_json(data):
    p = Path("reports/output")
    p.mkdir(parents=True, exist_ok=True)

    with open(p/"report.json","w") as f:
        json.dump(data,f,indent=2)
