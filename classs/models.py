from django.db import models

from teacher.models import Teacher


class Class(models.Model):
    teacher_info = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    grade_name = models.CharField("年级名", max_length=255)
    class_name = models.CharField("班级名", max_length=255)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
