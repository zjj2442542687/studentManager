from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from utils.my_info_judge import pd_adm_token, pd_super_adm_token
from utils.my_response import *
from rest_framework.parsers import MultiPartParser

from week.models import Week
from week.views.week_serializers import WeekInfoSerializersAll


class WeekOtherView(ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除week信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        # 删除
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('index', openapi.IN_FORM, type=openapi.TYPE_INTEGER,enum=[1, 2, 3, 4, 5, 6, 7],
                              description='(1, 周一), (2, 周二), (3, 周三), (4, 周四), (5, 周五), (6, 周六),(7, 周日)'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING,
                              description='描述'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        # 需要修改的
        pk = kwargs['pk']
        if not self.queryset.filter(pk=pk):
            return response_error_400(message="id未找到")
        # index
        index = request.data.get('index')
        if index:
            # 之前的index
            week = self.queryset.get(pk=pk)
            old_index = week.index
            if old_index != index and self.queryset.filter(index=index):
                return response_error_400(message="index已存在")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)
