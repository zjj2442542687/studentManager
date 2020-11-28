from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from examine.models import Examine
from examine.views.examine_serializers import ExamineInfoSerializersAll
from utils.my_info_judge import pd_adm_token, STATUS_TOKEN_NO_AUTHORITY, lookup_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400
from utils.my_utils import get_work_all_id, get_student_all_id


class ExaminePaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Examine.objects.all()
    serializer_class = ExamineInfoSerializersAll
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="查询所有审核信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN',
                              required=True)
        ]
    )
    def list(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        if lookup_token(request) not in [-2, -1, 0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="查询审核情况(根据学生ID或作业ID)",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('student', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学生id', enum=get_student_all_id()),
            openapi.Parameter('work', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='作业id', enum=get_work_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        if lookup_token(request) not in [-2, -1, 0, 3]:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

        # 作业
        work = request.GET.get("work")
        # examine = Examine.objects.filter(work=work)

        # 学生
        student = request.GET.get("student")
        if work is None and student is None:
            examine = Examine.objects.all()
        elif work is None:
            examine = Examine.objects.filter(student=student)
        elif student is None:
            examine = Examine.objects.filter(work=work)
        else:
            examine = Examine.objects.filter(student=student, work=work)

        print(examine)
        page = self.paginate_queryset(examine)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="老师查询自己发布作业审核状态",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('work', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='作业id', enum=get_work_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN'),
        ]
    )
    def search_teacher(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        work = request.GET.get("work")
        examine = Examine.objects.filter(work=work)

        print(examine)
        page = self.paginate_queryset(examine)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())

        return self.get_paginated_response(serializer.data)
