from django.db import models
from apps.users.models import User
from apps.activities.models import Activity


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='comments')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动', related_name='comments')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否被删除')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['activity', 'is_deleted', '-created_at']),  # 评论查询常用组合
            models.Index(fields=['user', '-created_at']),                     # 用户评论列表
        ]

    def __str__(self):
        return f'{self.user.username} - {self.activity.title}'
