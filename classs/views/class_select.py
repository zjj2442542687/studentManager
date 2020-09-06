from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.serializers import ModelSerializer

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from classs.models import Class
from classs.views.class_insert import ClassInfoSerializers
from utils.my_response import *


class ClassInfoSerializers2(ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"
        depth = 1


class ClassSelectView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    list:
    获得所有班级信息

    无描述

    retrieve:
    根据id查询班级信息

    输入id

    # 支持模糊查询
    """
    queryset = Class.objects.all()
    serializer_class = ClassInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="根据名字查询班级信息",
        operation_description="名字",
        deprecated=True
    )
    def retrieve_by_name(self, request, *args, **kwargs):
        try:
            # instance = self.queryset.filter(school_name__contains=kwargs.get("name"))
            instance = Class.objects.filter(class_name=kwargs.get("name"))
        except Class.DoesNotExist:
            return response_error_500(message="没找到")
        except Class.MultipleObjectsReturned:
            return response_error_500(message="返回多个")
        serializer = self.get_serializer(instance, many=True)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="根据学校id查询班级",
        operation_description="学校id",
        deprecated=True
    )
    def retrieve_by_school_id(self, request, *args, **kwargs):
        try:
            instance = Class.objects.filter(school_info_id=kwargs.get("school_id"))
        except Class.DoesNotExist:
            return response_error_500(message="没找到")
        except Class.MultipleObjectsReturned:
            return response_error_500(message="返回多个")
        serializer = self.get_serializer(instance, many=True)
        return response_success_200(data=serializer.data)
