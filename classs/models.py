from django.db import models

from school.models import School
from teacher.models import Teacher


class Class(models.Model):
    teacher_info = models.ForeignKey(Teacher, verbose_name="老师信息", on_delete=models.SET_NULL, null=True)
    class_name = models.CharField('班级名', max_length=255)
    school_info = models.ForeignKey(School, verbose_name="学校ID", on_delete=models.SET_NULL, null=True)

    def to_json(self):
        return {
            "teacher_info": self.teacher_info.to_json(),
            "class_name": self.class_name,
            "school_name": self.school_info.to_json(),
        }

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
