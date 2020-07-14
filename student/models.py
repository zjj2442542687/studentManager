from django.db import models

from user.models import User


class Student(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
