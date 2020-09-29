from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from school.views.school_insert import SchoolInfoSerializers
from utils.my_info_judge import pd_token, pd_adm_token, pd_super_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import *


class SchoolOtherView(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers

    @swagger_auto_schema(
        operation_summary="管理员修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员 TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    @swagger_auto_schema(
        operation_summary="根据id删除学校信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员 TOKEN')
        ]
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        pk = kwargs.get('pk')
        if not School.objects.filter(pk=pk):
            return response_success_200(message="学校未找到")
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")


class SchoolDeleteAllView(ModelViewSet):
    queryset = School.objects.all()

    @swagger_auto_schema(
        operation_summary="根据id列表批量删除学校信息及用户信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员TOKEN'),
        ],
        request_body=request_body(properties={
            'id_list': array_schema('学校ID列表', it=integer_schema())
        }),
    )
    def destroy_all(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token
        # print(request.data)
        list = request.data.get("id_list")
        message = ""
        print(list)
        for i in list:
            if not School.objects.filter(pk=i):
                message += "学校i+未找到"
            else:
                School.objects.filter(pk=i).delete()
        return response_success_200(message="批量删除删除结束,"+message)
