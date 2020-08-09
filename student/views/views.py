import pandas as pd
from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from student.models import Student
from FileInfo.models import FileInfo
from utils.my_response import *
from classs.models import Class
from user.models import User
from utils.my_swagger_auto_schema import *


class StudentInfoSerializers(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create:
    添加一条学生信息数据

    无描述
    """

    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'name': string_schema('学生姓名'),
            'sex': string_schema('性别'),
            'card': string_schema('身份证'),
            'clazz': string_schema('班级名称'),
            'phone_number': string_schema('电话号码'),
            'school': string_schema('学校名字'),
            'birthday': string_schema('生日'),
            'qq': string_schema('QQ'),
            'email': string_schema('邮件'),
        })
    )
    def create(self, request, *args, **kwargs):
        school = request.data.get('school')
        # 学校关联
        if not School.objects.get(school_name=school):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
        school_id = School.objects.get(school_name=school).id
        request.data["school"] = school_id
        # 班级关联
        clazz = request.data.get('clazz')
        if not Class.objects.get(class_name=clazz):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="班级不存在")
        clazz_id = Class.objects.get(class_name=clazz).id
        request.data["clazz"] = clazz_id
        # 添加用户信息
        card = request.data.get('card')
        phone_number = request.data.get('phone_number')
        # 用户检查是否存在
        if User.objects.filter(user_name=card):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
        if User.objects.filter(phone_number=phone_number):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
        user: User = User.objects.get_or_create(user_name=card, password=phone_number, phone_number=phone_number,
                                                role=1)
        request.data["user_info"] = User.objects.get(user_name=card).id

        resp = super().create(request)
        return response_success_200(data=resp.data)

    # @swagger_auto_schema(
    #     operation_summary="学生信息批量导入",
    #     operation_description="传入文件ID",
    #     request_body=request_body(
    #         properties={
    #             "id": integer_schema('文件ID'),
    #         }
    #     )
    # )
    # def Batch_import(self, request, *args, **kwargs):
    #     file_id = request.data.get('id')
    #     file_name = Update.objects.get(id=file_id).file
    #     excel_data = pd.read_excel(file_name, header=0, dtype='str')
    #     for dt in excel_data.iterrows():
    #         # 添加用户信息
    #         card = dt[1]['身份证']
    #         phone_number = dt[1]['手机号码(选填)']
    #         if not dt[1]['学生姓名'] or not dt[1]['性别'] or not card or not dt[1]['班级'] or not dt[1]['学校名称']:
    #             continue
    #         User.objects.get_or_create(user_name=card, password=phone_number,
    #                                                 phone_number=phone_number, role=1)
    #         Student.objects.create(
    #             user_info=User.objects.get(user_name=card),
    #             name=dt[1]['学生姓名'],
    #             sex=dt[1]['性别'],
    #             card=dt[1]['身份证'],
    #             phone_number=phone_number,
    #             clazz=Class.objects.get(class_name=dt[1]['班级']),
    #             school=School.objects.get(school_name=dt[1]['学校名称']),
    #             birthday=dt[1]['生日'],
    #             qq=dt[1]['QQ(选填)'],
    #             email=dt[1]['邮箱(选填)'],
    #         )
    #
    #     return response_success_200(message="成功!!!!")


class StudentInsertFileView(mixins.CreateModelMixin,
                            GenericViewSet):
    """
    Batch_import：
    Excel文件批量导入数据

    无描述
    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="学生信息批量导入",
        operation_description="传入文件ID",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='文件 ')
        ],
    )
    def Batch_import(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        excel_data = pd.read_excel(file, header=0, dtype='str')
        for dt in excel_data.iterrows():
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码(选填)']
            school = dt[1]['学校名称']
            class_name = dt[1]['班级']
            if not dt[1]['学生姓名'] or not dt[1]['性别'] or not card or not dt[1]['班级'] or not dt[1]['学校名称']:
                continue
            if User.objects.filter(user_name=card):
                message = card+"身份证已经注册存在"
                print(message)
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message=message)
            if User.objects.filter(phone_number=phone_number):
                message = card + phone_number
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message=message)
            if not School.objects.filter(school_name=school):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
            if not Class.objects.filter(class_name=class_name):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
            User.objects.get_or_create(user_name=card, password=phone_number,
                                       phone_number=phone_number, role=1)
            Student.objects.create(
                user_info=User.objects.get(user_name=card),
                name=dt[1]['学生姓名'],
                sex=dt[1]['性别'],
                card=dt[1]['身份证'],
                phone_number=phone_number,
                clazz=Class.objects.get(class_name=dt[1]['班级']),
                school=School.objects.get(school_name=dt[1]['学校名称']),
                birthday=dt[1]['生日'],
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            )

        return response_success_200(message="成功!!!!")


class StudentOtherView(ModelViewSet):
    """

    destroy:删除学生信息

    根据id删除用户信息

    输入id删除


    FileInfo:修改学生表信息

    根据id修改用户信息

    输入id修改

    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers


class StudentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有学生信息

    无描述

    retrieve:
    根据id查询学生信息

    输入id

    retrieve_by_student_name:
    根据名字查询学生信息

    输入姓名

    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    def retrieve_by_student_name(self, request, *args, **kwargs):
        try:
            # instance = self.queryset.get(user_name=kwargs.get("student_name"))
            # 模糊查询
            # instance = self.queryset.get(name__contains=kwargs.get("name"))
            instance = self.queryset.get(user_name=kwargs.get("student_name"))
        except Student.DoesNotExist:
            return response_error_500(status=STATUS_NOT_FOUND_ERROR, message="没找到")
        except Student.MultipleObjectsReturned:
            return response_error_500(status=STATUS_MULTIPLE_ERROR, message="找到多个姓名相同用户")
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
