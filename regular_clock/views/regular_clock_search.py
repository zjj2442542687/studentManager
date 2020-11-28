import datetime

from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from regular_add_record.models import RegularAddRecord
from regular_clock.models import RegularClock
from regular_clock.views.regular_clock_serializers import RegularClockSerializersSearch
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_success_200
from utils.my_time import date_to_time_stamp


class RegularClockPaginationSelectView(mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       GenericViewSet):
    queryset = RegularClock.objects.all()
    serializer_class = RegularClockSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="用户打卡信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('regular_add_record', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='regular_add_record的id'),
            openapi.Parameter('clock_in_time', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='打卡的时间戳， 传yyyy年MM月dd日的时间戳,表示查询该日下的打卡'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # token 返回regularClock
        regular_clock = search_token(request)

        # regular_add_record_id 查询
        regular_add_record_id = request.GET.get("regular_add_record")
        regular_clock = search_regular_add_record(regular_add_record_id, regular_clock)

        # clock_in_time 查询
        chock_in_time = request.GET.get("clock_in_time")
        regular_clock, pd = search_clock_in_time(chock_in_time, regular_clock)
        if not pd:
            return regular_clock

        page = self.paginate_queryset(regular_clock)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


# 根据用户传过来的token返回regularClock 的数据
def search_token(request):
    if request.auth == -1:  # 超级管理员
        return RegularClock.objects.all()

    regular_add_record = RegularAddRecord.objects.filter(user_id=request.user)
    return RegularClock.objects.filter(regular_add_record_id__in=[r.id for r in regular_add_record])


def search_regular_add_record(regular_add_record_id, regular_clock: QuerySet):
    if regular_add_record_id:
        # 查询用户添加的
        return regular_clock.filter(regular_add_record_id=regular_add_record_id)
    else:
        return regular_clock


def search_clock_in_time(clock_in_time, regular_clock: QuerySet):
    if clock_in_time:
        clock_in_time = int(clock_in_time)
        date_time = datetime.datetime.fromtimestamp(clock_in_time)
        try:
            # yyyy年MM月dd日 0:0:0
            now = date_to_time_stamp(year=date_time.year, month=date_time.month, day=date_time.day)
            # 第二天
            now2 = now + 24 * 3600
            return regular_clock.filter(clock_in_time__gte=now, clock_in_time__lte=now2), True
        except:
            return response_success_200(code=500, message="时间戳错误"), False
    return regular_clock, True
