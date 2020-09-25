from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_insert_info
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200
from utils.my_utils import get_regular_category_all_id, get_user_all_id, get_class_all_id
from utils.status import STATUS_TOKEN_NO_AUTHORITY


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
            openapi.Parameter('is_system', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='是不是系统(0不是，1是)',
                              enum=[0, 1], required=True),
            openapi.Parameter('regular_category', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='习惯类别的id',
                              enum=get_regular_category_all_id(), required=True),
            openapi.Parameter('clazz', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='class的id, 传表示它为该班级的regular',
                              enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        is_system = int(request.data.get("is_system"))
        if is_system == 1 and request.auth >= 0:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="没有权限添加系统类型的regular")

        title = request.data.get("title")
        regular_category_id = request.data.get("regular_category")
        class_id = request.data.get("clazz")

        # 检测插入数据的合法性
        check = check_insert_info(title, regular_category_id, request.user, class_id, request)
        if check:
            return check

        resp = super().create(request)
        return response_success_200(data=resp.data)
