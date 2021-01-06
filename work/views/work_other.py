from django.http import FileResponse
from django.utils.http import urlquote
from drf_yasg.openapi import FORMAT_DATETIME, Response
from rest_framework import mixins
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

# from regular_add_record.views.views import check_info, check_authority
from utils import status
from utils.my_info_judge import pd_token, pd_adm_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY, STATUS_PARAMETER_ERROR
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema
from utils.my_utils import get_class_all_id
from work.models import Work
from work.views.work_serializers import WorkInfoSerializersAll


class WorkOtherView(ModelViewSet, DestroyModelMixin):
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
        if lookup_token(request) not in [0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        print(request.data)
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.STATUS_200_SUCCESS)


class WorkInfoDownloadView(mixins.CreateModelMixin,
                           GenericViewSet):
    """
    download:
    作业文件下载

    无描述
    """
    queryset = Work.objects.all()

    # serializer_class = FileInfoSerializer

    def download(self, request, *args, **kwargs):
        if not Work.objects.filter(id=kwargs.get('pk')):
            return response_success_200(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!改作业ID不存在")
        work = Work.objects.get(id=kwargs.get('pk'))
        if not work.file:
            return response_success_200(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!改作业没有附件")
        # print(work)
        file_name = "" + work.clazz.class_name + "班" + work.course + "作业"
        # print('下载的文件名：' + file_name)
        print(work.file)
        str = '' + work.file.path
        str = str.split(".")[1]
        print(str)
        file = open(work.file.path, 'rb')
        resp = FileResponse(file)
        # response['Content-Type'] = 'application/vnd.ms-excel'
        resp['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(file_name + "."+str)
        return resp
