import logging
import sys
from pathlib import Path

from src.constants import LOG_FORMAT


def setup_logger(log_file: str, name: str = "batch_signal_pipeline") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT)

    # File handler — captures full log for review
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler — stderr so stdout stays clean for metrics output
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
