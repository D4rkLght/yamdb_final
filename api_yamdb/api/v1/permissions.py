from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ разрешен только администратору или суперпользователю.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Доступ разрешен только администратору или суперпользователю.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin))


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    message = (
        'Доступ разрешен только автору'
        'модератору, администратору или'
        'суперпользователю.'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ('moderator', 'admin',)
                or request.user.is_superuser
                or obj.author == request.user)
