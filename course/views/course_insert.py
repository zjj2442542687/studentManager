from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from classs.models import Class
from course.models import Course
from user.models import User
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema


class CourseInfoSerializers(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseInsertView(mixins.CreateModelMixin,
                      GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """

    queryset = Course.objects.all()
    serializer_class = CourseInfoSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'teacher_info': integer_schema('老师ID'),
            'class_info': integer_schema('班级ID'),
            'course_name': string_schema('课程名')
        })
    )
    def create(self, request, *args, **kwargs):
        teacher_info = request.data.get('teacher_info')
        class_info = request.data.get('class_info')
        # print(Class.objects.filter(grade_name=grade_name))
        # if Class.objects.filter(grade_name=grade_name):
        #     message = "班级已经存在"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        if not Teacher.objects.filter(id=teacher_info):
            message = "老师ID信息不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        if not Class.objects.filter(id=class_info):
            message = "班级ID信息不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        resp = super().create(request)
        return response_success_200(data=resp.data)
