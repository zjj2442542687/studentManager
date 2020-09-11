from django.db import models

# Create your models here.
from school.models import School
from user.models import User


class Parent(models.Model):
    user = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.CASCADE, null=True)

    # 以下全部改到user_details中
    # name = models.CharField("家长姓名", max_length=255)
    # sex = models.CharField('性别', max_length=255)
    # card = models.CharField("身份证", max_length=255)
    # phone_number = models.CharField("手机号码", max_length=255)
    # birthday = models.CharField("出生日期", max_length=255, null=True)
    # qq = models.CharField("QQ号码", max_length=255, null=True)
    # email = models.CharField("邮箱", max_length=255, null=True)

    def to_json(self):
        user_details = self.user.user_details
        return {
            "id": self.id,
            "name": user_details.name,
        }

    def search(self):
        user_details = self.user.user_details
        return {
            "id": self.id,
            "name": user_details.name,
            "sex": user_details.sex,
            "card": user_details.card,
            "phone_number": self.user.phone_number,
            "birthday": user_details.birthday,
            "qq": user_details.qq,
            "email": user_details.email,
        }

    class Meta:
        verbose_name = '家长'
        verbose_name_plural = verbose_name
