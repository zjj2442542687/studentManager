from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from classs.models import Class
from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherSerializersSearch
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class TeacherPaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="老师信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('school', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学校id'),
            openapi.Parameter('clazz_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id'),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='昵称'),
            openapi.Parameter('identity', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
        if check_token:
            return check_token

        role = int(my_decode_token(token)[1])
        if role >= 0:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")

        # 名字
        name = request.GET.get("name")
        teacher = search_name(name)

        # 学校
        school_id = request.GET.get("school_id")
        teacher = search_school(school_id, teacher)

        # 班级
        clazz_id = request.GET.get("clazz_id")
        clazz_result = search_clazz(clazz_id)
        # 因为查询的结果可能为空集合，所以用这个（为空集合也赋值）
        if clazz_result is not None:
            teacher = clazz_result

        # 昵称
        title = request.GET.get("title")
        teacher = search_title(title, teacher)

        # 身份
        identity = request.GET.get("identity")
        teacher = search_identity(identity, teacher)

        print(teacher)

        page = self.paginate_queryset(teacher)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())

        return self.get_paginated_response(serializer.data)


def search_name(name):
    if name:
        return Teacher.objects.filter(name__contains=name)
    else:
        return Teacher.objects.all()


def search_school(school_id, teacher):
    if not teacher:
        return teacher
    if school_id:
        return teacher.filter(school_id=school_id)
    else:
        return teacher


def search_clazz(clazz_id):
    if clazz_id:
        try:
            teacher = Class.objects.get(id=clazz_id).teacher_info
            if not teacher:
                return Teacher.objects.none()
            return Teacher.objects.filter(pk=teacher.pk)
        except Class.DoesNotExist:
            print("没找到")
            return Teacher.objects.none()
    else:
        return None


def search_title(title, teacher):
    if not teacher:
        return teacher
    if title:
        return teacher.filter(title__contains=title)
    else:
        return teacher


def search_identity(identity, teacher):
    if not teacher:
        return teacher
    if identity:
        return teacher.filter(identity__contains=identity)
    else:
        return teacher
