class JWTokenError(Exception):
    """Base class for all exceptions."""
    pass


class InvalidTokenError(JWTokenError):
    pass


class DecodeError(InvalidTokenError):
    pass


class ExpiredTokenError(InvalidTokenError):
    pass


class InvalidAuthError(InvalidTokenError):
    pass
