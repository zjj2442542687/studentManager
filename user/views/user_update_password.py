from drf_yasg.openapi import FORMAT_PASSWORD
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.views.urls import judge_code
from user.views.user_serializers import UserInfoSerializersUpdate
from utils.my_encryption import my_encode, my_decode
from utils.my_info_judge import pd_password, pd_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import *
from rest_framework.generics import get_object_or_404


class UserUpdatePassword(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersUpdate

    @swagger_auto_schema(
        operation_summary="手机号验证码修改密码",
        operation_description="传入手机号",
        request_body=request_body(
            required=["phone_number", "code", 'password'],
            properties={
                "phone_number": string_schema('手机号，必填'),
                "code": string_schema('验证码'),
                'password': string_schema('密码', f=FORMAT_PASSWORD),
            }
        ),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def update_password_by_phone(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        # 检测密码的长度
        check = pd_password(password)
        if check:
            return response_error_400(status=STATUS_400_BAD_REQUEST, message=check)

        # 检测手机号是否被注册
        if not User.objects.filter(phone_number=phone_number):
            return response_not_found_404(status=STATUS_NOT_FOUND_ERROR, message=f"该手机号({phone_number})未被注册!!")
        # 检测验证码是否正确
        if not judge_code(phone_number, request.data.get('code')):
            message = "验证码不正确"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        # 获得用户信息
        instance = self.queryset.get(phone_number=phone_number)
        # 如果查询出来的信息和token中的信息不一样，则返回权限不够
        if request.user != instance.pk:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message=f"没有权限修改({phone_number})")

        # 设置密码
        instance.password = my_encode(password)
        # 保存
        instance.save()
        serializer = self.get_serializer(instance)
        return response_success_200(message="成功!!!!")

    @swagger_auto_schema(
        operation_summary="根据旧密码修改密码",
        operation_description="密码",
        request_body=request_body(
            required=["old_password", 'new_password'],
            properties={
                "old_password": string_schema('旧的密码', f=FORMAT_PASSWORD),
                "new_password": string_schema('新密码', f=FORMAT_PASSWORD),
            }
        ),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def update_password_by_password(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        # 检测密码的长度
        check = pd_password(new_password)
        if check:
            return response_error_400(status=STATUS_400_BAD_REQUEST, message=check)
        # 获得用户信息
        instance = self.queryset.get(pk=request.user)
        print(my_decode(instance.password))
        # 判断输入的密码和原密码一样吗
        if my_encode(old_password) != instance.password:
            return response_error_400(status=STATUS_500_INTERNAL_SERVER_ERROR, message=f"原输入密码错误")

        # 设置密码
        instance.password = my_encode(new_password)
        # 保存
        instance.save()
        serializer = self.get_serializer(instance)
        return response_success_200(message="成功!!!!")

    def get_object(self):
        if self.action == "update_password_by_phone" or self.action == "update_password_by_password":
            pk = self.request.user
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, pk=pk)
        return super().get_object()
