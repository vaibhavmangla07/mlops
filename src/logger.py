"""Logging configuration for the batch signal pipeline."""

import logging
import sys


def setup_logger(log_file):
    """Configure and return a logger with dual output (file + console).

    Console output goes to stderr so stdout stays clean for metrics JSON
    output in Docker.

    Args:
        log_file: Path to the log file.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("batch_signal_pipeline")
    logger.setLevel(logging.INFO)

    # Clear existing handlers to prevent duplicates on repeated calls
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # File handler — captures full log for review
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)

    # Console handler — stderr so Docker stdout stays clean for metrics
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger