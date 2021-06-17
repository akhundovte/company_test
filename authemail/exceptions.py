
class AuthError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class RegistrationError(AuthError):
    pass


class AccountConfirmError(AuthError):
    pass


class AuthenticateError(Exception):
    pass
