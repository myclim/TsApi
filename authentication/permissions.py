from rest_framework.permissions import BasePermission
from authentication.models import RolePermissionModel



class UserCustomPermission(BasePermission):
    """
    Проверяет, есть ли у пользователя нужное разрешение.
    """
    def has_permission(self, request, view):
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated or not user.is_active:
            return False

        required_permission = getattr(view, "required_permission", None)
        if not required_permission:
            return False

        has_perm = RolePermissionModel.objects.filter(
            role=user.role,
            permission__name=required_permission
        ).exists()

        return has_perm
    
