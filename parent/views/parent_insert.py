import pandas as pd
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from FileInfo.models import FileInfo
from user.models import User
from utils.my_encryption import my_encode
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema


class ParentInfoSerializers(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class ParentInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """

    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'name': string_schema('家长姓名'),
            'sex': string_schema('性别'),
            'card': string_schema('身份证'),
            'phone_number': string_schema('电话号码'),
            'birthday': string_schema('生日'),
            'qq': string_schema('QQ'),
            # 'email': string_schema('邮件'),
        })
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
    serializer_class = ParentInfoSerializers
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="家长信息批量导入",
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
            phone_number = dt[1]['手机号码']
            if not dt[1]['家长姓名'] or not dt[1]['性别'] or not card:
                continue
            if User.objects.filter(user_name=card):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
            if User.objects.filter(phone_number=phone_number):
                return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")
            # print(dt[1]['班级'])
            password = my_encode(phone_number)
            User.objects.get_or_create(user_name=card, password=password,
                                       phone_number=phone_number, role=2)
            Parent.objects.create(
                user_info=User.objects.get(user_name=card),
                name=dt[1]['家长姓名'],
                sex=dt[1]['性别'],
                card=card,
                phone_number=phone_number,
                birthday=dt[1]['生日'],
                qq=dt[1]['QQ(选填)'],
                email=dt[1]['邮箱(选填)'],
            )

        return response_success_200(message="成功!!!!")
