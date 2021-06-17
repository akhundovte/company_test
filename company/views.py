from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from . import services
from .serializers import (
    CompanySerializer, CompanyBindSerializer, NewsSerializer
    )
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrReadOnlyObj, IsUserBindCompany
    )


class CompanyList(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        companies = services.get_all_companies()
        serializer = self.serializer_class(companies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyDetail(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnlyObj | IsUserBindCompany]

    def get(self, request, pk, format=None):
        company = self._get_object(pk)
        serializer = self.serializer_class(company)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        company = self._get_object(pk)
        serializer = self.serializer_class(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        company = self._get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, pk):
        try:
            company = services.get_company_by_id(pk)
        except services.EntityDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, company)
        return company


class CompanyBind(APIView):
    serializer_class = CompanyBindSerializer
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsCreate(APIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnlyObj | IsUserBindCompany]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._check_exists_company_and_permissions(serializer.validated_data['company_id'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _check_exists_company_and_permissions(self, company_id):
        try:
            company = services.get_company_by_id(company_id)
        except services.EntityDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, company)


class NewsDetail(APIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnlyObj | IsUserBindCompany]

    def get(self, request, pk, format=None):
        news = self._get_object(pk)
        serializer = self.serializer_class(news)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        news = self._get_object(pk)
        serializer = self.serializer_class(news, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        news = self._get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, pk):
        try:
            news = services.get_news_with_company_by_id(pk)
        except services.EntityDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, news)
        return news
