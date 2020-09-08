from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from regular_category.models import RegularCategory
from regular_category.views.regular_category_serializers import RegularCategoryInfoSerializersAll
from utils.my_info_judge import pd_super_adm_token
from utils.my_response import *
from rest_framework.parsers import MultiPartParser


class RegularCategoryOtherView(ModelViewSet):
    queryset = RegularCategory.objects.all()
    serializer_class = RegularCategoryInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除categoryCategory信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token
        # 需要修改的
        pk = kwargs['pk']
        if not self.queryset.filter(pk=pk):
            return response_error_400(message="id未找到")

        # 删除
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
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
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)
