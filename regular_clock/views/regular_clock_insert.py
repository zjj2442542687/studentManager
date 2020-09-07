import pandas as pd
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status

from parent.models import Parent
from FileInfo.models import FileInfo
from parent.views.parent_serializers import ParentInfoSerializersAll
from user.models import User
from user_details.models import UserDetails
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_phone_number, pd_qq, pd_email, pd_adm_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema


class RegularInsertView(mixins.CreateModelMixin,
                        GenericViewSet):

    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersAll

    @swagger_auto_schema(
        request_body=request_body(properties={
            'name': string_schema('家长姓名'),
            'sex': string_schema('性别'),
            'card': string_schema('身份证'),
            'phone_number': string_schema('电话号码'),
            'birthday': string_schema('生日'),
            'qq': string_schema('QQ'),
            # 'email': string_schema('邮件'),
        }),
        deprecated=True
    )
    def create(self, request, *args, **kwargs):
        # user_info = request.data.get('user_info')
        # if not User.objects.filter(id=user_info):
        #     message = "用户ID不存在"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        # 添加用户信息
        card = request.data.get('card')
        phone_number = request.data.get('phone_number')
        # 用户检查是否存在
        if User.objects.filter(user_name=card):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
        if User.objects.filter(phone_number=phone_number):
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
        password = my_encode(phone_number)
        user: User = User.objects.get_or_create(user_name=card, password=password, phone_number=phone_number,
                                                role=2)
        request.data["user_info"] = User.objects.get(user_name=card).id
        resp = super().create(request)
        return response_success_200(data=resp.data)

    # @swagger_auto_schema(
    #     operation_summary="家长信息批量导入",
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
    #         phone_number = dt[1]['手机号码']
    #         if not dt[1]['家长姓名'] or not dt[1]['性别'] or not card:
    #             continue
    #         # print(dt[1]['班级'])
    #         User.objects.get_or_create(user_name=card, password=phone_number,
    #                                                 phone_number=phone_number, role=2)
    #         Parent.objects.create(
    #             user_info=User.objects.get(user_name=card),
    #             name=dt[1]['家长姓名'],
    #             sex=dt[1]['性别'],
    #             card=card,
    #             phone_number=phone_number,
    #             birthday=dt[1]['生日'],
    #             qq=dt[1]['QQ(选填)'],
    #             email=dt[1]['邮箱(选填)'],
    #         )
    #
    #     return response_success_200(message="成功!!!!")


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
            if not dt[1]['家长姓名'] or not dt[1]['性别'] or not card:
                continue
            if User.objects.filter(user_name=card):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
            if User.objects.filter(phone_number=phone_number):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
            # print(dt[1]['班级'])
            print(phone_number)
            password = my_encode(phone_number)
            # 创建用户详情
            user_details_id = UserDetails.objects.create(
                name=dt[1]['家长姓名'],
                sex=-1 if dt[1]['性别'] == '女' else (1 if dt[1]['性别'] == '男' else 0),
                card=card,
                birthday=dt[1]['生日'],
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
    i = 0
    card_list = []
    phone_list = []

    for dt in excel_data.iterrows():
        i = i + 1
        message = ""

        card = dt[1]['身份证']
        phone_number = dt[1]['手机号码']
        qq = dt[1]['QQ(选填)']
        email = dt[1]['邮箱(选填)']

        if not dt[1]['家长姓名'] or not dt[1]['性别'] or not card or not phone_number or not dt[1]['生日']:
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
            phone_list.append(phone_number)

    if len(test) > 0:
        return response_error_400(status=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
