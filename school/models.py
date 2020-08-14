from django.db import models


def get_data(data):
    return f"{data.year}年{data.month}月{data.day}日"


class School(models.Model):
    school_name = models.CharField("学校名", max_length=255, unique=True)
    # school_code = models.IntegerField("学校验证码", unique=True)
    school_info = models.CharField("学校简介", max_length=550, default="这个学校很神秘，什么都没写")
    school_date = models.DateTimeField("学校注册日期", null=True, default="2000-00-00")

    def to_json(self):
        return {
            "school_name": self.school_name,
            "school_info": self.school_info,
            "school_date": get_data(self.school_date) if self.school_date else None,
        }

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name
