from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular_category.models import RegularCategory
from regular_category.views.regular_category_serializers import RegularCategoryInfoSerializersAll
from utils.my_info_judge import pd_super_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema


class RegularCategoryInsertView(mixins.CreateModelMixin,
                                GenericViewSet):
    queryset = RegularCategory.objects.all()
    serializer_class = RegularCategoryInfoSerializersAll

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        request_body=request_body(properties={
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

        resp = super().create(request)
        return response_success_200(data=resp.data)
