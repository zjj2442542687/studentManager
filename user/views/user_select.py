from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.views.urls import judge_code, get_info_by_token
from user.views.user_serializers import UserInfoSerializersLogin, UserInfoSerializersCheck, UserInfoSerializersPassword
from utils.my_encryption import my_encode, my_encode_token, my_decode
from utils.my_info_judge import *
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import *


class UserSelectView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersLogin

    @swagger_auto_schema(
        operation_summary="登录验证",
        operation_description="用户名或手机号加密码登录，同时优先用户名",
        request_body=request_body(
            required=["password"],
            properties={
                "user_name": string_schema('用户名'),
                "password": string_schema('密码，必填'),
                "phone_number": string_schema('手机号')
            }
        ),
    )
    def login(self, request):
        username = request.data.get("user_name")
        password = request.data.get("password")
        phone_number = request.data.get("phone_number")
        if User.objects.get(user_name=username).role >= 0:
            password = my_encode(password)

        print(f"用户名:{username},password:{password},phone_number:{phone_number}")
        try:
            if not password or not username and not phone_number:
                raise UserWarning
                # return Response({"message": "有空参数"})
            if username:
                instance = self.queryset.get(password=password, user_name=username)
            elif phone_number:
                instance = self.queryset.get(password=password, phone_number=phone_number)
            else:
                instance = None
        except User.DoesNotExist:
            return response_success_200(code=STATUS_PASSWORD_ERROR, message="用户名或密码错误")
        except UserWarning:
            return response_success_200(code=STATUS_PARAMETER_ERROR, message="参数错误！！！")
        # 设置token
        instance.token = my_encode_token(instance.pk, instance.role, my_encode(instance.user_name))
        # 保存
        instance.save()
        serializer = self.get_serializer(instance)
        print(f'数据是：{serializer.data}')
        # 获得角色信息
        print(123132123)
        print(get_info_by_token(instance.token))
        print(132131321)
        role_info = get_info_by_token(instance.token)
        role_info = role_info.to_json() if role_info else None
        return response_success_200(message="成功!!!!", data=serializer.data, role_info=role_info)

    @swagger_auto_schema(
        operation_summary="token自动登录",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def login_token(self, request):
        # 判断token
        check_token = pd_token(request)
        if check_token:
            return check_token

        print("这里!!!")
        # 获得用户信息
        instance = self.queryset.get(pk=request.user)
        print(instance)
        # 刷新token
        instance.token = my_encode_token(instance.pk, instance.role, my_encode(instance.user_name))
        # 保存
        instance.save()
        serializer = self.get_serializer(instance)
        print(f'数据是：{serializer.data}')
        # 获得角色信息
        role_info = get_info_by_token(instance.token)
        role_info = role_info.to_json() if role_info else None
        return response_success_200(message="成功!!!!", data=serializer.data, role_info=role_info)

    @swagger_auto_schema(
        operation_summary="手机号验证码登录",
        operation_description="传入手机号",
        request_body=request_body(
            required=["phone_number", "code"],
            properties={
                "phone_number": string_schema('手机号，必填'),
                "code": string_schema('验证码')
            }
        )
    )
    def login_phone_number(self, request):
        phone_number = request.data.get("phone_number")
        # 检测手机号是否被注册
        if not User.objects.filter(phone_number=phone_number):
            return response_success_200(code=STATUS_NOT_FOUND_ERROR, message=f"该手机号({phone_number})未被注册!!")
        # 检测验证码是否正确
        if not judge_code(phone_number, request.data.get('code')):
            message = "验证码不正确"
            return response_success_200(code=STATUS_CODE_ERROR, message=message)
        # 获得用户信息
        instance = self.queryset.get(phone_number=phone_number)
        # 设置token
        instance.token = my_encode_token(instance.pk, instance.role, my_encode(instance.user_name))
        # 保存
        instance.save()
        # c3RyaW5nIDE1OTYxNjM2ODcuNTM3NzE1
        # instance['teacher'] = get_info_by_token(instance.token)
        serializer = self.get_serializer(instance)
        # 获得角色信息
        role_info = get_info_by_token(instance.token)
        role_info = role_info.to_json() if role_info else None
        return response_success_200(code=STATUS_200_SUCCESS, message="成功!!!!", data=serializer.data,
                                    role_info=role_info)

    @swagger_auto_schema(
        operation_summary="检测手机号是否被注册",
        operation_description="传入手机号",
    )
    def check_phone_number(self, request, *args, **kwargs):
        phone_number = kwargs.get("phone_number")
        print(phone_number)
        phone_number_status = 0
        # 如果注册则它为1
        if self.queryset.filter(phone_number=phone_number):
            phone_number_status = 1
        print(phone_number_status)
        return response_success_200(phone_number_status=phone_number_status,
                                    message="手机号未被注册" if phone_number_status == 0 else "手机号已被注册")

    # class UserCheckView(mixins.ListModelMixin,
    #                     mixins.RetrieveModelMixin,
    #                     GenericViewSet):
    #     serializer_class = UserInfoSerializersCheck
    #     queryset = User.objects.all()
    #     parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="检测手机号验证码是否正确",
        operation_description="传入手机号、验证码和token",
        request_body=request_body(properties={
            'phone_number': string_schema('手机号'),
            'code': string_schema('验证码'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户TOKEN'),
        ],
    )
    def check_phone_code(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")
        check_token = pd_token(request)
        if check_token:
            return check_token
        # 检测手机号是否被注册
        # if not User.objects.filter(phone_number=phone_number):
        #     return response_success_200(code=STATUS_NOT_FOUND_ERROR, message=f"该手机号({phone_number})未被注册!!")
        # 检测验证码是否正确
        if not judge_code(phone_number, code):
            message = "验证码不正确"
            return response_success_200(code=STATUS_CODE_ERROR, message=message)
        return response_success_200(code=STATUS_200_SUCCESS, message="手机验证码正确！")


class UserSelectViewCheck(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersPassword

    @swagger_auto_schema(
        operation_summary="检测当前token密码是否正确",
        operation_description="传入token、密码",
        required=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def check_password(self, request, *args, **kwargs):
        password = request.data.get("password")
        # print(password)
        check_token = pd_token(request)
        if check_token:
            return check_token
        password = my_encode(password)
        # 获得pk
        pk = request.user
        if not User.objects.filter(pk=pk, password=password):
            return response_success_200(code=STATUS_NOT_FOUND_ERROR, message="用户名不存在或密码错误")
        return response_success_200(message="当前token用户密码正确")
