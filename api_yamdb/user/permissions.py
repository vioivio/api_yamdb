from rest_framework import permissions

"""
    Поменять permissions по требованиям
"""


class UserProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.check_role == 'admin'

    def has_object_permission(self, request, view, obj):
        if view.kwargs['username'] == 'me':
            return True
        return request.user.check_role == 'admin'


class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.check_role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.check_role == 'admin'


class ModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.check_role == 'moderator' or
                request.user.check_role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.user.check_role == 'moderator' or
                request.user.check_role == 'admin')


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.check_role == 'moderator' or
                request.user.check_role == 'admin' or
                obj.author == request.user or
                request.method in permissions.SAFE_METHODS)
