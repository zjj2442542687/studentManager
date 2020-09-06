from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from teacher.models import Teacher
from classs.models import Class
from user.models import User
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema


class ClassInfoSerializers(ModelSerializer):
    class Meta:
        model = Class
        fields = ["id", "class_name", "teacher_info", "school_info"]
        depth = 1


class ClassInsertView(mixins.CreateModelMixin,
                      GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """

    queryset = Class.objects.all()
    serializer_class = ClassInfoSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'teacher': integer_schema('辅导员ID'),
            'school': integer_schema('学校ID'),
            'class_name': string_schema('班级名')
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        class_name = request.data.get('class_name')
        print(class_name)
        if Class.objects.filter(class_name=class_name):
            message = "班级已经存在"
            return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)
        teacher_id = request.data.get('teacher')
        if not Teacher.objects.filter(id=teacher_id):
            message = "老师ID信息不存在"
            return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)

        school_id = request.data.get('school')
        if not School.objects.filter(id=school_id):
            message = "学校ID信息不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)

        teacher = Teacher.objects.get(id=teacher_id)
        headmaster_id = teacher.user_id
        try:
            clazz = self.queryset.create(headmaster_id=headmaster_id, school_id=school_id,
                                         class_name=class_name)
        #     一对一重复报错
        except IntegrityError:
            return response_error_400(message="该老师已有班级")

        # 修改老师的信息为管理员
        user = User.objects.get(id=teacher.user_id)
        teacher.identity = "辅导员"
        user.role = 3
        user.save()
        teacher.save()

        return response_success_200(data=clazz.to_json())
