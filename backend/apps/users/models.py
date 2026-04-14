from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    role = models.IntegerField(default=0, choices=((0, '普通用户'), (1, '管理员')), verbose_name='角色')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
