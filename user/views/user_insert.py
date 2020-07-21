import re

from django.core import signing
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from user.models import User
from rest_framework.response import Response

from user.views.urls import judge_code, check_phone_number, check_user_name
from user_details.views.urls import create_user_details
from utils.my_encryption import my_encode
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import *


class UserInfoSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInsertView(mixins.CreateModelMixin,
                     GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializers

    @swagger_auto_schema(
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         'code': openapi.Schema(type=openapi.TYPE_STRING, description="这是date"),
        #         'username': openapi.Schema(type=openapi.TYPE_INTEGER),
        #     }
        # ),
        request_body=request_body(properties={
            'user_name': string_schema('用户名'),
            'password': string_schema('密码'),
            'phone_number': string_schema('手机号'),
            'code': string_schema('验证码')
        })
    )
    # request_body=request_body(property={
    #             "code": string_schema("123")
    #         }),
    def create(self, request, *args, **kwargs):
        message = 'SUCCESS'
        user_name = request.data.get('user_name')
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        # 加密
        request.data["password"] = my_encode(password)

        try:
            if not pd_phone_number(phone_number):
                message = "手机号格式错误"
                raise UserWarning

            if check_user_name(user_name):
                message = "用户名已存在"
                return response_error_400(status=STATUS_USER_NAME_DUPLICATE, message=message)
            if check_phone_number(phone_number):
                message = "该手机号已被注册"
                return response_error_400(status=STATUS_PHONE_NUMBER_DUPLICATE, message=message)
            if not judge_code(phone_number, request.data.get('code')):
                message = "验证码不正确"
                return response_error_400(status=STATUS_CODE_ERROR, message=message)

        except UserWarning:
            return response_success_200(status=STATUS_PHONE_NUMBER_ERROR, message=message)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 创建用户详情
        create_user_details(serializer.data['id'])
        return response_success_200(data=serializer.data, headers=headers)


def pd_phone_number(phone) -> bool:
    return re.match(r'^1[345678]\d{9}$', phone) is not None
