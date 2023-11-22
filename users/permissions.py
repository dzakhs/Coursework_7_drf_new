from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Доступ только у пользователя
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.pk == request.user.pk


class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Доступ только владельцу аккаунта или суперпользователю
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser