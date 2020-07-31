from django.db import models

# Create your models here.
from user.models import User


class Teacher(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    school = models.CharField("学校", max_length=255)

    class Meta:
        verbose_name = '老师'
        verbose_name_plural = verbose_name
