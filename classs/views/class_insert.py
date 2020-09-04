from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from teacher.models import Teacher
from classs.models import Class
from user.models import User
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
            'teacher_info': integer_schema('辅导员ID'),
            'school_info': integer_schema('学校ID'),
            'class_name': string_schema('班级名')
        })
    )
    def create(self, request, *args, **kwargs):
        class_name = request.data.get('class_name')
        print(class_name)
        if Class.objects.filter(class_name=class_name):
            message = "班级已经存在"
            return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)
        teacher_info = request.data.get('teacher_info')
        if not Teacher.objects.filter(id=teacher_info):
            message = "老师ID信息不存在"
            return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)
        # 修改老师的信息为管理员
        teacher = Teacher.objects.get(id=teacher_info)
        user = User.objects.get(id=teacher.user_info_id)
        # 查看这个老师是不是已经是辅导员了
        if user.role == 3:
            return response_error_400(status=STATUS_PARAMETER_ERROR, message="该老师已经是辅导员了！！！！！！！！")
        teacher.identity = "辅导员"
        user.role = 3
        teacher.save()

        school_info = request.data.get('school_info')
        if not School.objects.filter(id=school_info):
            message = "学校ID信息不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        teacher = self.queryset.create(teacher_info_id=teacher_info, school_info_id=school_info, class_name=class_name)
        return response_success_200(data=teacher.to_json())
