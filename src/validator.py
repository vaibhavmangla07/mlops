from pathlib import Path

import pandas as pd
from src.constants import REQUIRED_COLUMNS
from src.exception import DataValidationError


def validate_input_file(filepath: str) -> None:
    if not Path(filepath).exists():
        raise DataValidationError(f"Input file not found: {filepath}")


def load_and_validate_csv(filepath: str) -> pd.DataFrame:
    validate_input_file(filepath)
    try:
        df = pd.read_csv(filepath)
    except pd.errors.ParserError as e:
        raise DataValidationError(f"Invalid CSV format: {e}") from e

    if df.empty:
        raise DataValidationError("Input CSV file is empty (zero rows)")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise DataValidationError(
            f"Missing required column(s): {missing}. Found: {list(df.columns)}"
        )

    return df
