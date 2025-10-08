from rest_framework.permissions import BasePermission


from users.models import User



class IsRiderRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "rider")
