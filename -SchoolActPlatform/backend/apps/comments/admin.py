from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'activity__title', 'content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'
