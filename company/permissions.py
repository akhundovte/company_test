from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Company, News
from .services import has_bind_user_to_company


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return _is_admin_auth_from_request(request)


class IsAdminOrReadOnlyObj(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return _is_admin_auth_from_request(request)


class IsUserBindCompany(BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Company):
            if request.method == 'DELETE':
                return False
            company = obj
        elif isinstance(obj, News):
            company = obj.company
        else:
            raise ValueError('Object is not instance Company or News')

        if _is_user_auth_from_request(request):
            return has_bind_user_to_company(user=request.user, company=company)
        return False


def _is_admin_auth_from_request(request):
    return bool(request.user and
                request.user.is_authenticated and
                request.user.is_admin
                )


def _is_user_auth_from_request(request):
    return bool(request.user and
                request.user.is_authenticated and
                request.user.is_user
                )
