from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'location', 'start_time', 'end_time', 'status', 'created_by', 'created_at']
    list_filter = ['type', 'status', 'created_at']
    search_fields = ['title', 'location', 'organizer']
    date_hierarchy = 'created_at'
