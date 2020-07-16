from django.db import models

# Create your models here.
from user.models import User


class Teacher(models.Model):
    name = models.CharField("班主任名字", max_length=255)
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '老师'
        verbose_name_plural = verbose_name
