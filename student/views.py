from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from student.models import Student


class StudentInfoSerializers(ModelSerializer):
    class Meta:
        model = Student
        fields = ['user_info']


class StudentInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create:
    添加一条学生信息数据

    无描述
    """

    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers


class StudentOtherView(ModelViewSet):
    """
    update:修改学生表信息

    无描述
    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers


class StudentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有学生信息

    无描述

    retrieve:
    根据id查询学生信息

    输入id

    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers2
