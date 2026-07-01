class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""


class DataValidationError(Exception):
    """Raised when input data fails validation checks."""


class ProcessingError(Exception):
    """Raised when signal processing encounters an error."""
