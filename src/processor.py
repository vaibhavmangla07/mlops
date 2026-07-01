import pandas as pd
from src.exception import DataValidationError

def load_data(input_file):
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
    df = df.copy()
    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    # Exclude first (window-1) rows where rolling mean is NaN.
    valid = df.dropna(subset=["rolling_mean"]).copy()
    valid["signal"] = (valid["close"] > valid["rolling_mean"]).astype(int)

    return valid
