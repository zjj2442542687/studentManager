
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.utils import json

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from parent.models import Parent
from student.models import Student
from teacher.models import Teacher
from user.models import User

from user.views.urls import judge_code
from user.views.user_serializers import UserInfoSerializersLess, UserInfoSerializersNoPassword
from utils.my_encryption import my_encode, my_encode_token, my_decode_token, my_decode
from utils.my_info_judge import pd_token
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class UserSelectView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersNoPassword

    @swagger_auto_schema(
        operation_summary="获得所有信息",
        operation_description="所有信息",
        responses={200: UserInfoSerializersLess}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = UserInfoSerializersLess(queryset, many=True)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="根据用户名查询",
        operation_description="我是说明",
    )
    def retrieve_by_username(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(user_name=kwargs.get("user_name"))
        except User.DoesNotExist:
            return response_error_500(status=STATUS_NOT_FOUND_ERROR, message="没找到")
        except User.MultipleObjectsReturned:
            return response_error_500(status=STATUS_MULTIPLE_ERROR, message="返回多个")
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)

    def retrieve_by_phone_number(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(phone_number=kwargs.get("phone_number"))
        except User.DoesNotExist:
            return response_error_500(status=STATUS_NOT_FOUND_ERROR, message="没找到")
        except User.MultipleObjectsReturned:
            return response_error_500(status=STATUS_MULTIPLE_ERROR, message="返回多个")
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)

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
            return response_error_400(message="用户名或密码错误")
        except UserWarning:
            return response_error_400(status=STATUS_PARAMETER_ERROR, message="参数错误！！！")
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
        role_info = get_info_by_token(instance.token).to_json()
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
        token = request.META.get("HTTP_TOKEN")
        print(f'token={token}')
        # token = request.data.get("token")
        # 判断token
        check_token = pd_token(request, token)
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
        role_info = get_info_by_token(instance.token).to_json()
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
            return response_not_found_404(status=STATUS_NOT_FOUND_ERROR, message=f"该手机号({phone_number})未被注册!!")
        # 检测验证码是否正确
        if not judge_code(phone_number, request.data.get('code')):
            message = "验证码不正确"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
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
        role_info = get_info_by_token(instance.token).to_json()
        return response_success_200(message="成功!!!!", data=serializer.data, role_info=role_info)

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


# 根据token获得详细信息
def get_info_by_token(token):
    dk = my_decode_token(token)
    if not dk:
        return None
    return get_info(int(dk[0]), int(dk[1]))


# 根据用户id和role获得详细信息
def get_info(user_id: int, role: int):
    print(f'userId={user_id}, role={role}')
    # 老师(0) 或 辅导员(3)
    if role == 0 or role == 3:
        return Teacher.objects.get(user_info_id=user_id)
    # 学生
    elif role == 1:
        return Student.objects.get(user_info_id=user_id)
    # 家长
    elif role == 2:
        return Parent.objects.get(user_info_id=user_id)
    elif role == -1:
        return User.objects.get(id=user_id)
    return "wu"
