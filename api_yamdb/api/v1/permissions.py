from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Проверяет, является ли пользователь аутентифицирован
    в роли администратора или автора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminPermission(permissions.BasePermission):
    """Проверяет, является ли метод запроса безопасным или пользователь
    аутентифицирован в роли администратора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminModeratorAuthorPermission(permissions.BasePermission):
    """Проверяет, является ли метод запроса безопасным или пользователь
    аутентифицирован в роли администратора, автора или модератера."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
            )
        )
