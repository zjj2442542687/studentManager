import pandas as pd
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from parent.models import Parent
from parent.views.parent_serializers import ParentInfoSerializersAll, ParentInfoSerializersInsert
from parent.views.views import check_parent_insert_info
from student.views.views import create_user_details_and_user
from user.models import User
from user_details.models import UserDetails
from utils.my_card import IdCard
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_phone_number, pd_qq, pd_email, pd_adm_token, STATUS_PARAMETER_ERROR
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.my_time import date_to_time_stamp


class ParentInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersInsert

    @swagger_auto_schema(
        operation_summary="管理员添加数据",
        request_body=request_body(properties={
            'name': string_schema('家长姓名'),
            'card': string_schema('身份证'),
            'phone_number': string_schema('电话号码'),
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

        check_info = check_parent_insert_info(request)
        if check_info:
            return check_info

        # 创建用户详情和用户
        create_user_details_and_user(request, 2)

        resp = super().create(request)
        return response_success_200(data=resp.data)


class ParentInsertFileView(mixins.CreateModelMixin,
                           GenericViewSet):
    """
    Batch_import：
    Excel文件批量导入数据

    无描述
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="家长信息批量导入",
        operation_description="传入文件ID",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='文件 '),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
    )
    def batch_import(self, request, *args, **kwargs):
        # check_token = pd_adm_token(request)
        # if check_token:
        #     return check_token

        file = request.FILES.get("file")
        check_file = batch_import_test(file)
        if check_file:
            return check_file

        excel_data = pd.read_excel(file, header=0, dtype='str')
        for dt in excel_data.iterrows():
            # 添加用户信息
            card = dt[1]['身份证']
            phone_number = dt[1]['手机号码']
            if not dt[1]['家长姓名'] or not card:
                continue
            if User.objects.filter(user_name=card):
                message = card + "身份证已经注册存在"
                return response_success_200(code=STATUS_PARAMETER_ERROR, message=message)
            if User.objects.filter(phone_number=phone_number):
                message = phone_number + "手机号码已经存在"
                return response_success_200(code=STATUS_PARAMETER_ERROR, message=message)
            # print(dt[1]['班级'])
            print(phone_number)

            password = my_encode(phone_number)
            # 分析身份证
            id_card = IdCard(card)
            # 创建用户详情
            user_details_id = UserDetails.objects.create(
                name=dt[1]['家长姓名'],
                sex=id_card.sex,
                card=card,
                birthday=date_to_time_stamp(year=id_card.birth_year, month=id_card.birth_month, day=id_card.birth_day),
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            ).id
            # 创建user
            user_id = User.objects.create(
                user_name=card, password=password,
                phone_number=phone_number, role=2, user_details_id=user_details_id
            ).id
            Parent.objects.create(
                user_id=user_id,
            )

        return response_success_200(message="成功!!!!")


def batch_import_test(file):
    excel_data = pd.read_excel(file, header=0, dtype='str')
    test = []
    i = 1
    card_list = []
    phone_list = []

    for dt in excel_data.iterrows():
        i = i + 1
        message = ""

        card = dt[1]['身份证']
        phone_number = dt[1]['手机号码']
        qq = dt[1]['QQ(选填)']
        email = dt[1]['邮箱(选填)']

        if not dt[1]['家长姓名'] or not card or not phone_number:
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

        #  验证qq号
        if not qq and not pd_qq(qq):
            message += ",qq号格式错误"

        # 验证邮箱
        if not email and not pd_email(email):
            message += ",邮箱格式错误"

        if message:
            test.append({"index": i, "message": message})
        card_list.append(card)
    if phone_number:
        phone_list.append(phone_number)

    if len(test) > 0:
        return response_error_400(code=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
