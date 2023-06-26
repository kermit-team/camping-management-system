from rest_framework import permissions


class PostAnonElseStaffOrUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.user.is_authenticated and request.method in {'GET', 'PUT', 'PATCH', 'DELETE'}:
            return True
        return False

    def has_object_permission(self, request, view, user):
        if request.user.is_staff or request.user == user:
            return True
