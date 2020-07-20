
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from user.models import User
from utils.my_response import *
from utils.my_response import response_error_400, response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema


class TeacherInfoSerializers(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user_info']


class TeacherInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'user_info': string_schema('用户ID')
        })
    )
    def create(self, request, *args, **kwargs):
        user_info = request.data.get('user_info')
        if not User.objects.filter(id=user_info):
            message = "用户ID不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        response = super().create(request)
        return response_success_200(data=response.data)
