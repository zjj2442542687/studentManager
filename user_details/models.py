from django.db import models


# Create your models here.
from user.models import User


class UserDetails(models.Model):
    user = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    name = models.CharField("昵称", max_length=255, null=True)
    avatar = models.ImageField("头像", upload_to="userDetails/avatar", null=True)
    sex = models.SmallIntegerField('性别', choices=((-1, '女'), (0, '保密'), (1, '男')), default=0)
    birthday = models.DateTimeField("出生日期", null=True)
    personal_signature = models.CharField("个性签名", max_length=255, default="这个人很神秘，什么都没写")

    class Meta:
        verbose_name = "用户详细信息"
        verbose_name_plural = verbose_name
