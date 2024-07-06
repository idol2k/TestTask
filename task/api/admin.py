from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Employee, Client, Task, Access


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            "Additional Info",
            {
                "fields": ("is_employee", "is_client"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Task)
admin.site.register(Access)