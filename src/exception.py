"""Lightweight custom exceptions for the batch signal pipeline."""


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""


class DataValidationError(Exception):
    """Raised when dataset validation fails."""