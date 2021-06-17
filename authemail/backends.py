from .models import User

from rest_framework import authentication, exceptions

from .token import JWT_HEADER_NAME, get_token_identity, JWTokenError


class JWTAuthentication(authentication.BaseAuthentication):
    jwt_header_name = JWT_HEADER_NAME

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        parts_header = authentication.get_authorization_header(request).split()

        if not parts_header or parts_header[0].lower() != self.jwt_header_name.lower().encode():
            return None

        if len(parts_header) == 1:
            msg = ('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(parts_header) > 2:
            msg = ('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = parts_header[1].decode()
        except UnicodeError:
            msg = ('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            user_id = get_token_identity(token)
        except JWTokenError as e:
            raise exceptions.AuthenticationFailed(str(e))

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exists.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, token)

    def authenticate_header(self, request):
        return self.jwt_header_name
