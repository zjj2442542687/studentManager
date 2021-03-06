# 分页查询
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from user.models import User
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from user.views.user_serializers import UserSerializersSearch
from utils.my_response import response_error_400, response_success_200
from utils.status import STATUS_PARAMETER_ERROR, STATUS_TOKEN_NO_AUTHORITY


class UserPaginationSelectView(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('role', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='(-2, 学校管理员)，(0, 老师), (1, 学生), (2, 家长), (3, 辅导员)', enum=[-2, 0, 1, 2, 3]),
            openapi.Parameter('user_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='用户名'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # role
        role = request.GET.get("role")
        check_role, user = search_role(role)
        if not check_role:
            return user

        # 名字
        name = request.GET.get("user_name")
        user = search_name(name, user)

        page = self.paginate_queryset(user)
        serializer = UserSerializersSearch(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


def search_role(role):
    if role:
        # if int(role) < 0 or int(role) > 3:
        if role not in '-20123':
            return False, response_success_200(code=STATUS_PARAMETER_ERROR, message="role的范围为(0`3)")
        user = User.objects.filter(role=role)
    else:
        # 返回 role >=  0 的
        user = User.objects.filter(role__gte=0)
    return True, user


def search_name(name, user):
    if name:
        return user.filter(user_name__contains=name)
    else:
        return user
