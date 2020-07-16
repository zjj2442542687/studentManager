from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from rest_framework.response import Response

from utils.my_response import *


class ParentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"
        depth = 1


class ParentSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    获得所有家长信息

    无描述

    retrieve:
    根据id查询家长信息

    。。
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers2

    # def list(self, request, *args, **kwargs):
    #     resp = super().list(request, *args, **kwargs)
    #     return response_success_200(data=resp.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     print("开始")
    #     try:
    #         resp = super().retrieve(request, *args, **kwargs)
    #         return response_success_200(data=resp.data)
    #     except Exception as e:
    #         print(f'找到错误!!{e}')
    #         print(dir(e))
    #         return response_not_found_404(message="没找到!")
    #
    #     # print("结束")
    #     # print(response)
    #     # print(response.data)
    #     # if response.status_code == 200:
    #     #     return response_success_200(data=response.data)
