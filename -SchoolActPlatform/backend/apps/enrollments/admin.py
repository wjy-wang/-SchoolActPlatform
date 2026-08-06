from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'activity__title']
