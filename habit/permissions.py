from rest_framework import permissions

from rest_framework import permissions


class IsCreatorOrStaff(permissions.BasePermission):
    """
    Доступ только владельцу или модератору
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().creator

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Разрешить только чтение для неавторизованных пользователей
            return True
        return obj.creator == request.user  # Разрешить изменение или удаление только владельцу привычки


class IsOwner(permissions.BasePermission):
    """
    Доступ только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        return False
