from django.db import models


class School(models.Model):
    school_name = models.CharField("学校名", max_length=255, unique=True)
    school_code = models.IntegerField("学校验证码", unique=True)

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name
