from drf_yasg.openapi import FORMAT_DATE, FORMAT_DATETIME
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

from utils.my_swagger_auto_schema import request_body, string_schema, array_schema, integer_schema
from utils.my_utils import get_regular_all_id


class RegularAddRecordOtherView(ModelViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersInsert

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
        request_body=request_body(properties={
            'describe': string_schema(description="我是描述", default="默认值", title="标题"),
            'regular': integer_schema('描述', default=1),
            'reminder_time': string_schema('提醒时间', default="12:00"),
            'start_time': string_schema('每天开始的时间', default="12:00"),
            'end_time': string_schema('每天结束的时间', default="12:00"),
            'start_date': string_schema('开始日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
            'end_date': string_schema('结束日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
            'week': array_schema('周'),
        }),
        manual_parameters=[
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


