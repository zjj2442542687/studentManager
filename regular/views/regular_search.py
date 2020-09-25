from django.db.models import Q, QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from regular.models import Regular
from regular.views.regular_serializers import RegularSerializersSearch
from utils.my_info_judge import pd_token, pd_super_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_success_200
from utils.my_utils import get_class_all_id


class RegularPaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Regular.objects.all()
    serializer_class = RegularSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="习惯养成查询",
        operation_description="token为可选参数，如果不传递则只可以查看系统的regular",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('clazz', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级', enum=get_class_all_id()),
            openapi.Parameter('is_system', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='是不是系统的(不传,若token不为空则查看所有的,超级管理员才可用), (0,不是), (1,是), (2,系统的加上个人的))',
                              enum=[0, 1, 2]),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='TOKEN(不传，返回所有is_system为1的), (传了，根据is_system 返回)'),
        ]
    )
    def search(self, request, *args, **kwargs):
        # is_system
        is_system = request.GET.get("is_system")
        regular, pd = search_is_system(request, is_system)
        if not pd:  # 没成功，就是出错了
            return regular

        # class
        class_id = request.GET.get("clazz")
        regular = search_class(request, class_id, regular)

        page = self.paginate_queryset(regular)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_is_system(request, is_system):
    token = request.META.get("HTTP_TOKEN")
    if not token:  # 没有传token, 返回系统的
        return Regular.objects.filter(is_system=1), True
    if is_system is None:  # 没有传参

        # 判断token的是否为超级管理员
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token, False

        return Regular.objects.all(), True

    is_system = int(is_system)
    if is_system == 1:
        return Regular.objects.filter(is_system=1), True
    elif is_system == 0:  # 浏览自己添加的信息
        # 判断token的可用性
        check_token = pd_token(request)
        if check_token:
            return check_token, False
        # 返回该用户的所有非系统regular
        return Regular.objects.filter(user_id=request.user, is_system=0), True
    elif is_system == 2:
        # 判断token的可用性
        check_token = pd_token(request)
        if check_token:
            return check_token, False
        # 返回该用户的所有系统以及个人非系统的regular
        return Regular.objects.filter(Q(user_id=request.user, is_system=0) | Q(is_system=1)), True

    return response_success_200(message="参数错误"), False


# 查询班级的信息，
def search_class(request, class_id, regular: QuerySet):
    token = request.META.get("HTTP_TOKEN")
    if class_id and token:
        return regular.filter(clazz_id=class_id)
    else:
        return regular
