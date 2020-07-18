from django.db import models

from user.models import User
from parent.models import Parent


class Student(models.Model):
    user_info = models.ForeignKey(User, verbose_name="用户信息", on_delete=models.SET_NULL, null=True)
    parent_info = models.ForeignKey(Parent, verbose_name="主监护人信息", on_delete=models.SET_NULL, null=True)
    parent2_info = models.ForeignKey(Parent, verbose_name="主监护人信息", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
