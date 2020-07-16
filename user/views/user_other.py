from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from user.models import User
from user.views.urls import send_code
from user.views.user_insert import pd_phone_number
from user.views.user_select import UserInfoSerializers
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import *


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

    def partial_update(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        phone_number = request.data.get("phone_number")
        pk = kwargs['pk']
        if not User.objects.filter(pk=pk):
            return response_not_found_404(message="id未找到")
        # 验证手机号是否正确
        if phone_number and not pd_phone_number(phone_number):
            return response_error_400(message="手机号格式错误!!!!!!!")
        # 如果id一样且用户名不一样（因为前面已经判断了pk，所以pk是找得到的）
        if user_name and not User.objects.filter(pk=pk, user_name=user_name):
            # 如果这个名字已经被占用
            if User.objects.filter(user_name=user_name):
                return response_error_500(message="用户名已经存在")

        # 如果id一样且手机号不一样（因为前面已经判断了pk，所以pk是找得到的）
        if phone_number and not User.objects.filter(pk=pk, phone_number=phone_number):
            # 如果这个手机号已经被占用
            if User.objects.filter(phone_number=phone_number):
                return response_error_500(message="手机号已经被绑定")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(message="修改成功!", data=resp.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return response_success_200(message="删除成功!")


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
            return response_error_400(status=STATUS_PHONE_NUMBER_ERROR, message='参数错误或手机号不合法')
        return response_success_200(message="发送验证码成功,验证码在10分钟内有效")
