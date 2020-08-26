from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination


# class MyLimitOffsetPagination(LimitOffsetPagination):
#     # 默认显示的个数
#     default_limit = 5
#     offset_query_param = "index"
#     offset_query_description = "开始的位置"
#     limit_query_param = "size"
#     limit_query_description = "获得的个数，默认5个，最多100个"
#     # 一页最多显示的个数
#     max_limit = 100


class MyLimitOffsetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    page_size_query_description = "lnt说的那种(多少个)"
    page_query_param = "index"
    page_query_description = "lnt说的那种(第几页)"
