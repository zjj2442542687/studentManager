from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from user.models import User
from rest_framework.response import Response

# class UserInfoSerializers3(ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
from user.views.urls import send_code
from user.views.user_insert import pd_phone_number, STATUS_CODE_SUCCESS
from user.views.user_select import UserInfoSerializers
from utils.my_swagger_auto_schema import request_body, string_schema


class UserOtherView(ModelViewSet):
    """
    partial_update:
    根据id修改用户信息

    无描述

    destroy:
    根据id删除用户信息

    输入id删除
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializers

    # def get_code(self):


class Other(APIView):
    """
    post:
    发送验证码

    传入一个手机号
    """

    @swagger_auto_schema(
        request_body=request_body({
            "phone_number": string_schema("填入手机号")
        },
            required=['phone_number']
        )
    )
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        try:
            if not pd_phone_number(phone_number):
                raise UserWarning
            send_code(phone_number)
        except UserWarning:
            raise exceptions.ParseError('参数错误或手机号不合法')
        return Response({"status": STATUS_CODE_SUCCESS, "message": "发送验证码成功,验证码在2分钟内有效"})
