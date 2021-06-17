from django.urls import path

from .views import AccountCreationView, LoginView


urlpatterns = [
    path('signup/', AccountCreationView.as_view(), name='signup_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    ]
