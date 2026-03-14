def summarize_logs(logs):
    if not logs:
        return "No logs found."

    return f"{len(logs)} log rows retrieved for analysis."