"""Metrics construction and persistence."""

import json


def create_success_metrics(config, rows_processed, signal_rate, latency_ms):
    """Build the success metrics dictionary.

    Args:
        config: Validated configuration dictionary.
        rows_processed: Total rows in the input dataset.
        signal_rate: Fraction of valid rows where signal == 1.
        latency_ms: Total wall-clock runtime in milliseconds.

    Returns:
        Metrics dictionary matching the required JSON schema.
    """
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
    """Build the error metrics dictionary.

    Args:
        version: Pipeline version (may be 'unknown' if config failed to load).
        error_message: Human-readable description of the failure.

    Returns:
        Error metrics dictionary.
    """
    return {
        "version": version,
        "status": "error",
        "error_message": str(error_message),
    }


def save_metrics(metrics, output_file):
    """Write metrics dictionary to a JSON file.

    Args:
        metrics: Metrics dictionary (success or error).
        output_file: Output file path.
    """
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)