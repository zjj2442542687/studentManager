from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from parent.views.parent_serializers import ParentInfoSerializersUpdate
from user.views.urls import del_user
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token
from utils.my_response import *
from rest_framework.parsers import MultiPartParser


class ParentOtherView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除家长信息及用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
        if check_token:
            return check_token
        role = int(my_decode_token(token)[1])
        if role >= 0:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")
        # 先删除用户
        check_del = del_user(2, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除家长
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
        if check_token:
            return check_token

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_info_id=self.request.user)
        return super().get_object()
