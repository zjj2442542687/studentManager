from django.db import models

from teacher.models import Teacher
from timetable.models import Timetable


class Course(models.Model):
    timetable = models.ForeignKey(Timetable, verbose_name="课表", on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    course_name = models.CharField("课程名称", max_length=255)
    index = models.CharField("第几节课", max_length=10)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
