from django.db import models

from student.models import Student
from user.models import User


class UserCharRecord(models.Model):
    class Meta:
        verbose_name = '用户聊天表'
        verbose_name_plural = verbose_name

    send = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='发送方',
                             related_name="FKUserCharRecordSend")
    receive = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='接收方',
                                related_name="FKUserCharRecordReceive")
    content = models.TextField('内容', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.SmallIntegerField('状态', default=0, choices=((0, '未读'), (1, '已读')))

    def __str__(self):
        return f'{self.content} {self.status}'
