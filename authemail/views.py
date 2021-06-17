from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountCreationSerializer, AuthenticationSerializer


class AccountCreationView(APIView):
    """Создание аккаунта."""
    serializer_class = AccountCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'token': serializer.data['token']},
            status=status.HTTP_201_CREATED,
            )


class LoginView(APIView):
    """Аутентификация пользователя."""
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
