from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField("用户名", max_length=255, unique=True)
    password = models.CharField("密码", max_length=255, default="123456")
    phone_number = models.CharField("手机号", max_length=255, unique=True)
    role = models.SmallIntegerField('角色',
                                    choices=((-2, '学校管理员'), (-1, '超级管理员'), (0, '老师'), (1, '学生'), (2, '家长'), (3, '辅导员')),
                                    default=1)
    # role_id = models.IntegerField('',)
    # name = models.CharField("昵称", max_length=255, null=True)
    avatar = models.ImageField("头像", upload_to="user/avatar", null=True)
    token = models.CharField("token", max_length=255)

    # personal_signature = models.CharField("个性签名", max_length=255, default="这个人很神秘，什么都没写")

    def to_json(self):
        return {
            "user_name": self.user_name,
            "password": self.password,
            "phone_number": self.phone_number,
            "role": self.role,
        }

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户名:{self.user_name}, 密码:{self.password}, phoneNumber={self.phone_number}'
