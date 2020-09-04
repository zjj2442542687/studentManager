from django.db import models

from teacher.models import Teacher
from classs.models import Class


class Course(models.Model):
    course_name = models.CharField("课程名称", max_length=255)
    teacher_info = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    index = models.CharField("第几节课", max_length=10)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
