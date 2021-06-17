from rest_framework import serializers
from rest_framework.settings import api_settings

from django.contrib.auth import password_validation
from django.core.validators import EmailValidator
from django.db import Error as DBError
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User
from .validators import PasswordRegValidator, UnicodeNameValidator
from .exceptions import RegistrationError, AuthenticateError


class ErrorMsgMixin:
    error_messages_fields = {
        'email': {
            'required': "Введите E-mail.",
            'invalid': "Введите корректный E-mail.",
            'max_length': ("Превышено допустимое количество символов"
                           " (%(limit_value)s) в E-mail."),
            },
        'password': {
            'required': "Введите пароль.",
            'max_length': ("Превышено допустимое количество символов"
                           " (%(limit_value)s) в пароле."),
            },
        }


class AccountCreationSerializer(ErrorMsgMixin, serializers.Serializer):
    """Сериализатор создания аккаунта."""
    error_messages_fields = {
        'name': {
            'invalid': "Имя содержит запрещенные символы.",
            'max_length': ("Превышено допустимое количество символов"
                           " (%(limit_value)s) в имени."),
            },
        'email': {
            **ErrorMsgMixin.error_messages_fields['email'],
            'unique': "Пользователь с такой почтой уже существует.",
            },
        'password': {
            **ErrorMsgMixin.error_messages_fields['password'],
            'min_length': "Пароль должен быть не менее %(min_length)d символов.",
            'invalid': "Пароль должен состоять из латинских букв или цифр.",
            'entirely_numeric': "Пароль не может состоять только из цифр.",
            },
        }
    password_validators = [
        password_validation.UserAttributeSimilarityValidator(
            user_attributes=('name', 'email')),
        password_validation.CommonPasswordValidator(),
        password_validation.MinimumLengthValidator(),
        password_validation.NumericPasswordValidator(),
        ]

    name = serializers.CharField(
        label='Имя',
        max_length=127,
        required=False,
        allow_blank=True,
        default='',
        validators=(UnicodeNameValidator(
            message=error_messages_fields['name']['invalid']), ),
        error_messages={
            'max_length': error_messages_fields['name']['max_length'],
            }
        )

    email = serializers.EmailField(
        label="E-mail",
        max_length=255,
        required=True,
        error_messages={
            'required': error_messages_fields['email']['required'],
            'blank': error_messages_fields['email']['required'],
            'max_length': error_messages_fields['email']['max_length'],
            'invalid': error_messages_fields['email']['invalid'],
            }
        )

    password = serializers.CharField(
        label="Пароль",
        max_length=127,
        required=True,
        write_only=True,
        trim_whitespace=False,
        validators=(PasswordRegValidator(
            message=error_messages_fields['password']['invalid']), ),
        error_messages={
            'required': error_messages_fields['password']['required'],
            'blank': error_messages_fields['password']['required'],
            }
        )

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        email = email.lower()
        self._unique_email_validate(email)
        user = User(name=name, email=email)
        self._validate_password(password, user)
        data['user'] = user
        return data

    def _unique_email_validate(self, email):
        """Проверка уникальности аккаунта по email."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': self.error_messages_fields['email']['unique']}, code='unique')

    def _validate_password(self, password, user):
        try:
            password_validation.validate_password(
                password, user=user, password_validators=self.password_validators)
        except DjangoValidationError as error:
            # чтобы указать поле, через словарь поднимаем исключение
            raise DjangoValidationError({'password': error})

    def create(self, validated_data):
        user = validated_data['user']
        password = validated_data['password']
        role = validated_data.get('role')
        if role:
            user.role = role
        user.set_password(password)
        try:
            user.save()
        except DBError as e:
            raise RegistrationError(
                'Error while saving to db.', error=e)
        return user


class AuthenticationSerializer(ErrorMsgMixin, serializers.Serializer):
    """Сериализатор аутентификации."""

    error_messages_fields = {
        'email': {
            **ErrorMsgMixin.error_messages_fields['email'],
            'not_exists': "Аккаунт с указанной почтой не найден.",
            },
        'password': {
            **ErrorMsgMixin.error_messages_fields['password'],
            'invalid': "Введен неправильный пароль.",
            },
        api_settings.NON_FIELD_ERRORS_KEY: {
            'inactive': "Аккаунт заблокирован, обратитесь к администратору.",
            }
        }

    email = serializers.CharField(
        label="E-mail",
        max_length=255,
        required=True,
        write_only=True,
        validators=(EmailValidator(
            message=error_messages_fields['email']['invalid']), ),
        error_messages={
            'required': error_messages_fields['email']['required'],
            'max_length': error_messages_fields['email']['invalid'],
            }
        )

    password = serializers.CharField(
        label="Пароль",
        required=True,
        write_only=True,
        trim_whitespace=False,
        error_messages={'required': error_messages_fields['password']['required'], }
        )

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        email = email.lower()

        user = self._authenticate(email, password)
        self._check_authenticate_user(user)

        return {
            'token': user.token,
            }

    def _authenticate(self, email, password):
        try:
            user = User.objects.authenticate(email=email, password=password)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'email': self.error_messages_fields['email']['not_exists']},
                code='not_exists',
                )
        except AuthenticateError:
            raise serializers.ValidationError(
                {'password': self.error_messages_fields['password']['invalid']},
                code='invalid',
                )
        return user

    def _check_authenticate_user(self, user):
        if not user.can_authenticate():
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY:
                    self.error_messages_fields[api_settings.NON_FIELD_ERRORS_KEY]['inactive']},
                code='inactive',
                )
