import json
from pathlib import Path
from typing import Any, Dict

from src.constants import DEFAULT_ENCODING


def write_json(data: Dict[str, Any], filepath: str) -> None:
    with open(filepath, "w", encoding=DEFAULT_ENCODING) as f:
        json.dump(data, f, indent=2)


def elapsed_ms(start_time: float, end_time: float) -> int:
    return int((end_time - start_time) * 1000)
