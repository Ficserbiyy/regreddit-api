
class AuthenticationError(Exception):
    """Raised when authentication is required or credentials are invalid."""

class ValidationError(Exception):
    """Raised when user input is invalid."""

class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""