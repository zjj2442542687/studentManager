from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_update_info
from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersInsert
from regular_add_record.views.views import check_authority, check_info
from utils.my_info_judge import pd_super_adm_token, pd_token
from utils.my_response import *
from rest_framework.parsers import MultiPartParser

from utils.my_utils import get_regular_all_id


class RegularAddRecordOtherView(ModelViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersInsert
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除RegularAddRecord的信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检查权限
        check = check_authority(self, request, kwargs)
        if check:
            return check

        # 删除
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改!!",
        required=[],
        manual_parameters=[
            openapi.Parameter('describe', openapi.IN_FORM, type=openapi.TYPE_STRING, description='标题'),
            openapi.Parameter('regular', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='习惯的id',
                              enum=get_regular_all_id()),
            openapi.Parameter('reminder_time', openapi.IN_FORM, type=openapi.TYPE_STRING, description='提醒时间'),
            openapi.Parameter('start_time', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='每天开始的时间'),
            openapi.Parameter('end_time', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='每天结束的时间'),
            openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description='开始日期时间',
                              format=openapi.FORMAT_DATETIME),
            openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description='结束日期时间',
                              format=openapi.FORMAT_DATETIME),
            openapi.Parameter('week', openapi.IN_FORM, type=openapi.TYPE_ARRAY, description='周',
                              items=openapi.Items(type=openapi.TYPE_INTEGER)),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_info(request)

        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检查权限
        check = check_authority(self, request, kwargs)
        if check:
            return check

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)


