from django.db import models

from classs.models import Class


class Timetable(models.Model):
    clazz = models.ForeignKey(Class, verbose_name="班级信息", on_delete=models.SET_NULL, null=True)
    week = models.SmallIntegerField('星期',
                                    choices=((1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'),
                                             (7, '星期天')),
                                    default=1)
    Date = models.DateField("日期")

    class Meta:
        verbose_name = '课表'
        verbose_name_plural = verbose_name
