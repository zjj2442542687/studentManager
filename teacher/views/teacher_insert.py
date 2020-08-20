from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherInfoSerializersAll
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_phone_number, pd_qq, pd_email
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from school.models import School
from user.models import User
import pandas as pd


class TeacherInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersAll

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
        if not School.objects.filter(school_name=school):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
        school_id = School.objects.get(school_name=school).id
        request.data["school"] = school_id
        # 添加用户信息
        card = request.data.get('card')
        phone_number = request.data.get('phone_number')
        # 用户检查是否存在
        if User.objects.filter(user_name=card):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
        if User.objects.filter(phone_number=phone_number):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
        password = my_encode(phone_number)
        User.objects.get_or_create(user_name=card, password=password, phone_number=phone_number,
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
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersAll
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
    def batch_import(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        check_file = batch_import_test(file)
        if check_file:
            return check_file
        excel_data = pd.read_excel(file, header=0, dtype='str')
        for dt in excel_data.iterrows():
            if not dt[1]['老师姓名'] or not dt[1]['性别'] or not dt[1]['身份证'] or not dt[1]['学校名称']:
                continue
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码']
            school = dt[1]['学校名称']
            if User.objects.filter(user_name=card):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
            if User.objects.filter(phone_number=phone_number):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
            if not School.objects.filter(school_name=school):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
            password = my_encode(phone_number)
            User.objects.get_or_create(user_name=card, password=password,
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
        return response_success_200(message="成功!!!!")


def batch_import_test(file):
    excel_data = pd.read_excel(file, header=0, dtype='str')
    test = []
    i = 0
    card_list = []
    phone_list = []
    for dt in excel_data.iterrows():
        i = i + 1
        message = ""

        card = dt[1]['身份证']
        phone_number = dt[1]['手机号码']
        school = dt[1]['学校名称']
        qq = dt[1]['QQ(选填)']
        email = dt[1]['邮箱(选填)']

        if not dt[1]['老师姓名'] or not dt[1]['性别'] or not card or not school:
            message += "有空字段"

        # 判断身份证的格式是否存在
        if not pd_card(card):
            message += ",身份证格式错误"
        elif card in card_list:
            message += f",身份证和{card_list.index(card) + 1}重复"
        elif User.objects.filter(user_name=card):
            message += ",身份证已经注册存在"

        if not pd_phone_number(phone_number):
            message += ",手机号格式错误"
        elif phone_number in phone_list:
            message += f",手机号和{phone_list.index(phone_number) + 1}重复"
        elif User.objects.filter(phone_number=phone_number):
            message += ",手机号码已经注册存在"

        if not School.objects.filter(school_name=school):
            message += ",学校不存在"

        #  验证qq号
        if not qq and not pd_qq(qq):
            message += ",qq号格式错误"

        # 验证邮箱
        if not email and not pd_email(email):
            message += ",邮箱格式错误"

        if message:
            test.append({"index": i, "message": message})
        card_list.append(card)
        phone_list.append(phone_number)
    if len(test) > 0:
        return response_error_400(status=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
