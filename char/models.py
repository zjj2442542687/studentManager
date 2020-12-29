from django.db import models

from examine.models import Examine
from student.models import Student
from user.models import User
from work.models import Work


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


class UserNotice(models.Model):
    class Meta:
        verbose_name = '用户通知表'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='用户')
    level = models.SmallIntegerField('消息类别', default=0, choices=((0, '作业'), (1, '完成作业')))
    work = models.ForeignKey(Work, null=True, verbose_name='作业ID', on_delete=models.CASCADE, )
    examine = models.ForeignKey(Examine, null=True, verbose_name='检查ID', on_delete=models.CASCADE, )
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.SmallIntegerField('状态', default=0, choices=((0, '未读'), (1, '已读')))

    def __str__(self):
        return f'{self.user} {self.status}'

    def to_json(self):
        js = {
            'level': self.level,
            'levelValue': self.get_level_display(),
            'createTime': str(self.create_time),
            'status': self.status,
            'statusValue': self.get_status_display(),
        }
        if self.work:
            js['work'] = self.work.id
        if self.examine:
            js['examine'] = self.examine.id
        return js
