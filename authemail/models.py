from enum import IntEnum

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from .exceptions import AuthenticateError
from .token import create_access_token


class UserManager(BaseUserManager):

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            raise e
        else:
            if not user.check_password(password):
                raise AuthenticateError('Введен неверный пароль.')
            return user


class RoleConst(IntEnum):
    USER = 0
    ADMIN = 1


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        (RoleConst.USER, 'USER'),
        (RoleConst.ADMIN, 'ADMIN'),
        )

    is_staff = False

    name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    email = models.EmailField(verbose_name='Почта', unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=RoleConst.USER)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def can_authenticate(self):
        return self.is_active

    @property
    def is_admin(self):
        return self.role == RoleConst.ADMIN

    @property
    def is_user(self):
        return self.role == RoleConst.USER

    @property
    def token(self):
        return create_access_token(self.pk)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'account_user'
