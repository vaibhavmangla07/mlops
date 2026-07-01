#!/usr/bin/env python3
"""MLOps batch job: rolling-mean signal pipeline."""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def main():
    start_time = time.time()

    # ── CLI arguments ────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="MLOps batch job — rolling mean signal pipeline")
    parser.add_argument("--input", required=True, help="Path to input OHLCV CSV file")
    parser.add_argument("--config", required=True, help="Path to config YAML file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON file")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    args = parser.parse_args()

    # ── Logging setup ────────────────────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(args.log_file, mode="w"),
            logging.StreamHandler(sys.stderr),
        ],
    )
    logger = logging.getLogger(__name__)
    logger.info("Job started")

    version = "unknown"

    try:
        # ── Load and validate config ─────────────────────────────────────
        config_path = Path(args.config)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {args.config}")

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ValueError("Config file is empty or not a valid YAML mapping")

        for key in ("seed", "window", "version"):
            if key not in config:
                raise ValueError(f"Missing required config key: '{key}'")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logger.info(f"Config loaded and validated — seed={seed}, window={window}, version={version}")

        # ── Load and validate data ───────────────────────────────────────
        input_path = Path(args.input)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.input}")

        try:
            df = pd.read_csv(input_path)
        except pd.errors.ParserError as e:
            raise ValueError(f"Invalid CSV format: {e}") from e

        if df.empty:
            raise ValueError("Input CSV file is empty (zero rows)")

        if "close" not in df.columns:
            raise ValueError(f"Missing required 'close' column. Found columns: {list(df.columns)}")

        rows_loaded = len(df)
        logger.info(f"Data loaded — {rows_loaded} rows")

        # ── Compute rolling mean ─────────────────────────────────────────
        df["rolling_mean"] = df["close"].rolling(window).mean()
        logger.info("Rolling mean computed")

        # First (window-1) rows have NaN rolling mean — exclude them from signal and metrics.
        valid = df.dropna(subset=["rolling_mean"]).copy()

        # ── Generate signal ──────────────────────────────────────────────
        valid["signal"] = (valid["close"] > valid["rolling_mean"]).astype(int)
        logger.info("Signal generated")

        # ── Build metrics ────────────────────────────────────────────────
        signal_rate = round(valid["signal"].mean(), 4)
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_loaded,
            "metric": "signal_rate",
            "value": signal_rate,
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success",
        }

        logger.info(f"Metrics — signal_rate={signal_rate}, rows_processed={rows_loaded}, latency_ms={latency_ms}")
        logger.info("Job completed successfully")

    except Exception as e:
        logger.error(f"Job failed: {e}", exc_info=True)
        latency_ms = int((time.time() - start_time) * 1000)
        metrics = {
            "version": version,
            "status": "error",
            "error_message": str(e),
        }
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Error metrics written to {args.output}")
        sys.exit(1)

    # ── Write success metrics ────────────────────────────────────────────
    with open(args.output, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Metrics written to {args.output}")
    logger.info("Job ended")


if __name__ == "__main__":
    main()
