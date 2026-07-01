# Configuration keys that must be present in config.yaml
REQUIRED_CONFIG_KEYS: list[str] = ["seed", "window", "version"]

# Column that must exist in the input CSV
REQUIRED_COLUMNS: list[str] = ["close"]

# Logging
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(message)s"

# Metrics status values
SUCCESS_STATUS: str = "success"
ERROR_STATUS: str = "error"

# Metric name
SIGNAL_RATE_METRIC: str = "signal_rate"

# File encoding
DEFAULT_ENCODING: str = "utf-8"
