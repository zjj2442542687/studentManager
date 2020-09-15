from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from student.views.views import create_user_details_and_user
from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherInfoSerializersAll, TeacherInfoSerializersInsert
from teacher.views.views import check_teacher_insert_info
from user_details.models import UserDetails
from utils.my_card import IdCard
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_phone_number, pd_qq, pd_email, pd_adm_token, STATUS_PARAMETER_ERROR
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from school.models import School
from user.models import User
import pandas as pd

from utils.my_time import date_to_time_stamp


class TeacherInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersInsert

    @swagger_auto_schema(
        operation_summary="教师信息单独导入",
        operation_description="说明：身份证和电话号码必须未注册过，学校必须存在",
        request_body=request_body(properties={
            'name': string_schema('老师姓名'),
            'card': string_schema('身份证'),
            'title': string_schema('职称'),
            'phone_number': string_schema('电话号码'),
            'school': integer_schema('学校id'),
            'qq': string_schema('QQ'),
            'email': string_schema('邮件'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 检测teacher插入的合法性
        check_info = check_teacher_insert_info(request)
        if check_info:
            return check_info

        # 创建用户详情和用户
        create_user_details_and_user(request, 0)

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
                              description='文件 '),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
    )
    def batch_import(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        file = request.FILES.get("file")
        check_file = batch_import_test(file)
        if check_file:
            return check_file
        excel_data = pd.read_excel(file, header=0, dtype='str')
        for dt in excel_data.iterrows():
            if not dt[1]['老师姓名'] or not dt[1]['身份证'] or not dt[1]['学校名称']:
                continue
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码']
            school = dt[1]['学校名称']
            if User.objects.filter(user_name=card):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
            if User.objects.filter(phone_number=phone_number):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
            if not School.objects.filter(school_name=school):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="学校不存在")
            password = my_encode(phone_number)
            # 分析身份证
            id_card = IdCard(card)
            # 创建用户详情
            user_details_id = UserDetails.objects.create(
                name=dt[1]['老师姓名'],
                sex=id_card.sex,
                card=card,
                birthday=date_to_time_stamp(year=id_card.birth_year, month=id_card.birth_month, day=id_card.birth_day),
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            ).id
            # 创建user
            user_id = User.objects.create(
                user_name=card, password=password,
                phone_number=phone_number, role=0, user_details_id=user_details_id
            ).id
            Teacher.objects.create(
                user_id=user_id,
                title=dt[1]['职称'],
                school=School.objects.get(school_name=school),
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

        if not dt[1]['老师姓名'] or not card or not school:
            message += "有空字段"

        # 判断身份证的格式是否存在
        if not pd_card(card):
            message += ",身份证格式错误"
        elif card in card_list:
            message += f",身份证和{card_list.index(card) + 1}重复"
        elif UserDetails.objects.filter(card=card):
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
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
