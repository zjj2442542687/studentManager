from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from school.models import School
from school.views.school_insert import SchoolInfoSerializers
from utils.my_response import *


class SchoolSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有学校信息

    无描述

    retrieve:
    根据id查询学校信息

    输入id

    retrieve_by_name:
    根据名字查询学校信息！

    传入学校名字！
    # 支持模糊查询
    """
    queryset = School.objects.all()
    serializer_school = SchoolInfoSerializers

    def retrieve_by_name(self, request, *args, **kwargs):
        # School.objects.filter(school_name__contains=kwargs.get("name"))
        try:
            # instance = self.queryset.filter(school_name__contains=kwargs.get("name"))
            instance = School.objects.filter(school_name__contains=kwargs.get("name"))
        except School.DoesNotExist:
            return response_error_500(message="没找到")
        except School.MultipleObjectsReturned:
            return response_error_500(message="返回多个")
        serializer = self.get_serializer(instance, many=True)
        return response_success_200(data=serializer.data)
