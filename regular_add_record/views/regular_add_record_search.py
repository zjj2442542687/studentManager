from django.db.models import Q, QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from parent.models import Parent
from parent.views.parent_serializers import ParentSerializersSearch
from regular.models import Regular
from regular.views.regular_serializers import RegularSerializersSearch
from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordSerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token, pd_adm_token, pd_super_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400
from utils.my_utils import get_class_all_id, get_regular_all_id
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class RegularAddRecordPaginationSelectView(mixins.ListModelMixin,
                                           mixins.RetrieveModelMixin,
                                           GenericViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="习惯养成查询",
        operation_description="token为可选参数，如果不传递则只可以查看系统的regular",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('user', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='用户的id'),
            openapi.Parameter('regular', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='regular（习惯）'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='用户的token'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 查询user_id
        user_id = request.GET.get("user")
        regular_add_record, pd = search_user(request, user_id)
        if not pd:  # 有错误信息
            return regular_add_record

        # 查询regular_id
        regular_id = request.GET.get("regular")
        regular_add_record = search_regular(regular_id, regular_add_record)

        page = self.paginate_queryset(regular_add_record)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


# 查询user_id
def search_user(request, user_id):
    if not user_id and request.auth != -1:  # 如果没有传，而且不是超级管理员,默认为token中对应的user_id
        user_id = request.user
    elif user_id:  # 如果传了，强转成int类型(以为它得到的默认为string类型)
        user_id = int(user_id)
    else:  # 现在这种情况是超级管理员查询且它没有传值
        return RegularAddRecord.objects.all(), True

    if request.auth >= 0 and user_id != request.user:  # 用户id和token对应的id不一样
        return response_error_400(message="不能查询他人信息"), False

    return RegularAddRecord.objects.filter(user_id=user_id), True


# 根据regular_id查询信息，
def search_regular(regular_id, regular_add_record: QuerySet):
    if regular_id:
        return regular_add_record.filter(regular_id=regular_id)
    else:
        return regular_add_record
