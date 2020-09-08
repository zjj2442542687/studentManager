from django.db import models

from user_details.models import UserDetails


class User(models.Model):
    user_name = models.CharField("用户名", max_length=255, unique=True)
    password = models.CharField("密码", max_length=255, default="123456")
    phone_number = models.CharField("手机号", max_length=255, unique=True)
    role = models.SmallIntegerField('角色',
                                    choices=((-2, '学校管理员'), (-1, '超级管理员'), (0, '老师'), (1, '学生'), (2, '家长'), (3, '辅导员')),
                                    default=1)
    token = models.CharField("token", max_length=255, default="-1")
    user_details = models.OneToOneField(UserDetails, verbose_name="用户信息", on_delete=models.CASCADE, null=True)
    # 改到user_details中
    # avatar = models.ImageField("头像", upload_to="user/avatar", null=True)

    def to_json(self):
        return {
            "user_name": self.user_name,
            "phone_number": self.phone_number,
            "role": self.role,
        }

    def search(self):
        return {
            "user_name": self.user_name,
            "phone_number": self.phone_number,
            "role": self.role,
            "user_details": self.user_details.to_json() if self.user_details else None
        }

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户名:{self.user_name}, 密码:{self.password}, phoneNumber={self.phone_number}'
