from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from classs.models import Class
from classs.views.class_serializers import ClassInfoSerializersUpdate
from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherInfoSerializersAll
from user.models import User
from utils.my_info_judge import pd_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_success_200


class TeacherSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersAll

    @swagger_auto_schema(
        operation_summary="通过用户的token获得老师信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def retrieve_by_token(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if not (request.auth == 0 or request.auth == 3):
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        instance = self.queryset.get(user_id=request.user)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)


class ClassSelectView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = ClassInfoSerializersUpdate
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="通过辅导员的token获得所带班级信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def search_clazz(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth not in [0, 3]:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.user)
        # techer_id = Teacher.objects.get(user_id=request.user).id
        # print(techer_id)
        clazz = Class.objects.filter(headmaster=request.user)
        print(clazz)

        page = self.paginate_queryset(clazz)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        print(serializer.data)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="通过老师的token获得该老师所有班级信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def search_clazz_teacher(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth not in [0, 3]:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.user)
        techer_id = Teacher.objects.get(user_id=request.user).id
        print(techer_id)
        clazz = Class.objects.filter(teachers=techer_id)
        print(clazz)

        page = self.paginate_queryset(clazz)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        print(serializer.data)
        return self.get_paginated_response(serializer.data)
