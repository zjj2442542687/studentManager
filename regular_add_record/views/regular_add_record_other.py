import time

from drf_yasg.openapi import FORMAT_DATETIME
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersInsert
from regular_add_record.views.views import check_authority, check_update_time
from utils.my_info_judge import pd_token
from utils.my_response import *

from utils.my_swagger_auto_schema import request_body, string_schema, array_schema, integer_schema


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
        # 需要修改的检测
        pk = kwargs['pk']

        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检查权限
        check = check_authority(self, request, pk)
        if check:
            return check

        # 删除
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改!!",
        operation_description=f"当前的时间戳是 {int(time.time())}",
        request_body=request_body(properties={
            'describe': string_schema(description="我是描述", default="默认值", title="标题"),
            'regular': integer_schema('描述', default=1),
            'reminder_time': integer_schema('提醒时间'),
            'start_time': integer_schema('每天开始的时间'),
            'end_time': integer_schema('每天结束的时间'),
            'start_date': integer_schema('开始日期时间'),
            'end_date': integer_schema('结束日期时间'),
            'week': array_schema('周'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        # 需要修改的检测
        pk = kwargs['pk']

        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检查权限
        check = check_authority(self, request, pk)
        if check:
            return check
        # 判断时间
        check_time = check_update_time(request, pk)
        if check_time:
            return check_time

        resp = super().partial_update(request, *args, **kwargs)

        return response_success_200(data=resp.data)
