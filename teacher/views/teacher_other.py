from rest_framework.viewsets import ModelViewSet

from teacher.views.teacher_insert import TeacherInfoSerializers
from user.models import User


class TeacherOtherView(ModelViewSet):
    """
    partial_update:
    根据id修改老师信息

    无描述

    destroy:
    根据id删除老师信息

    输入id删除
    """
    queryset = User.objects.all()
    serializer_class = TeacherInfoSerializers
