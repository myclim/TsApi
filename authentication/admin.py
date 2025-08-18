from django.contrib import admin
from authentication.models import *



admin.site.register(RoleModel)
admin.site.register(UserModel)
admin.site.register(PermissionModel)
admin.site.register(RolePermissionModel)
