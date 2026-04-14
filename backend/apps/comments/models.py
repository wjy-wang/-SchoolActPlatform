from django.db import models
from apps.users.models import User
from apps.activities.models import Activity

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
