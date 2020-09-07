from django.db import models
import django.utils.timezone as timezone
from regular.models import Regular
from user.models import User
from week.models import Week


class RegularAddRecord(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.SET_NULL, null=True)
    describe = models.CharField("描述", max_length=255, null=True)
    regular = models.ForeignKey(Regular, verbose_name="习惯养成", on_delete=models.SET_NULL, null=True)
    reminder_time = models.TimeField("提醒时间", default=timezone.now)
    start_time = models.TimeField("开始时间", default=timezone.now)
    end_time = models.TimeField("结束时间", default=timezone.now)
    start_date = models.DateTimeField("开始日期", default=timezone.now)
    end_date = models.DateTimeField("结束日期", default=timezone.now)
    week = models.ManyToManyField(Week, verbose_name="需要打卡的周")
    # is_clock = models.SmallIntegerField('今日是否打卡了', choices=((0, '是'), (1, '否')), default=0)

    def to_json(self):
        return {
        }

    def search(self):
        return {
        }

    class Meta:
        verbose_name = "习惯养成添加记录"
        verbose_name_plural = verbose_name
