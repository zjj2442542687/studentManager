from django.db import models

from parent.models import Parent
from school.models import School
from classs.models import Class
from user.models import User
from parent.models import Parent


class Student(models.Model):
    user_info = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    name = models.CharField("学生姓名", max_length=255)
    sex = models.CharField('性别', max_length=255)
    card = models.CharField("身份证", max_length=255)
    clazz = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField("手机号码", max_length=255, null=True)
    school = models.ForeignKey(School, verbose_name="学校信息", on_delete=models.SET_NULL, null=True)
    birthday = models.CharField("出生日期", max_length=255, null=True)
    qq = models.CharField("QQ号码", max_length=255, null=True)
    email = models.CharField("邮箱", max_length=255, null=True)
    parent = models.ManyToManyField(Parent, verbose_name="监护人信息")

    class Meta:
        verbose_name = '学生'
