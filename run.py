"""Batch Signal Pipeline — main entry point.

Orchestrates the full batch job: load config → validate data → process → write metrics.

Usage:
    python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
"""

import argparse
import json
import sys
import time

from src.config import load_config
from src.exception import ConfigurationError, DataValidationError
from src.logger import setup_logger
from src.metrics import create_success_metrics, create_error_metrics, save_metrics
from src.processor import load_data, generate_signal


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Batch Signal Pipeline")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    return parser.parse_args()


def main():
    """Run the batch signal pipeline end-to-end."""
    start_time = time.time()
    args = parse_arguments()

    # Initialize logger
    logger = setup_logger(args.log_file)
    logger.info("Job started")

    version = "unknown"

    try:
        # Load and validate configuration
        config = load_config(args.config)
        version = config["version"]
        logger.info(f"Config loaded and validated — seed={config['seed']}, window={config['window']}, version={version}")

        # Load and validate input data
        df = load_data(args.input)
        rows_processed = len(df)
        logger.info(f"Data loaded — {rows_processed} rows")

        # Compute rolling mean and generate signal
        valid = generate_signal(df, config["window"])
        logger.info("Rolling mean computed")
        logger.info("Signal generated")

        # Calculate metrics
        signal_rate = valid["signal"].mean()
        latency_ms = (time.time() - start_time) * 1000

        metrics = create_success_metrics(
            config=config,
            rows_processed=rows_processed,
            signal_rate=signal_rate,
            latency_ms=latency_ms,
        )
        logger.info(
            f"Metrics — signal_rate={round(signal_rate, 4)}, "
            f"rows_processed={rows_processed}, latency_ms={int(latency_ms)}"
        )

        # Write metrics
        save_metrics(metrics, args.output)
        logger.info(f"Metrics written to {args.output}")
        logger.info("Job completed — status=success")

    except (ConfigurationError, DataValidationError) as e:
        logger.error(f"Job failed: {e}")
        metrics = create_error_metrics(version=version, error_message=str(e))
        save_metrics(metrics, args.output)
        logger.info(f"Error metrics written to {args.output}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        metrics = create_error_metrics(version=version, error_message=str(e))
        save_metrics(metrics, args.output)
        logger.info(f"Error metrics written to {args.output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
