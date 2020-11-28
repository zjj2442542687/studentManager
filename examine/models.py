from django.db import models

# Create your models here.
from student.models import Student
from work.models import Work


class Examine(models.Model):
    student = models.ForeignKey(Student, verbose_name="提交学生ID", on_delete=models.SET_NULL, null=True)
    work = models.ForeignKey(Work, verbose_name="作业ID", on_delete=models.SET_NULL, null=True)
    grade = models.IntegerField("成绩", default=0)
    opinion = models.CharField("老师意见", default="无", max_length=255)
    state = models.BooleanField("批阅状态", default=False)
    file = models.FileField('作业附件', upload_to="workFile/", null=True)

    class Meta:
        verbose_name = "作业审核"
        verbose_name_plural = verbose_name
