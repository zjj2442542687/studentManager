from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from user_details.models import UserDetails
from user_details.views.my_limit_offset_pagination import MyLimitOffsetPagination
from user_details.views.user_details_insert import UserDetailsInfoSerializers
from utils.my_response import *


class UserDetailsInfoSerializers2(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"
        depth = 1


class UserDetailsSelectView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            GenericViewSet):
    """
    list:
    获得所有用户详情信息

    无描述

    retrieve:
    根据id查询用户信息

    输入id

    retrieve_by_user_id:
    根据用户id查询用户详情信息！

    传入用户名id

    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializers2
    pagination_class = MyLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def retrieve_by_user_id(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        print(user_id)
        if not user_id:
            return response_error_400(message="用户id不能为空")
        user_details = self.queryset.filter(user_id=user_id).values()
        print(user_details)
        return response_success_200(data="user_details")
