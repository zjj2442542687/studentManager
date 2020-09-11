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
