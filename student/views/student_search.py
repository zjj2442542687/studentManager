from drf_yasg import openapi
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from student.models import Student
from student.views.student_serializers import StudentSerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_info_judge import pd_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_success_200
from utils.my_utils import get_school_all_id, get_class_all_id
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class StudentPaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="学生信息查询",
        operation_description="默认查询所有",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('school_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学校id', enum=get_school_all_id()),
            openapi.Parameter('clazz_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id', enum=get_class_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # if request.auth >= 0:
        #     return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")

        # 名字
        name = request.GET.get("name")
        student = search_name(name)

        # 学校
        school_id = request.GET.get("school_id")
        student = search_school(school_id, student)

        # 班级
        clazz_id = request.GET.get("clazz_id")
        student = search_clazz(clazz_id, student)

        page = self.paginate_queryset(student)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_name(name):
    if name:
        user_details = UserDetails.objects.filter(name__contains=name)
        # 查询用户对应的用户详情id   以及role=1 的信息
        user = User.objects.filter(user_details_id__in=[x.pk for x in user_details]).filter(role=1)
        print(user)
        return Student.objects.filter(user_id__in=[x.pk for x in user])
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


class StudentPaginationView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="根据班级查询学生信息",
        pagination_class=None,
        operation_description="传入token和班级id",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN'),
            openapi.Parameter('clazz_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id', enum=get_class_all_id()),
        ]
    )
    def clazz_search(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth not in [-1, -2, 0, 3]:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")

        # 班级
        clazz_id = request.GET.get("clazz_id")
        student = Student.objects.filter(clazz=clazz_id)

        page = self.paginate_queryset(student)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)
