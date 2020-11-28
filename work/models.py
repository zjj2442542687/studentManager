import django.utils.timezone as timezone

from django.db import models

from classs.models import Class
from teacher.models import Teacher


class Work(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name="发布老师ID", on_delete=models.SET_NULL, null=True)
    clazz = models.ForeignKey(Class, verbose_name="班级ID", on_delete=models.CASCADE, null=True)
    course = models.CharField("作业课程科目", max_length=255)
    title = models.CharField("作业标题", max_length=255)
    content = models.CharField("作业内容", max_length=255)
    release_Time = models.BigIntegerField("作业发布日期时间", default=timezone.now)
    start_date = models.BigIntegerField("作业开始日期时间", default=timezone.now)
    end_date = models.BigIntegerField("作业结束日期时间", default=timezone.now)
    file = models.FileField('作业发布附件', upload_to="workFile/", null=True)
    request = models.CharField("作业要求", max_length=255, null=True)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name
