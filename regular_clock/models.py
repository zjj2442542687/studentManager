from django.db import models

from regular_add_record.models import RegularAddRecord


class RegularClock(models.Model):
    regular_add_record = models.ForeignKey(RegularAddRecord, verbose_name="打卡用户所添加的", on_delete=models.SET_NULL, null=True)
    image = models.ImageField("图片", upload_to="image/regularClock", null=True)
    mood = models.CharField("心情", max_length=255, null=True, default="心情怎么样，记录一下吧~")
    clock_in_time = models.DateTimeField("打卡时间", auto_now_add=True, blank=True)

    def to_json(self):
        return {
            "title": self.mood,
        }

    def search(self):
        return {
            "title": self.mood,
        }

    class Meta:
        verbose_name = "习惯养成的打卡"
        verbose_name_plural = verbose_name
