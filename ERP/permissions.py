from rest_framework import permissions

class IsAdminManagerEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'Admin':
            return True  # Full access
        elif user.role == 'Manager':
            # Can only modify users in their own department
            return obj.department == user.department
        elif user.role == 'Employee':
            # Can only access own profile and allow only GET or PATCH/PUT
            return obj == user and request.method in ['GET', 'PUT', 'PATCH']
        else:
            return False
