import time

from django.db import models

from classs.models import Class
from regular_category.models import RegularCategory
from user.models import User


class Regular(models.Model):
    regular_category = models.ForeignKey(RegularCategory, verbose_name="属于的类别", on_delete=models.SET_NULL, null=True)
    image = models.ImageField("图片", upload_to="image/regular", null=True)
    title = models.CharField("标题", max_length=20, null=True)
    describe = models.CharField("描述", max_length=255, null=True)
    user = models.ForeignKey(User, verbose_name="创建者", on_delete=models.CASCADE, null=True)
    clazz = models.ForeignKey(Class, verbose_name="班级", on_delete=models.CASCADE, null=True)
    is_system = models.SmallIntegerField('是不是系统的(0，否，1，是决定公开和私有性，是系统则公开)', choices=((0, '否'), (1, '是')), default=0)
    creation_time = models.BigIntegerField("创建时间", blank=True, default=int(time.time()))

    def to_json(self):
        return {
            "title": self.title,
            "describe": self.describe,
        }

    def search(self):
        return {
            "title": self.title,
            "describe": self.describe,
        }

    class Meta:
        verbose_name = "习惯养成"
        verbose_name_plural = verbose_name
