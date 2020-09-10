from drf_yasg.openapi import FORMAT_DATETIME
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from regular_add_record.views.views import check_info, check_authority
from utils.my_info_judge import pd_token, pd_adm_token, lookup_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from work.models import Work
from work.views.work_serializers import WorkInfoSerializersAll


class WorkOtherView(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="修改!!",
        # request_body=request_body(properties={
        #     'teacher': integer_schema('老师id'),
        #     'clazz': integer_schema('班级id'),
        #     'course': string_schema('作业课程科目'),
        #     'title': string_schema('作业标题'),
        #     'content': string_schema('作业内容'),
        #     'request': string_schema('作业要求'),
        #     'start_date': string_schema('作业开始日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
        #     'end_date': string_schema('作业结束日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
        #     'release_Time': string_schema('作业发布日期时间', default="2020-09-08 12:00", f=FORMAT_DATETIME),
        # }),
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='文件 '),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检查权限
        check = check_authority(self, request, kwargs)
        if check:
            return check

        resp = super().partial_update(request, *args, **kwargs)

        return response_success_200(data=resp.data)
