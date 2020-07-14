from django.db import models

# Create your models here.
from user.models import User


class Parent(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '家长表11'
        verbose_name_plural = verbose_name
