from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from user_details.models import UserDetails
from user_details.views.user_details_serializers import UserDetailsInfoSerializersUpdate
from utils.my_response import *
from rest_framework.parsers import MultiPartParser


class UserDetailsOtherView(ModelViewSet):
    """
    partial_update:
    根据用户id修改用户详情信息

    无描述

    destroy:
    根据id删除用户详情信息

    输入用户详情id删除
    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        # 检测token
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_id=self.request.user)
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        # print(School.objects.all())
        return response_success_200(message="删除成功!!")
