from django.db import models

# Create your models here.
from classs.models import Class


class Timetable(models.Model):
    # table_time = models.DateTimeField("课程时间")
    class_info = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    # table_week = models.CharField("周几", max_length=255)
    table_course = models.ManyToManyField()

    class Meta:
        verbose_name = '课表'
        verbose_name_plural = verbose_name
