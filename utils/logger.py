import json
from datetime import datetime

def log_run(query, report):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "status": report.get("status"),
        "component": report.get("component"),
        "equipment_type": report.get("equipment_type"),
        "confidence_score": report.get("confidence_score"),
        "root_cause": report.get("root_cause"),
        "report": report
    }

    with open("run_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")