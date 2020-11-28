from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from examine.models import Examine
from examine.views.examine_serializers import ExamineInfoSerializersAll
from utils import status
from utils.my_info_judge import pd_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_response import response_error_400, response_success_200


class ExamineOtherView(ModelViewSet):
    queryset = Examine.objects.all()
    serializer_class = ExamineInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="老师审核作业",
        manual_parameters=[
            openapi.Parameter('grade', openapi.IN_FORM, type=openapi.TYPE_STRING, description='作业成绩'),
            openapi.Parameter('opinion', openapi.IN_FORM, type=openapi.TYPE_STRING, description='老师指导意见'),
            openapi.Parameter('state', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='是否批阅'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN',
                              required=True)
        ]
    )
    def examine_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) not in [0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.data)
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    @swagger_auto_schema(
        operation_summary="作业删除",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN',
                              required=True)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) not in [-2, -1, 0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
