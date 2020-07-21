from rest_framework.pagination import LimitOffsetPagination


class MyLimitOffsetPagination(LimitOffsetPagination):
    # 默认显示的个数
    default_limit = 5
    offset_query_param = "index"
    offset_query_description = "开始的位置"
    limit_query_param = "size"
    limit_query_description = "获得的个数，默认5个，最多10个"
    # 一页最多显示的个数
    max_limit = 10
