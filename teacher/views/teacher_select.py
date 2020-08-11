from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from teacher.views.teacher_insert import TeacherInfoSerializers
from utils.my_response import *


class TeacherInfoSerializers2(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        depth = 1


class TeacherSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有老师信息

    无描述

    retrieve:
    根据id查询老师信息

    输入id

    retrieve_by_name:
    根据名字查询老师信息！

    传入名字！
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    def retrieve_by_name(self, request, *args, **kwargs):
        try:
            # instance = self.queryset.get(name=kwargs.get("name"))
            # instance = self.queryset.get(name__contains=kwargs.get("name"))
            instance = self.queryset.filter(name__contains=kwargs.get("name"))
        except Teacher.DoesNotExist:
            return response_error_500(message="没找到")
        except Teacher.MultipleObjectsReturned:
            return response_error_500(message="返回多个")
        serializer = self.get_serializer(instance, many=True)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="通过用户的token获得老师信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def retrieve_by_token(self, request):
        token = request.META.get("HTTP_TOKEN")
        # token = request.data.get("token")
        print(token)
        print(request.user)
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!")

        instance = self.queryset.get(user_info=request.user)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
