from rest_framework.viewsets import ModelViewSet

from teacher.views.teacher_insert import TeacherInfoSerializers
from teacher.models import Teacher


class TeacherOtherView(ModelViewSet):
    """
    partial_update:
    根据id修改老师信息

    无描述

    destroy:
    根据id删除老师信息

    输入id删除
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers
