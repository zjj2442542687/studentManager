from drf_yasg import openapi
from drf_yasg.openapi import FORMAT_DATETIME
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from utils.my_info_judge import pd_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
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
        # request_body=request_body(properties={
        #     'teacher': integer_schema('老师id'),
        #     'clazz': integer_schema('班级id'),
        #     'course': string_schema('作业课程科目'),
        #     'title': string_schema('作业标题'),
        #     'content': string_schema('作业内容'),
        #     'request': string_schema('作业要求'),
        #     'start_date': string_schema('作业开始日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
        #     'end_date': string_schema('作业结束日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
        #     'release_Time': string_schema('作业发布日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME)
        # }),
        manual_parameters=[
            # openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
            #                   description='文件 '),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) is not 3:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.data)
        resp = super().create(request)
        return response_success_200(data=resp.data)
