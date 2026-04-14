from django.db import models
from apps.users.models import User
from apps.activities.models import Activity

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    status = models.IntegerField(default=0, choices=((0, '待确认'), (1, '已确认')), verbose_name='报名状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    class Meta:
        verbose_name = '报名'
        verbose_name_plural = '报名'
        unique_together = ('user', 'activity')
