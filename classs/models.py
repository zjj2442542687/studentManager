from django.db import models

# from teacher.models import Teacher
from school.models import School
from teacher.models import Teacher


class Class(models.Model):
    teacher_info = models.ForeignKey(Teacher, verbose_name="辅导员ID", on_delete=models.SET_NULL, null=True)
    class_name = models.CharField("班级名", max_length=255)
    school_name = models.ForeignKey(School, verbose_name="学校ID", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
