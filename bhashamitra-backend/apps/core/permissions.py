"""Custom permissions."""
from rest_framework import permissions


class IsParentOfChild(permissions.BasePermission):
    """Permission to check if user is the parent of the child."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Handle Child object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Handle objects with child FK (Progress, etc.)
        if hasattr(obj, 'child'):
            return obj.child.user == request.user
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission for owners or admins."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
