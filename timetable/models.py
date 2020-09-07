from django.db import models

from classs.models import Class
from week.models import Week


class Timetable(models.Model):
    clazz = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    week = models.ForeignKey(Week, verbose_name="周", on_delete=models.SET_NULL, null=True)
    Date = models.DateField("日期", auto_now_add=True, blank=True)

    class Meta:
        verbose_name = '课表'
        verbose_name_plural = verbose_name
