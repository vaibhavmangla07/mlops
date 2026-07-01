import argparse
import sys
import time

from src.config import load_config
from src.exception import ConfigurationError, DataValidationError, ProcessingError
from src.logger import setup_logger
from src.metrics import build_error_metrics, build_success_metrics, save_metrics
from src.processor import compute_rolling_mean, generate_signal
from src.utils import elapsed_ms
from src.validator import load_and_validate_csv


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch Signal Pipeline — rolling mean signal generation"
    )
    parser.add_argument("--input", required=True, help="Path to input OHLCV CSV file")
    parser.add_argument("--config", required=True, help="Path to config YAML file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON file")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    return parser.parse_args()


def main() -> None:
    """Run the batch signal pipeline end-to-end."""
    start_time = time.time()
    args = parse_args()

    # Initialize logger
    logger = setup_logger(log_file=args.log_file)
    logger.info("Job started")

    version = "unknown"

    try:
        # Load and validate configuration
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]
        logger.info(f"Config loaded — seed={seed}, window={window}, version={version}")

        # Load and validate input data
        df = load_and_validate_csv(args.input)
        rows_processed = len(df)
        logger.info(f"Data loaded — {rows_processed} rows")

        # Compute rolling mean
        df = compute_rolling_mean(df, window)
        logger.info("Rolling mean computed")

        # Generate binary signal
        valid = generate_signal(df)
        logger.info("Signal generated")

        # Calculate metrics
        signal_rate = round(valid["signal"].mean(), 4)
        latency_ms = elapsed_ms(start_time, time.time())

        metrics = build_success_metrics(
            version=version,
            rows_processed=rows_processed,
            signal_rate=signal_rate,
            latency_ms=latency_ms,
            seed=seed,
        )
        logger.info(
            f"Metrics — signal_rate={signal_rate}, "
            f"rows_processed={rows_processed}, latency_ms={latency_ms}"
        )

        # Write metrics
        save_metrics(metrics, args.output)
        logger.info(f"Metrics written to {args.output}")
        logger.info("Job completed — status=success")

    except (ConfigurationError, DataValidationError, ProcessingError) as e:
        logger.error(f"Job failed: {e}")
        metrics = build_error_metrics(version=version, error_message=str(e))
        save_metrics(metrics, args.output)
        logger.info(f"Error metrics written to {args.output}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        metrics = build_error_metrics(version=version, error_message=str(e))
        save_metrics(metrics, args.output)
        logger.info(f"Error metrics written to {args.output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
