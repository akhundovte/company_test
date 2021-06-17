import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from .exceptions_token import (
    JWTokenError, InvalidTokenError,
    DecodeError, ExpiredTokenError,
    )

__all__ = (
    'create_access_token', 'get_token_identity',
    'JWTokenError', 'JWT_HEADER_NAME',
    )

JWT_SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_HEADER_NAME = 'Bearer'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)


def create_access_token(user_id, secret=None, algorithm=None):
    """Создание access токена."""
    timedelta = JWT_ACCESS_TOKEN_EXPIRES
    token_data = {'user_id': user_id}
    expires, _ = _get_expires(timedelta)
    return _encode_token(token_data, expires, secret, algorithm)


def get_token_identity(access_token):
    """Получение user_id из access токена."""
    payload = _decode_token(access_token)
    user_id = payload.get('user_id')
    if not user_id:
        raise InvalidTokenError('ID пользователя не найден в теле токена.')
    return user_id


def _get_expires(timedelta):
    now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    expires_dt = now_utc + timedelta
    expires = int(expires_dt.timestamp())
    return expires, expires_dt


def _encode_token(token_data, expires, secret=None, algorithm=None):
    if algorithm is None:
        algorithm = JWT_ALGORITHM
    if secret is None:
        secret = JWT_SECRET_KEY

    token_data['exp'] = expires
    encoded_token = jwt.encode(token_data, secret, algorithm)
    return encoded_token


def _decode_token(token, secret=None, algorithms=None):
    if algorithms is None:
        algorithms = [JWT_ALGORITHM]
    if secret is None:
        secret = JWT_SECRET_KEY

    try:
        payload = jwt.decode(
            token, secret,
            verify=True,
            algorithms=algorithms,
            options={'verify_exp': False}
            )
    except jwt.ExpiredSignatureError as e:
        # если сигнатура не соответствует данным
        raise InvalidTokenError(str(e))
    except jwt.InvalidTokenError as e:
        # базовая ошибка
        raise InvalidTokenError(str(e))

    expires = payload.get('exp')
    if not expires:
        raise InvalidTokenError('Срок действия не найден в теле токена.')

    try:
        expires = int(expires)
    except ValueError:
        raise DecodeError(
            'Срок действия (exp) должен быть целым числом.')

    now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    if int(now_utc.timestamp()) > expires:
        raise ExpiredTokenError(
            'Ошибка при проверке токена: Сессия просрочена.')

    return payload
