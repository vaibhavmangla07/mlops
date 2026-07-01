# Configuration loading, validation, and seed initialization.

from pathlib import Path
from typing import Any, Dict

import numpy as np
import yaml

from src.constants import REQUIRED_CONFIG_KEYS
from src.exception import ConfigurationError


def load_config(config_path: str) -> Dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise ConfigurationError(f"Config file not found: {config_path}")

    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in config file: {e}") from e

    if not isinstance(config, dict):
        raise ConfigurationError("Config file is empty or not a valid YAML mapping")

    # Validate required keys
    for key in REQUIRED_CONFIG_KEYS:
        if key not in config:
            raise ConfigurationError(f"Missing required config key: '{key}'")

    # Set random seed for deterministic execution
    np.random.seed(config["seed"])

    return config
