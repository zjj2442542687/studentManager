from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from user.models import User


class TeacherInfoSerializers(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        depth = 1


class TeacherInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers
