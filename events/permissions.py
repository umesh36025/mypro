from rest_framework import permissions
from django.http import HttpRequest

class IsAdminOrMD(permissions.BasePermission):
    """
    Custom permission to only allow Admins or users with role 'MD'.
    Assumes your User model has a 'role' attribute or similar.
    """
    def has_permission(self, request:HttpRequest, view):
        # Allow if user is staff (Admin)
        if request.user.is_superuser:
            return True
        return False     
        # Check for 'MD' role (Adjust 'role' attribute name as per your User model)

