from django.db import models

from teacher.models import Teacher
from timetable.models import Timetable


class Course(models.Model):
    timetable = models.ForeignKey(Timetable, verbose_name="课表", on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    course_name = models.CharField("课程名称", max_length=255)
    index = models.SmallIntegerField('课时',
                                     choices=(
                                         (1, ' 第一节课'), (2, ' 第二节课'), (3, ' 第三节课'), (4, ' 第四节课'), (5, ' 第五节课'),
                                         (6, ' 第六节课'),
                                         (7, ' 第七节课'), (8, ' 第八节课')),
                                     default=1)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
