from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from utils.my_info_judge import pd_super_adm_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from week.models import Week
from week.views.week_serializers import WeekInfoSerializersAll


class WeekInsertView(mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekInfoSerializersAll

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        request_body=request_body(properties={
            'index': integer_schema('周的下标'),
            'title': string_schema('描述'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        # 添加用户信息
        index = request.data.get('index')
        # 用户index否存在
        if self.queryset.filter(index=index):
            return response_error_400(message="index 已存在")

        resp = super().create(request)
        return response_success_200(data=resp.data)
