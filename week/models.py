from django.db import models


class Week(models.Model):
    index = models.SmallIntegerField('位置',
                                     choices=((1, '周一'), (2, '周二'), (3, '周三'), (4, '周四'), (5, '周五'), (6, '周六'),
                                              (7, '周日')),
                                     default=1, unique=True)
    title = models.CharField("标题", max_length=255, null=True)

    class Meta:
        verbose_name = "周"
        verbose_name_plural = verbose_name
