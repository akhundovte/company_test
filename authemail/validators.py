from django.core.validators import RegexValidator


class PasswordRegValidator(RegexValidator):
    """Только латинские символы и цифры."""
    regex = r'^[a-zA-Z0-9]+$'
    message = ''
    code = 'invalid'
    flags = 0


class UnicodeNameValidator(RegexValidator):
    """
    см. UnicodeUsernameValidator - contrib.auth.validators.py
    все цифры, символы верхнего, нижнего регистра и "_", ".", "+", "-", "@", пробел.
    """
    regex = r'^[\w.@+ -]+$'
    message = ''
    code = 'invalid'
    flags = 0
