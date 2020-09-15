from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from parent.models import Parent
from parent.views.parent_serializers import ParentSerializersSearch
from user.models import User
from user_details.models import UserDetails
from utils.my_info_judge import pd_adm_token
from utils.my_limit_offset_pagination import MyLimitOffsetPagination


class ParentPaginationSelectView(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 GenericViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializersSearch
    pagination_class = MyLimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="家长信息查询",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='名字'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def search(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        # 名字
        name = request.GET.get("name")
        parent = search_name(name)

        page = self.paginate_queryset(parent)
        serializer = self.serializer_class(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


def search_name(name):
    if name:
        user_details = UserDetails.objects.filter(name__contains=name)
        # 查询用户对应的用户详情id   以及role=2 的信息
        user = User.objects.filter(user_details_id__in=[x.pk for x in user_details]).filter(role=2)
        print(user)
        return Parent.objects.filter(user_id__in=[x.pk for x in user])
    else:
        return Parent.objects.all()
