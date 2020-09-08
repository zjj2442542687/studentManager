from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_update_info
from utils.my_info_judge import pd_super_adm_token
from utils.my_response import *
from rest_framework.parsers import MultiPartParser

from utils.my_utils import get_regular_category_all_id


class RegularOtherView(ModelViewSet):
    queryset = Regular.objects.all()
    serializer_class = RegularInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除category的信息",
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
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='标题'),
            openapi.Parameter('describe', openapi.IN_FORM, type=openapi.TYPE_STRING, description='描述'),
            openapi.Parameter('regular_category', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='习惯类别的id',
                              enum=get_regular_category_all_id()),
            openapi.Parameter('user', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='user的id'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        # 需要修改的检测
        pk = kwargs['pk']
        regular_category_id = request.data.get("regular_category")
        user_id = request.data.get("user")
        check_info = check_update_info(regular_category_id, user_id, pk)
        if check_info:
            return check_info

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)
