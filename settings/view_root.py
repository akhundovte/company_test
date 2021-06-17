from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'Регистрация': reverse('signup_user', request=request),
        'Получение JWT токена': reverse('login_user', request=request),
        'Компании': reverse('company', request=request),
        'Новости': reverse('news', request=request),
        'Создание связи между компанией и пользователем ': reverse('company-bind', request=request),
    })
