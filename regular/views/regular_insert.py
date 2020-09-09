from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_insert_info
from regular_category.models import RegularCategory
from utils.my_info_judge import pd_super_adm_token
from utils.my_response import response_success_200, response_error_400
from utils.my_utils import get_regular_category_all_id, get_user_all_id, get_class_all_id


class RegularInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    queryset = Regular.objects.all()
    serializer_class = RegularInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='标题'),
            openapi.Parameter('describe', openapi.IN_FORM, type=openapi.TYPE_STRING, description='描述'),
            openapi.Parameter('regular_category', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='习惯类别的id',
                              enum=get_regular_category_all_id()),
            openapi.Parameter('user', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='user的id',
                              enum=get_user_all_id()),
            openapi.Parameter('clazz', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='class的id, 传表示它为该班级的regular',
                              enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超级管理员的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        title = request.data.get("title")
        regular_category_id = request.data.get("regular_category")
        user_id = request.data.get("user")
        class_id = request.data.get("clazz")

        check = check_insert_info(title, regular_category_id, user_id, class_id)
        if check:
            return check

        resp = super().create(request)
        return response_success_200(data=resp.data)
