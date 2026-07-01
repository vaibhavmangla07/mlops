from typing import Any, Dict

from src.constants import ERROR_STATUS, SIGNAL_RATE_METRIC, SUCCESS_STATUS
from src.utils import write_json


def build_success_metrics(version: str, rows_processed: int, signal_rate: float, latency_ms: int, seed: int) -> Dict[str, Any]:
    return {
        "version": version,
        "rows_processed": rows_processed,
        "metric": SIGNAL_RATE_METRIC,
        "value": signal_rate,
        "latency_ms": latency_ms,
        "seed": seed,
        "status": SUCCESS_STATUS,
    }


def build_error_metrics(version: str, error_message: str) -> Dict[str, Any]:
    return {
        "version": version,
        "status": ERROR_STATUS,
        "error_message": error_message,
    }


def save_metrics(metrics: Dict[str, Any], filepath: str) -> None:
    write_json(metrics, filepath)
