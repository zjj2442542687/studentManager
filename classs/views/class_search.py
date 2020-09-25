from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from classs.models import Class
from classs.views.class_serializers import ClassSerializersSearch
from utils.my_info_judge import pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_utils import get_school_all_id


class ClassPaginationSelectView(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                GenericViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="班级信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('class_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('school_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学校的id', enum=get_school_all_id()),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 名字
        class_name = request.GET.get("class_name")
        clazz = search_name(class_name)

        # 学校
        school_id = request.GET.get("school_id")
        clazz = search_school(school_id, clazz)

        page = self.paginate_queryset(clazz)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_name(class_name):
    if class_name:
        return Class.objects.filter(class_name__contains=class_name)
    else:
        return Class.objects.all()


def search_school(school_id, clazz):
    if school_id:
        return clazz.filter(school_id=school_id)
    else:
        return clazz
