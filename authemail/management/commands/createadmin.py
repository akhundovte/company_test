import getpass
from rest_framework import serializers

from django.core.management.base import BaseCommand

from authemail.models import RoleConst
from authemail.serializers import AccountCreationSerializer


class Command(BaseCommand):
    serializer_class = AccountCreationSerializer

    def handle(self, *args, **options):
        is_valid = False
        serializer_empty = self.serializer_class()

        while not is_valid:
            username = self._input_username(serializer_empty)
            email = self._input_email(serializer_empty)
            password = self._input_password(serializer_empty)

            data = {'name': username, 'password': password, 'email': email}
            serializer = self.serializer_class(data=data)
            is_valid = serializer.is_valid()
            if not is_valid:
                self.stderr.write(_get_str_errors(serializer.errors))
                continue
            serializer.save(role=RoleConst.ADMIN)

    def _input_username(self, serializer):
        username = None
        while username is None:
            username = input('Введите имя: ')
            try:
                username = self._run_field_validation('name', username, serializer)
            except CommandValidationError as e:
                self.stderr.write(str(e))
                username = None
                continue
        return username

    def _input_email(self, serializer):
        email = None
        while email is None:
            email = input('Введите E-mail: ')
            try:
                email = self._run_field_validation('email', email, serializer)
            except CommandValidationError as e:
                self.stderr.write(str(e))
                email = None
                continue
        return email

    def _input_password(self, serializer):
        password = None
        while password is None:
            password = getpass.getpass('Введите пароль: ')
            try:
                password = self._run_field_validation('password', password, serializer)
            except CommandValidationError as e:
                self.stderr.write(str(e))
                password = None
                continue

            password2 = getpass.getpass('Введите пароль (повторно): ')
            if password != password2:
                self.stderr.write("Ошибка: Пароли не совпадают.")
                password = None
                continue
        return password

    def _run_field_validation(self, field, value, serializer):
        try:
            validated_value = serializer.fields[field].run_validation(value)
        except serializers.ValidationError as err:
            msg = '\n'.join(item['message'] for item in err.get_full_details())
            raise CommandValidationError(msg)
        return validated_value


def _get_str_errors(errors):
    if isinstance(errors, list):
        return '\n'.join(str(item) for item in errors)
    elif isinstance(errors, dict):
        return '\n'.join(_get_str_errors(value) for key, value in errors.items())


class CommandValidationError(Exception):
    pass
