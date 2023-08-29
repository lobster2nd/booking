from rest_framework import permissions


class IsSupplierOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.cat == 'Пользователь':
            return request.method in permissions.SAFE_METHODS
        return request.user.cat == 'Поставщик'