from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from course.models import Course
from course.views.course_insert import CourseInfoSerializers
from utils.my_response import *


class CourseSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有课程信息

    无描述

    retrieve:
    根据id查询课程信息

    输入id

    retrieve_by_name:
    根据课程名称查询课程信息！

    传入课程名字！
    # 支持模糊查询
    """
    queryset = Course.objects.all()
    serializer_class = CourseInfoSerializers

    def retrieve_by_name(self, request, *args, **kwargs):
        # School.objects.filter(school_name__contains=kwargs.get("name"))
        try:
            # instance = self.queryset.filter(school_name__contains=kwargs.get("name"))
            instance = Course.objects.filter(course_name__contains=kwargs.get("name"))
        except Course.DoesNotExist:
            return response_error_500(message="没找到")
        except Course.MultipleObjectsReturned:
            return response_error_500(message="返回多个")
        serializer = self.get_serializer(instance, many=True)
        return response_success_200(data=serializer.data)