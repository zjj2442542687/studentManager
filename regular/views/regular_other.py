from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_update_info, check_pk_and_permission
from utils.my_info_judge import pd_super_adm_token, pd_token
from utils.my_response import response_success_200
from rest_framework.parsers import MultiPartParser

from utils.my_utils import get_regular_category_all_id, get_user_all_id, get_class_all_id


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
            return response_success_200(message="id未找到")

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
            openapi.Parameter('clazz', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='class的id, 传表示它为该班级的regular',
                              enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs['pk']

        # 检测用户对这个pk的访问权限
        check_permission = check_pk_and_permission(request, pk)
        if check_permission:
            return check_permission

        # 需要修改的检测
        regular_category_id = request.data.get("regular_category")
        class_id = request.data.get("clazz")
        check_info = check_update_info(regular_category_id, request.user, class_id)
        if check_info:
            return check_info

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)
