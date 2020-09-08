from django.db import models


class Week(models.Model):
    index = models.SmallIntegerField('位置',
                                     choices=((1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'),
                                              (7, '星期天')),
                                     default=1, unique=True)
    title = models.CharField("标题", max_length=255, null=True)

    class Meta:
        verbose_name = "周"
        verbose_name_plural = verbose_name
