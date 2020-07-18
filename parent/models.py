from django.db import models

# Create your models here.
from user.models import User
from student.models import Student


class Parent(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    stu_info = models.ForeignKey(Student, verbose_name="学生信息", on_delete=models.SET_NULL, name=True)

    class Meta:
        verbose_name = '家长'
        verbose_name_plural = verbose_name
