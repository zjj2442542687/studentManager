from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from regular_category.models import RegularCategory
from regular_category.views.regular_category_serializers import RegularCategorySerializersSearch
from utils.my_info_judge import pd_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination


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
