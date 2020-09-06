from django.db import models

from school.models import School
from teacher.models import Teacher
from user.models import User


class Class(models.Model):
    # 班主任和班级有且只有一个相对应
    headmaster = models.OneToOneField(User, verbose_name="老师信息", on_delete=models.SET_NULL, null=True,
                                      error_messages={
                                          'unique': "老师信息唯一"})
    class_name = models.CharField('班级名', max_length=255)
    school = models.ForeignKey(School, verbose_name="学校ID", on_delete=models.SET_NULL, null=True)
    teachers = models.ManyToManyField(Teacher, verbose_name="老师")

    def to_json(self):
        return {
            "id": self.id,
            "teacher": self.headmaster.to_json() if self.headmaster else None,
            "class_name": self.class_name,
            "school": self.school.to_json() if self.school else None,
        }

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
