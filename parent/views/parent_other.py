from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from parent.views.parent_serializers import  ParentInfoSerializersUpdate
from utils.my_response import *
from rest_framework.parsers import MultiPartParser


class ParentOtherView(ModelViewSet):
    """
    destroy:
    根据id删除家长信息

    输入家长id删除
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        # print(Parent.objects.all())
        return response_success_200(message="删除成功!!")

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
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="token参数错误!!!!!")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_info_id=self.request.user)
        return super().get_object()
