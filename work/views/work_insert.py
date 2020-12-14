from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from utils.my_info_judge import pd_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_response import response_success_200, response_error_400
from utils.my_utils import get_class_all_id, get_teacher_all_id
from work.models import Work
from work.views.work_serializers import WorkInfoSerializersAll


class WorkInsertView(mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="教师发布作业",
        operation_description="说明：教师和班级必须存在，可以上传文件",
        manual_parameters=[
            openapi.Parameter('course', openapi.IN_FORM, type=openapi.TYPE_STRING, description='作业课程科目', required=True),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='作业标题', required=True),
            openapi.Parameter('content', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业内容', required=True),
            openapi.Parameter('release_Time', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业发布日期时间',
                              required=True),
            openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业开始日期时间',
                              required=True),
            openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业结束日期时间',
                              required=True),
            openapi.Parameter('request', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业要求'),
            openapi.Parameter('teacher', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='teacher的id',
                              enum=get_teacher_all_id(), required=True),
            openapi.Parameter('clazz', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='class的id',
                              enum=get_class_all_id(), required=True),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) not in [0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.data)
        resp = super().create(request)
        return response_success_200(data=resp.data)
