import json

def create_success_metrics(config, rows_processed, signal_rate, latency_ms):
    return {
        "version": config["version"],
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": int(latency_ms),
        "seed": config["seed"],
        "status": "success",
    }


def create_error_metrics(version, error_message):
    return {
        "version": version,
        "status": "error",
        "error_message": str(error_message),
    }


def save_metrics(metrics, output_file):
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)
