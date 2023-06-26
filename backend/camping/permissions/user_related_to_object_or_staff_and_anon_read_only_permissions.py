from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from camping.models import Opinion


class UserRelatedToObjectOrStaffAndAnonReadOnlyPermissions(DjangoModelPermissionsOrAnonReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if isinstance(obj, Opinion) and request.user == obj.author:
            return True
