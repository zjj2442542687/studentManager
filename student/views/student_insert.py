import pandas as pd
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from classs.models import Class
from parent.models import Parent
from school.models import School
from student.models import Student
from student.views.student_serializers import StudentInfoSerializersInsert
from student.views.views import check_student_insert_info, create_user_details_and_user
from user.models import User
from user_details.models import UserDetails
from utils.my_card import IdCard
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_phone_number, pd_token, pd_adm_token, STATUS_TOKEN_NO_AUTHORITY, \
    STATUS_PARAMETER_ERROR
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import *
from utils.my_time import date_to_time_stamp


class StudentInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersInsert

    @swagger_auto_schema(
        operation_summary="添加一条数据",
        request_body=request_body(properties={
            'name': string_schema('学生姓名'),
            'card': openapi.Schema(type=openapi.TYPE_STRING, description="身份证"),
            'clazz': integer_schema('班级id'),
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

        # 检测插入的数据
        check_insert = check_student_insert_info(request)
        if check_insert:
            return check_insert

        # 创建userDetails和user, 并将user的id放到request中
        create_user_details_and_user(request, 1)

        resp = super().create(request)
        return response_success_200(data=resp.data)

    @swagger_auto_schema(
        operation_description="传入学生id和家长id",
        operation_summary="学生添加家长",
        request_body=request_body(properties={
            'parent_id': integer_schema('家长id'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='student的TOKEN'),
        ]
    )
    def add_parent(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth != 1:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        student_id = Student.objects.get(user_id=request.user).id
        parent_id = request.data.get('parent_id')

        if not Parent.objects.filter(id=parent_id).exists():
            return response_success_200(message="未找到该信息")
        print(student_id)
        print(parent_id)
        self.queryset.get(pk=student_id).parent.add(parent_id)

        return response_success_200(message="成功")


class StudentInsertFileView(mixins.CreateModelMixin,
                            GenericViewSet):
    """
    Batch_import：
    Excel文件批量导入数据

    无描述
    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersInsert
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="学生信息批量导入",
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
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码(选填)']
            school = dt[1]['学校名称']
            class_name = dt[1]['班级']
            if not dt[1]['学生姓名'] or not card or not dt[1]['班级'] or not dt[1]['学校名称']:
                continue
            if User.objects.filter(user_name=card):
                message = card + "身份证已经注册存在"
                print(message)
                return response_success_200(code=STATUS_PARAMETER_ERROR, message=message)
            if User.objects.filter(phone_number=phone_number):
                message = card + phone_number
                return response_success_200(code=STATUS_PARAMETER_ERROR, message=message)
            if not School.objects.filter(school_name=school):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="学校不存在")
            if not Class.objects.filter(class_name=class_name):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="学校不存在")
            password = my_encode(phone_number)

            # 分析身份证
            id_card = IdCard(card)
            # 创建用户详情
            user_details_id = UserDetails.objects.create(
                name=dt[1]['学生姓名'],
                sex=id_card.sex,
                card=card,
                birthday=date_to_time_stamp(year=id_card.birth_year, month=id_card.birth_month, day=id_card.birth_day),
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            ).id
            # 创建user
            user_id = User.objects.create(
                user_name=card, password=password,
                phone_number=phone_number, role=1, user_details_id=user_details_id
            ).id
            Student.objects.create(
                user_id=user_id,
                clazz=Class.objects.get(class_name=dt[1]['班级']),
                school=School.objects.get(school_name=school)
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
        # 添加用户信息
        card = dt[1]['身份证']
        phone_number = dt[1]['手机号码(选填)']
        school = dt[1]['学校名称']
        class_name = dt[1]['班级']

        if not dt[1]['学生姓名'] or not card or not class_name or not school:
            message += "有空字段"

        # 判断身份证的格式是否存在
        if not pd_card(card):
            message += ",身份证格式错误"
        elif card in card_list:
            message += f",身份证和{card_list.index(card) + 1}重复"
        elif UserDetails.objects.filter(card=card):
            message += ",身份证已经注册存在"

        if phone_number:
            if not pd_phone_number(phone_number):
                message += ",手机号格式错误"
            elif phone_number in phone_list:
                message += f",手机号和{phone_list.index(phone_number) + 1}重复"
            elif User.objects.filter(phone_number=phone_number):
                message += ",手机号码已经注册存在"

        if not School.objects.filter(school_name=school):
            message += ",学校不存在"
        elif not Class.objects.filter(class_name=class_name, school_id=School.objects.get(school_name=school).id):
            message += ",学校中班级名不存在"

        if message:
            test.append({"index": i, "message": message})
        card_list.append(card)
        if phone_number:
            phone_list.append(phone_number)

    if len(test) > 0:
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
