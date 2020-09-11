from drf_yasg.openapi import FORMAT_DATETIME, Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

# from regular_add_record.views.views import check_info, check_authority
from utils import status
from utils.my_info_judge import pd_token, pd_adm_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from utils.my_utils import get_class_all_id
from work.models import Work
from work.views.work_serializers import WorkInfoSerializersAll


class WorkOtherView(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="修改!!",
        manual_parameters=[
            openapi.Parameter('course', openapi.IN_FORM, type=openapi.TYPE_STRING, description='作业课程科目'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='作业标题'),
            openapi.Parameter('content', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业内容'),
            openapi.Parameter('release_Time', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业发布日期时间'),
            openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业开始日期时间'),
            openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业结束日期时间'),
            openapi.Parameter('request', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业要求'),
            openapi.Parameter('clazz', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='class的id',
                              enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN',
                              required=True)
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) is not 0 and 3:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.data)
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
