from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from parent.models import Parent
from parent.views.parent_serializers import ParentSerializersSearch
from school.models import School
from school.views.school_serializers import SchoolSerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from utils.my_response import response_error_400
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class SchoolPaginationSelectView(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 GenericViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="学校信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('school_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 名字
        school_name = request.GET.get("school_name")
        school = search_name(school_name)

        page = self.paginate_queryset(school)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_name(school_name):
    if school_name:
        return School.objects.filter(school_name=school_name)
    else:
        return School.objects.all()
