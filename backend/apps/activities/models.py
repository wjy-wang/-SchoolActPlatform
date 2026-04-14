from django.db import models
from apps.users.models import User

class Activity(models.Model):
    title = models.CharField(max_length=100, verbose_name='活动标题')
    description = models.TextField(verbose_name='活动描述')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    type = models.IntegerField(choices=((0, '讲座'), (1, '比赛'), (2, '晚会')), verbose_name='活动类型')
    location = models.CharField(max_length=100, verbose_name='活动地点')
    poster = models.CharField(max_length=200, verbose_name='活动海报URL')
    organizer = models.CharField(max_length=50, verbose_name='组织者')
    status = models.IntegerField(default=0, choices=((0, '未开始'), (1, '进行中'), (2, '已结束')), verbose_name='状态')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
