from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class RoleModel(models.Model):
    ROLES = [("admin", "Admin"), ("manager", "Manager"), ("guest", "Guest")]
    name = models.CharField(max_length=50, choices=ROLES, unique=True)

    def __str__(self):
        return self.name


class UserModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(to=RoleModel, on_delete=models.SET_NULL, null=True)

    def set_password(self, password):
        self.password = make_password(password)

    def get_password(self, password):
        return check_password(password, self.password)

    def delete_user(self):
        self.is_active = False
        self.save()

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.first_name}: {self.email}"


class PermissionModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RolePermissionModel(models.Model):
    role = models.ForeignKey(to=RoleModel, on_delete=models.CASCADE)
    permission = models.ForeignKey(to=PermissionModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role}: {self.permission}"
