from rest_framework.pagination import LimitOffsetPagination


class MyLimitOffsetPagination(LimitOffsetPagination):
    # 默认显示的个数
    default_limit = 5
    offset_query_param = "index"
    limit_query_param = "size"
    # 一页最多显示的个数
    max_limit = 10
