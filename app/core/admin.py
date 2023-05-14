"""
Django Admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserRoleAdmin(admin.TabularInline):
    model = models.UserRole
    extra = 1


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    inlines = [UserRoleAdmin]
    ordering = ['id']
    list_display = ['id', 'username', 'email']
    fieldsets = (
        (_('Personal Info'), {'fields': ('username', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserRole)
admin.site.register(models.Role)
admin.site.register(models.Permission)
