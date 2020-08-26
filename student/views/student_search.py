from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from student.models import Student
from student.views.student_serializers import StudentSerializersSearch
from user.models import User
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from user.views.user_serializers import UserSerializersSearch
from utils.my_response import response_error_400
from utils.status import STATUS_PARAMETER_ERROR, STATUS_TOKEN_NO_AUTHORITY


class StudentPaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="学生信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('school', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学校id'),
            openapi.Parameter('clazz_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id'),
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
        student = search_name(name)

        # 学校
        school_id = request.GET.get("school_id")
        student = search_clazz(school_id, student)

        # 班级
        clazz_id = request.GET.get("clazz_id")
        student = search_clazz(clazz_id, student)

        page = self.paginate_queryset(student)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_name(name):
    if name:
        return Student.objects.filter(name__contains=name)
    else:
        return Student.objects.all()


def search_school(school_id, student):
    if school_id:
        return student.filter(school_id=school_id)
    else:
        return student


def search_clazz(clazz_id, student):
    if clazz_id:
        return student.filter(clazz_id=clazz_id)
    else:
        return student