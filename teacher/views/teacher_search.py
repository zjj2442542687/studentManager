from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from classs.models import Class
from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherSerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_utils import get_school_all_id, get_class_all_id


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
                              description='学校id', enum=get_school_all_id()),
            openapi.Parameter('clazz', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级id', enum=get_class_all_id()),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='昵称'),
            openapi.Parameter('role', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='角色', enum=[0, 3]),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 名字
        name = request.GET.get("name")
        teacher = search_name(name)

        # 学校
        school = request.GET.get("school")
        teacher = search_school(school, teacher)

        # 班级
        clazz = request.GET.get("clazz")
        clazz_result = search_clazz(clazz)
        # 因为查询的结果可能为空集合，所以用这个（为空集合也赋值）
        if clazz_result is not None:
            teacher = clazz_result

        # 昵称
        title = request.GET.get("title")
        teacher = search_title(title, teacher)

        # 身份
        role = request.GET.get("role")
        teacher = search_role(role, teacher)

        print(teacher)

        page = self.paginate_queryset(teacher)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        print(serializer.data)
        return self.get_paginated_response(serializer.data)


def search_name(name):
    if name:
        user_details = UserDetails.objects.filter(name__contains=name)
        print(user_details)
        # 查询用户对应的用户详情id   以及role=0或role=3 的信息
        user = User.objects.filter(user_details_id__in=[x.pk for x in user_details]).filter(Q(role=0) | Q(role=3))
        print(user)
        return Teacher.objects.filter(user_id__in=[x.pk for x in user])
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


def search_role(role, teacher):
    if not teacher:
        return teacher
    if role:
        return teacher.filter(user__role=role)
    else:
        return teacher
