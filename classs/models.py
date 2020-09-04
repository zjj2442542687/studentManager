from django.db import models

from school.models import School
from teacher.models import Teacher


class Class(models.Model):
    # 辅导员和班级有且只有一个相对应
    teacher_info = models.OneToOneField(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True,
                                        error_messages={
                                            'unique': "老师信息唯一"})
    class_name = models.CharField('班级名', max_length=255)
    school_info = models.ForeignKey(School, verbose_name="学校ID", on_delete=models.SET_NULL, null=True)

    def to_json(self):
        return {
            "id": self.id,
            "teacher_info": self.teacher_info.to_json() if self.teacher_info else None,
            "class_name": self.class_name,
            "school_info": self.school_info.to_json() if self.school_info else None,
        }

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
