import time

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersInsert
from regular_add_record.views.views import check_insert_time
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema, array_schema


class RegularAddRecordInsertView(mixins.CreateModelMixin,
                                 GenericViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersInsert

    @swagger_auto_schema(
        operation_summary="添加数据 ",
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
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        # 先检测用户输入的时间的规范性
        check_time = check_insert_time(request)
        if check_time:
            return check_time

        check_token = pd_token(request)
        if check_token:
            return check_token

        resp = super().create(request)
        return response_success_200(data=resp.data)
