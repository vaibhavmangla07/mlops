import pandas as pd
from src.exception import ProcessingError


def compute_rolling_mean(df: pd.DataFrame, window: int) -> pd.DataFrame:
    try:
        df = df.copy()
        df["rolling_mean"] = df["close"].rolling(window).mean()
        return df
    except Exception as e:
        raise ProcessingError(f"Failed to compute rolling mean: {e}") from e


def generate_signal(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Exclude rows where rolling mean is NaN (first window-1 rows).
        valid = df.dropna(subset=["rolling_mean"]).copy()
        valid["signal"] = (valid["close"] > valid["rolling_mean"]).astype(int)
        return valid
    except Exception as e:
        raise ProcessingError(f"Failed to generate signal: {e}") from e
