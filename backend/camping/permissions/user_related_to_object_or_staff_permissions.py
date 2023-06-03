from rest_framework import permissions

from camping.models import Reservation, Opinion, Car


class UserRelatedToObjectOrAdminPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if (isinstance(obj, Reservation) and request.user == obj.user) or \
                (isinstance(obj, Opinion) and request.user == obj.author) or \
                (isinstance(obj, Car) and request.user in obj.drivers):
            return True
