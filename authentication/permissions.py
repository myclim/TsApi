from rest_framework.permissions import BasePermission
from authentication.models import RolePermissionModel, PermissionModel




class UserCustomPermission(BasePermission):
    """
    Проверяет, есть ли у пользователя нужное разрешение.
    Требуемое разрешение указывается во view`.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated or not user.is_active:
            return False

        required_permission = getattr(view, "required_permission", None)
        if not required_permission:
            return False

        return RolePermissionModel.objects.filter(
            role=user.role,
            permission__name=required_permission
        ).exists()