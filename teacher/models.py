from django.db import models

# Create your models here.
from school.models import School
from user.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, verbose_name="用户信息(用户ID)", on_delete=models.CASCADE, null=True)
    title = models.CharField("职称", max_length=255)
    school = models.ForeignKey(School, verbose_name="学校信息(学校ID)", on_delete=models.CASCADE, null=True)

    # 以下全部改到user_details中
    # name = models.CharField("老师姓名", max_length=255)
    # sex = models.CharField('性别', max_length=255)
    # card = models.CharField("身份证", max_length=255)
    # phone_number = models.CharField("手机号码", max_length=255)
    # birthday = models.CharField("出生日期", max_length=255, null=True)
    # qq = models.CharField("QQ号码", max_length=255, null=True)
    # email = models.CharField("邮箱", max_length=255, null=True)

    def to_json(self):
        role = self.user.role
        return {
            "id": self.id,
            "title": self.title,
            "identity": "辅导员" if role == 3 else ("普通教师" if role == 0 else "未知"),
            "school": self.school.to_json() if self.school else None,
        }

    def search(self):
        user_details = self.user.user_details
        role = self.user.role
        return {
            "name": user_details.name,
            "sex": user_details.sex,
            "card": user_details.card,
            "title": self.title,
            "identity": "辅导员" if role == 3 else ("普通教师" if role == 0 else "未知"),
            "phone_number": self.user.phone_number,
            "birthday": user_details.birthday,
            "qq": user_details.qq,
            "email": user_details.email,
        }

    class Meta:
        verbose_name = '老师'
