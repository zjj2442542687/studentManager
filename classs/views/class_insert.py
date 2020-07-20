from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from classs.models import Class
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema


class ClassInfoSerializers(ModelSerializer):
    class Meta:
        model = Class
        fields = ['user_info']


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
            'teacher_info': string_schema('老师ID'),
            'grade_name': string_schema('年级名'),
            'class_name': string_schema('班级名')
        })
    )
    def create(self, request, *args, **kwargs):
        teacher_info = request.data.get('teacher_info')
        grade_name = request.data.get('grade_name')
        class_name = request.data.get('class_name')
        # print(Class.objects.filter(grade_name=grade_name))
        # if Class.objects.filter(grade_name=grade_name):
        #     message = "班级已经存在"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        # if not Teacher.objects.filter(id=teacher_info):
        #     message = "用户ID不存在"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        response = super().create(request)
        return response_success_200(data=response.data)
