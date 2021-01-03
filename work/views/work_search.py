from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from classs.models import Class
from teacher.models import Teacher
from utils.my_info_judge import pd_adm_token, STATUS_TOKEN_NO_AUTHORITY, pd_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400, response_success_200
from utils.my_utils import get_class_all_id
from work.models import Work
from work.views.work_serializers import WorkSerializersSearch


class WorkPaginationSelectView(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializersSearch
    pagination_class = MyLimitOffsetPagination

    """
        List a queryset.
        """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="管理员查询作业信息",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('clazz', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id', enum=get_class_all_id()),
            openapi.Parameter('teacher', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='老师id', enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search_adm(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 班级
        clazz = request.GET.get("clazz")
        work = Work.objects.filter(clazz=clazz)

        # 老师
        teacher = request.GET.get("teacher")
        if work is None:
            work = Work.objects.filter(teacher=teacher)
        elif teacher is not None:
            work = work.filter(teacher=teacher)

        print(work)
        page = self.paginate_queryset(work)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="老师查询自己发布作业信息",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='老师TOKEN'),
        ]
    )
    def search_teacher(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth not in [0, 3]:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够，该token不是学生")
        # 老师
        teacher = Teacher.objects.get(user=request.user).id
        work = Work.objects.filter(teacher=teacher)

        print(work)
        page = self.paginate_queryset(work)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="辅导员查询自己班级作业信息",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='辅导员TOKEN'),
        ]
    )
    def search_clazz(self, request, *args, **kwargs):
        # teacher_pk = Class.objects.get(pk=request.GET.get('clazz')).headmaster.pk
        # if request.user is not teacher_pk:
        #     print(request.user)
        #     print(teacher_pk)
        #     return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="这不是您所带班级")
        # # 班级
        # clazz = request.GET.get("clazz")
        # work = Work.objects.filter(clazz=clazz)
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth not in [3]:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="权限不够，该token不是辅导员")
        clazz = Class.objects.get(headmaster=request.user)
        work = Work.objects.filter(clazz=clazz)

        print(work)
        page = self.paginate_queryset(work)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)
