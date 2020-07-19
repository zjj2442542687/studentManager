from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from utils.my_response import *
from parent.views.parent_insert import ParentInfoSerializers
from user.models import User


# class UserInfoSerializers3(ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class ParentOtherView(ModelViewSet):
    """
    destroy:
    根据id删除家长信息

    输入家长id删除
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers

    def destroy(self, request, *args, **kwargs):
        pk = request.data.get('pk')
        # if not User.objects.filter(id=pk):
        #     message = "找不到改家长ID信息"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        Parent.objects.filter(id=pk).delete()
        return response_success_200(message="删除成功!!")
