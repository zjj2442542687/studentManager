from django.db import models


class School(models.Model):
    school_name = models.CharField("学校名", max_length=255, unique=True)
    # school_code = models.IntegerField("学校验证码", unique=True)
    school_info = models.CharField("学校简介", max_length=550, default="这个学校很神秘，什么都没写")
    school_date = models.DateTimeField("学校注册日期", null=True, default="2000-00-00")

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name
