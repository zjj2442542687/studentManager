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
from regular_category.models import RegularCategory
from regular_category.views.regular_category_serializers import RegularCategorySerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token, pd_adm_token, pd_super_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400
from utils.my_utils import get_class_all_id, get_regular_all_id
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class RegularCategoryPaginationSelectView(mixins.ListModelMixin,
                                          mixins.RetrieveModelMixin,
                                          GenericViewSet):
    queryset = RegularCategory.objects.all()
    serializer_class = RegularCategorySerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="习惯养成类别的查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='title'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='用户的token'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 查询user_id
        title = request.GET.get("title")
        regular_category = search_title(title)

        page = self.paginate_queryset(regular_category)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


# 查询title
def search_title(title):
    if title:
        return RegularCategory.objects.filter(title__contains=title)
    return RegularCategory.objects.all()
