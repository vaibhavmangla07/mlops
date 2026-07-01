import yaml
import numpy as np
from src.exception import ConfigurationError

def load_config(config_path):
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

    except FileNotFoundError:
        raise ConfigurationError(f"Config file not found: {config_path}")

    except yaml.YAMLError:
        raise ConfigurationError("Invalid YAML file.")

    if not isinstance(config, dict):
        raise ConfigurationError("Configuration must be a dictionary.")

    required_keys = ["seed", "window", "version"]

    for key in required_keys:
        if key not in config:
            raise ConfigurationError(f"Missing required key: {key}")

    np.random.seed(config["seed"])

    return config
