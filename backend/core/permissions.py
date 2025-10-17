from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        ADMIN_METHODS = [
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
        ]
        is_superuser = request.user.is_authenticated and request.user.is_superuser
        if request.method in ADMIN_METHODS and not is_superuser:
            return False
        return True


class IsSuperuserOrReadonlyAuthorize(permissions.BasePermission):
    
    def has_permission(self, request, view):
        ADMIN_METHODS = [
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
        ]
        is_superuser = request.user.is_authenticated and request.user.is_superuser
        if request.method in ADMIN_METHODS and not is_superuser:
            return False
        return True