from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from classs.models import Class
from classs.views.class_select import ClassInfoSerializers2
from utils.my_info_judge import pd_token
from utils.my_response import response_error_400
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class ClassOtherView(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassInfoSerializers2

    @swagger_auto_schema(
        operation_summary="删除",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth >= 0:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")

        return super().destroy(request, *args, **kwargs)
