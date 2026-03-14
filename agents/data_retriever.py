import pandas as pd

def retrieve_logs(state):
    component = state["component"]

    df = pd.read_csv("data/sensor_logs.csv")
    filtered = df[df["equipment"] == component]

    logs = filtered.to_dict(orient="records")

    return {
        **state,
        "logs": logs
    }