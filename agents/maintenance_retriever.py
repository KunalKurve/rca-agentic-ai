import pandas as pd

def retrieve_maintenance(state):
    component = state["component"]

    df = pd.read_csv("data/maintenance_history.csv")
    filtered = df[df["equipment"] == component]

    history = filtered.to_dict(orient="records")

    return {
        **state,
        "maintenance_history": history
    }