from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),  # 'groups', 'user_permissions'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
