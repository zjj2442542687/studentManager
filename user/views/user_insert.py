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
from user_details.views.urls import *
from school.models import School
from utils.my_encryption import my_encode
from utils.my_response import *
from utils.my_swagger_auto_schema import *
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
        request_body=request_body(properties={
            'user_name': string_schema('用户名'),
            'password': string_schema('密码'),
            'school': string_schema('学校名称'),
            'phone_number': string_schema('手机号'),
            'role': integer_schema('角色(0, 老师), (1, 学生), (2, 家长)', default=1),
            'code': string_schema('验证码'),
            'name': string_schema('真实姓名'),
            'invitation_code': string_schema('邀请码')
        })
    )
    # request_body=request_body(property={
    #             "code": string_schema("123")
    #         }),
    def create(self, request, *args, **kwargs):
        message = 'SUCCESS'
        # 用户名
        user_name = request.data.get('user_name')
        # 手机号
        phone_number = request.data.get("phone_number")
        # 密码
        password = request.data.get("password")
        # 学校
        school = request.data.get('school')
        # 真实姓名
        name = request.data.get('name')
        # 加密
        request.data["password"] = my_encode(password)
        # 邀请码
        invitation_code = request.data.get('invitation_code')
        # 角色
        role = request.data.get('role')

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
            # print(School.objects.filter(school_name=school))
            # print(School.objects.filter(school_name=school).filter(school_code=invitation_code))
            if not School.objects.filter(school_name=school):
                message = "学校不存在"
                return response_error_400(status=STATUS_CODE_ERROR, message=message)
            elif not School.objects.filter(school_name=school).filter(school_code=invitation_code):
                message = "学校验证码不正确"
                return response_error_400(status=STATUS_CODE_ERROR, message=message)
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
        create_user_details(user_id=serializer.data['id'], name=name)
        # 创建角色信息
        if role == 0:
            create_teacher(user_id=serializer.data['id'], school=school)
        elif role == 1:
            create_student(user_id=serializer.data['id'], school=school)
        elif role == 2:
            create_parent(user_id=serializer.data['id'], school=school)
        else:
            message = "角色不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        return response_success_200(data=serializer.data, headers=headers)


def pd_phone_number(phone) -> bool:
    return re.match(r'^1[345678]\d{9}$', phone) is not None
