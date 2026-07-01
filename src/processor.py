"""Signal processing — data loading, rolling mean, and binary signal generation."""

import pandas as pd

from src.exception import DataValidationError


def load_data(input_file):
    """Load and validate the input CSV file.

    Args:
        input_file: Path to the CSV file.

    Returns:
        Validated DataFrame.

    Raises:
        DataValidationError: If the file is missing, invalid, empty, or lacks 'close'.
    """
    try:
        df = pd.read_csv(input_file)

    except FileNotFoundError:
        raise DataValidationError(f"Input file not found: {input_file}")

    except Exception:
        raise DataValidationError("Invalid CSV file.")

    if df.empty:
        raise DataValidationError("Input file is empty.")

    if "close" not in df.columns:
        raise DataValidationError("Missing required column: close")

    return df


def generate_signal(df, window):
    """Compute rolling mean and generate binary signal.

    Signal = 1 if close > rolling_mean, else 0.
    First (window-1) rows have NaN rolling mean and are excluded.

    Args:
        df: DataFrame with a 'close' column.
        window: Rolling window size.

    Returns:
        DataFrame with only valid (non-NaN) rows, including 'rolling_mean' and 'signal' columns.
    """
    df = df.copy()
    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    # Exclude first (window-1) rows where rolling mean is NaN.
    valid = df.dropna(subset=["rolling_mean"]).copy()
    valid["signal"] = (valid["close"] > valid["rolling_mean"]).astype(int)

    return valid