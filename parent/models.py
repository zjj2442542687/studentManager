from django.db import models

# Create your models here.
from school.models import School
from user.models import User


class Parent(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    name = models.CharField("家长姓名", max_length=255)
    sex = models.CharField('性别', max_length=255)
    card = models.CharField("身份证", max_length=255)
    phone_number = models.CharField("手机号码", max_length=255)
    # school = models.ForeignKey(School, verbose_name="学校信息", on_delete=models.SET_NULL, null=True)
    birthday = models.CharField("出生日期", max_length=255, null=True)
    qq = models.CharField("QQ号码", max_length=255, null=True)
    email = models.CharField("邮箱", max_length=255, null=True)

    class Meta:
        verbose_name = '家长'
        verbose_name_plural = verbose_name
