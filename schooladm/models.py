from django.db import models

# Create your models here.
from school.models import School
from user.models import User


class Schooladm(models.Model):
    school = models.ForeignKey(School, verbose_name="学校信息", on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, verbose_name="用户信息", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "学校管理员"
        verbose_name_plural = verbose_name
