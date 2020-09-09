import re

from drf_yasg.openapi import FORMAT_DATE, FORMAT_DATETIME
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersInsert
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema, array_schema


class RegularAddRecordInsertView(mixins.CreateModelMixin,
                                 GenericViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersInsert

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        operation_description="描述",
        request_body=request_body(properties={
            'describe': string_schema(description="我是描述", default="默认值", title="标题"),
            'regular': integer_schema('描述', default=1),
            'reminder_time': string_schema('提醒时间', default="12:00", f=FORMAT_DATE),
            'start_time': string_schema('每天开始的时间', default="12:00", f=FORMAT_DATE),
            'end_time': string_schema('每天结束的时间', default="12:00", f=FORMAT_DATE),
            'start_date': string_schema('开始日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
            'end_date': string_schema('结束日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
            'week': array_schema('周'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        print(request.data)
        print(request.GET.get("week"))

        resp = super().create(request)
        return response_success_200(data=resp.data)
