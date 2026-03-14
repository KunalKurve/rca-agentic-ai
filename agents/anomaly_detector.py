def detect_anomalies(state):
    logs = state.get("logs", [])
    anomalies = []

    for row in logs:
        if row["pressure"] > 140:
            anomalies.append(f"High pressure at {row['timestamp']}: {row['pressure']}")
        if row["temp"] > 190:
            anomalies.append(f"High temperature at {row['timestamp']}: {row['temp']}")
        if row["vibration"] > 1.5:
            anomalies.append(f"High vibration at {row['timestamp']}: {row['vibration']}")
        if str(row["status"]).lower() == "tripped":
            anomalies.append(f"Trip event at {row['timestamp']}")

    return {
        **state,
        "anomalies": anomalies
    }