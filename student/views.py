from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from student.models import Student
from utils.my_response import *
from utils.my_swagger_auto_schema import *


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

    根据id修改用户信息

    输入id修改

    destroy:删除学生信息

    根据id删除用户信息

    输入id删除

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

    retrieve_by_studentname:
    根据名字查询学生信息

    输入姓名

    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    def retrieve_by_studentname(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(user_name=kwargs.get("student_name"))
        except Student.DoesNotExist:
            return response_error_500(status=STATUS_NOT_FOUND_ERROR, message="没找到")
        except Student.MultipleObjectsReturned:
            return response_error_500(status=STATUS_MULTIPLE_ERROR, message="找到多个姓名相同用户")
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
