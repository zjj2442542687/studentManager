from django.db import models

from user.models import User
from parent.models import Parent


class Student(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    # parent = models.ManyToManyField(Parent, verbose_name="监护人信息")
    school = models.CharField("学校", max_length=255)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
