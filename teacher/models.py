from django.db import models

# Create your models here.
from school.models import School
from user.models import User


class Teacher(models.Model):
    user_info = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    # school = models.CharField("学校", max_length=255)
    name = models.CharField("老师姓名", max_length=255)
    sex = models.CharField('性别', max_length=255)
    card = models.CharField("身份证", max_length=255)
    title = models.CharField("职称", max_length=255)
    identity = models.CharField("身份", max_length=255)
    # clazz = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField("手机号码", max_length=255)
    school = models.ForeignKey(School, verbose_name="学校信息", on_delete=models.SET_NULL, null=True)
    birthday = models.CharField("出生日期", max_length=255, null=True)
    qq = models.CharField("QQ号码", max_length=255, null=True)
    email = models.CharField("邮箱", max_length=255, null=True)
    # school = models.CharField("学校", max_length=255)

    def to_json(self):
        return {
            "name": self.name,
            "sex": self.sex,
            "card": self.card,
            "title": self.title,
            "identity": self.identity,
            "phone_number": self.phone_number,
            "school": self.school.to_json() if self.school else None,
            "birthday": self.birthday,
            "qq": self.qq,
            "email": self.email,
        }

    class Meta:
        verbose_name = '老师'
