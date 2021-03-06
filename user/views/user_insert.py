from drf_yasg.openapi import FORMAT_PASSWORD
from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from parent.models import Parent
from schooladm.models import Schooladm
from student.models import Student
from teacher.models import Teacher
from user.views.urls import judge_code, check_phone_number, check_user_name
from user.views.user_serializers import UserInfoSerializersAll, UserInfoSerializersLess
from user_details.views.urls import *
from school.models import School
from utils.my_encryption import my_encode, my_encode_token
from utils.my_info_judge import pd_phone_number, pd_adm_token, pd_super_adm_token
from utils.my_response import *
from utils.my_swagger_auto_schema import *
from utils.status import *


class UserInsertView(mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersLess

    @swagger_auto_schema(
        operation_summary="添加一条用户数据",
        operation_description="添加一条用户数据",
        request_body=request_body(properties={
            'user_name': string_schema('用户名'),
            'password': string_schema('密码', f=FORMAT_PASSWORD),
            'phone_number': string_schema('手机号'),
            'role': integer_schema('角色(0, 老师), (1, 学生), (2, 家长)', default=1),
            'name': string_schema('真实姓名'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
        # deprecated=True
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 用户名
        user_name = request.data.get('user_name')
        # 手机号
        phone_number = request.data.get("phone_number")
        # 密码
        password = request.data.get("password")
        # 角色
        role = request.data.get('role')
        # 真实姓名
        name = request.data.get('name')

        if not (role == 0 or role == 1 or role == 2):
            return response_success_200(code=STATUS_PARAMETER_ERROR, message="role的取值为(0, 1, 2)")

        if not pd_phone_number(phone_number):
            message = "手机号格式错误"
            return response_success_200(code=STATUS_PHONE_NUMBER_DUPLICATE, message=message)

        if check_user_name(user_name):
            message = "用户名已存在"
            return response_success_200(code=STATUS_USER_NAME_DUPLICATE, message=message)
        if check_phone_number(phone_number):
            message = "该手机号已被注册"
            return response_success_200(code=STATUS_PHONE_NUMBER_DUPLICATE, message=message)

        # 创建用户详情 并获得他的id
        user_details_id = UserDetails.objects.create(name=name).id

        # 加密
        request.data["password"] = my_encode(password)
        request.data['user_details'] = user_details_id
        request.data['token'] = "-1"

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 创建角色信息
        user_id = serializer.data['id']
        if role == 0:
            save_teacher = Teacher(user_id=user_id)
            save_teacher.save()
        elif role == 1:
            save_student = Student(user_id=user_id)
            save_student.save()
        elif role == 2:
            save_parent = Parent(user_id=user_id)
            save_parent.save()
        else:
            message = "角色不存在"
            return response_success_200(status=STATUS_CODE_ERROR, message=message)
        # data = serializer.data
        print(f'数据是：{serializer.data}')
        return response_success_200(code=STATUS_200_SUCCESS, data=serializer.data, headers=headers)

    @swagger_auto_schema(
        operation_summary="添加一条学校管理员数据",
        operation_description="添加一条学校管理员数据",
        request_body=request_body(properties={
            'user_name': string_schema('用户名'),
            'password': string_schema('密码', f=FORMAT_PASSWORD),
            'phone_number': string_schema('手机号'),
            'name': string_schema('真实姓名'),
            'school_id': integer_schema('学校的id'),
        }),
        manual_parameters=[
            # openapi.Parameter('school_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
            #                   description='学校的id'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员TOKEN'),
        ],
    )
    def create_stu_adm(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        # 用户名
        user_name = request.data.get('user_name')
        # 手机号
        phone_number = request.data.get("phone_number")
        # 密码
        password = request.data.get("password")
        # 真实姓名
        name = request.data.get('name')
        # 真实姓名
        school_id = request.data.get('school_id')

        if check_user_name(user_name):
            message = "用户名已存在"
            return response_success_200(code=STATUS_USER_NAME_DUPLICATE, message=message)
        if check_phone_number(phone_number):
            message = "该手机号已被注册"
            return response_success_200(code=STATUS_PHONE_NUMBER_DUPLICATE, message=message)
        if not pd_phone_number(phone_number):
            message = "手机号格式错误"
            return response_success_200(code=STATUS_PHONE_NUMBER_DUPLICATE, message=message)

        # 创建用户详情 并获得他的id
        user_details_id = UserDetails.objects.create(name=name).id

        # 加密
        # request.data["password"] = my_encode(password)
        # request.data['user_details'] = user_details_id
        # request.data['role'] = -2
        # request.data['token'] = "-1"

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return response_success_200(code=STATUS_200_SUCCESS, data=serializer.data, headers=headers)

        # 创建user
        user_id = User.objects.create(
            user_name=user_name, password=my_encode(password),
            phone_number=phone_number, role=-2, user_details_id=user_details_id, token=-1
        ).id
        Schooladm.objects.create(
            school_id=school_id, user_id=user_id,
        )

        return response_success_200(message="成功!!!!")
