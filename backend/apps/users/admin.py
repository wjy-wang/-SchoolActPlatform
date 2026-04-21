from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'student_id', 'email', 'phone', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'student_id', 'email', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('student_id', 'phone', 'role')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('student_id', 'phone', 'role')}),
    )
