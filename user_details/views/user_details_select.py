from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from user.models import User
from user_details.models import UserDetails
from user_details.views.my_limit_offset_pagination import MyLimitOffsetPagination
from user_details.views.user_details_serializers import UserDetailsInfoSerializersAll
from utils.my_response import *


# 分页查询
class UserDetailsPaginationSelectView(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      GenericViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersAll
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="获得所有用户详情信息",
    )
    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return response_success_200(data=resp.data)


class UserDetailsSelectView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            GenericViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersAll

    @swagger_auto_schema(
        operation_summary="根据用户token获得用户详情",
        operation_description="传入token",
        pagination_class=None,
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def retrieve_by_token(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        print(f'token={token}')
        # token = request.data.get("token")
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!")

        # 根据用户id查询用户详情
        instance = self.queryset.get(user_id=request.user)

        if not instance:
            return response_error_400(message="获得用户信息失败")
        user_details = self.get_serializer(instance).data
        print(user_details)
        return response_success_200(data=user_details)
