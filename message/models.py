from django.db import models

# Create your models here.
from student.models import Student
from user.models import User


class StudentNoticeHz(models.Model):
    class Meta:
        verbose_name = '学生信息通知表'
        verbose_name_plural = verbose_name
        db_table = 'T_StudentNotice'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='发送人')
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, verbose_name='学生')
    level = models.SmallIntegerField('消息类别', default=0, choices=((0, '系统'), (1, '留言'), (2, '推送')))
    json = models.JSONField('json', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.SmallIntegerField('状态', default=0, choices=((0, '未读'), (1, '已读')))

    def __str__(self):
        return f'{self.Student_id} {self.status_hz}'
