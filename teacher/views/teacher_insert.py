import xlrd
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from school.models import School
from user.models import User
from studentManager import settings
from FileInfo.models import FileInfo
import pandas as pd


class TeacherInfoSerializers(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create:
    添加一条数据

    无描述

    Batch_import：
    Excel文件批量导入数据

    无描述
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers

    @swagger_auto_schema(
        operation_summary="教师信息单独导入",
        operation_description="说明：身份证和电话号码必须未注册过，学校必须存在",
        request_body=request_body(properties={
            'name': string_schema('老师姓名'),
            'sex': string_schema('性别'),
            'card': string_schema('身份证'),
            'title': string_schema('职称'),
            'identity': string_schema('身份'),
            # 'clazz': integer_schema('班级'),
            'phone_number': string_schema('电话号码'),
            'school': string_schema('学校名字'),
            'birthday': string_schema('生日'),
            'qq': string_schema('QQ'),
            'email': string_schema('邮件'),
        })
    )
    def create(self, request, *args, **kwargs):
        # 学校关联
        school = request.data.get('school')
        if not School.objects.get(school_name=school):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
        school_id = School.objects.get(school_name=school).id
        request.data["school"] = school_id
        # 添加用户信息
        card = request.data.get('card')
        phone_number = request.data.get('phone_number')
        # 用户检查是否存在
        if User.objects.get(user_name=card):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
        if User.objects.get(phone_number=phone_number):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
        User.objects.get_or_create(user_name=card, password=phone_number, phone_number=phone_number,
                                   role=0)
        request.data["user_info"] = User.objects.get(user_name=card).id

        resp = super().create(request)
        return response_success_200(data=resp.data)


class TeacherInsertFileView(mixins.CreateModelMixin,
                            GenericViewSet):
    """
    create:
    添加一条数据

    无描述

    Batch_import：
    Excel文件批量导入数据

    无描述
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializers
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="教师信息批量导入",
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
            if not dt[1]['老师姓名'] or not dt[1]['性别'] or not dt[1]['身份证'] or not dt[1]['学校名称']:
                continue
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码']
            school = dt[1]['学校名称']
            if User.objects.get(user_name=card):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
            if User.objects.get(phone_number=phone_number):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
            if not School.objects.get(school_name=school):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
            User.objects.get_or_create(user_name=card, password=phone_number,
                                       phone_number=phone_number, role=0)
            Teacher.objects.create(
                user_info=User.objects.get(user_name=card),
                name=dt[1]['老师姓名'],
                sex=dt[1]['性别'],
                card=card,
                title=dt[1]['职称'],
                identity=dt[1]['身份'],
                phone_number=phone_number,
                school=School.objects.get(school_name=school),
                birthday=dt[1]['生日'],
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            )
            # print(excel_data[i][i])
            # print(excel_data[i][:])
        # file = request.FILES.get('file')

        # 循环二进制写入		括号里是settings 配置的路径
        # with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
        #     for i in file.readlines():
        #         f.write(i)
        #
        # excel = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + file.name)
        # excel.sheet_names()

        #  获取 sheet_by_index(0) 下标是0 的value
        # sheet = excel.sheet_by_index(0)
        #	sheet.row_values(1) 	当前下标的值，打印出来看下就知道
        # print(sheet.row_values(1))

        #	sheet.nrows 总行数   sheet.ncols 总列数
        # print(sheet.nrows)
        # print(sheet.ncols)
        return response_success_200(message="成功!!!!")
