from django.db import models

# Create your models here.
from teacher.models import Teacher
from classs.models import Class


class Course(models.Model):
    teacher_info = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    class_info = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    course_name = models.CharField("课程名称", max_length=255, unique=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

