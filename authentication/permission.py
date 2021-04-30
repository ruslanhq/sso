from rest_framework.permissions import BasePermission


class StaffOnly(BasePermission):
    STAFF_GROUPS = ['admin', 'manager']

    def has_permission(self, request, view):
        groups = request.user.groups.all()
        return groups.filter(title__in=self.STAFF_GROUPS).exists()
