from rest_framework.permissions import DjangoModelPermissions

from camping.models import Reservation, Car, Payment


class UserRelatedToObjectOrStaffPermissions(DjangoModelPermissions):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if isinstance(obj, Payment) and request.user == obj.reservation.user:
            return True
        if isinstance(obj, Reservation) and request.user == obj.user:
            return True
        if isinstance(obj, Car) and request.user in obj.drivers.all():
            return True
