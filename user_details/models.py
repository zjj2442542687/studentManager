import time

from django.db import models


class UserDetails(models.Model):
    name = models.CharField("昵称", max_length=255, null=True)
    avatar = models.ImageField("头像", upload_to="userDetails/avatar", null=True)
    card = models.CharField("身份证", max_length=255, null=True)
    sex = models.SmallIntegerField('性别', choices=((-1, '女'), (0, '保密'), (1, '男')), default=0)
    birthday = models.BigIntegerField("出生日期", null=True, default=int(time.time()))
    qq = models.CharField("QQ号码", max_length=255, null=True)
    email = models.EmailField("邮箱", max_length=255, null=True)
    personal_signature = models.CharField("个性签名", max_length=255, default="这个人很神秘，什么都没写")

    def to_json(self):
        return {
            "name": self.name,
            "avatar": self.avatar.path,
            "sex": self.sex,
            "birthday": self.birthday,
            "qq": self.qq,
            "email": self.email,
            "personal_signature": self.personal_signature,
        }

    class Meta:
        verbose_name = "用户详细信息"
        verbose_name_plural = verbose_name
