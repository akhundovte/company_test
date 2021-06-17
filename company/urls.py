from django.urls import path
from company import views


urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='company'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company-detail'),
    path('companies/bind/', views.CompanyBind.as_view(), name='company-bind'),
    path('news/', views.NewsCreate.as_view(), name='news'),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='news-detail'),
    ]
