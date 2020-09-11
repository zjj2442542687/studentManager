from django.db import models

from parent.models import Parent
from school.models import School
from classs.models import Class
from user.models import User
from parent.models import Parent


def to_parent_list(parent):
    parents = []
    for p in parent:
        parents.append(p.search())
    return parents


class Student(models.Model):
    user = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.CASCADE, null=True)
    clazz = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, verbose_name="学校信息", on_delete=models.CASCADE, null=True)
    parent = models.ManyToManyField(Parent, verbose_name="监护人信息")

    # 以下全部改到user_details中
    # name = models.CharField("学生姓名", max_length=255)
    # sex = models.CharField('性别', max_length=255)
    # card = models.CharField("身份证", max_length=255)
    # phone_number = models.CharField("手机号码", max_length=255, null=True)
    # birthday = models.CharField("出生日期", max_length=255, null=True)
    # qq = models.CharField("QQ号码", max_length=255, null=True)
    # email = models.CharField("邮箱", max_length=255, null=True)

    def to_json(self):
        return {
            "clazz": self.clazz.to_json() if self.clazz else None,
            "school": self.school.to_json() if self.school else None,
            "parent": to_parent_list(self.parent.all()) if self.parent else None,
        }

    def search(self):
        user_details = self.user.user_details
        return {
            "name": user_details.name,
            "sex": user_details.sex,
            "card": user_details.card,
            "phone_number": self.user.phone_number,
            "birthday": user_details.birthday,
            "qq": user_details.qq,
            "email": user_details.email,
        }

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name
