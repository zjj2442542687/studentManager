from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from user_details.models import UserDetails
from user_details.views.user_details_insert import UserDetailsInfoSerializers
from user_details.views.user_details_select import UserDetailsInfoSerializers2
from utils.my_response import *
from rest_framework.parsers import MultiPartParser

from utils.my_swagger_auto_schema import request_body, string_schema


class UserDetailsInfoSerializersUpdate(ModelSerializer):
    nickname = serializers.CharField(label='昵称', required=False)
    avatar = serializers.ImageField(label='头像', required=False)
    sex = serializers.IntegerField(label='性别', required=False)
    birthday = serializers.DateTimeField(label='生日', required=False)
    personal_signature = serializers.CharField(label='个性签名', required=False)

    class Meta:
        model = UserDetails
        fields = ["nickname", "avatar", "sex", "birthday", "personal_signature"]
        depth = 1


class UserDetailsOtherView(ModelViewSet):
    """
    partial_update:
    根据用户id修改用户详情信息

    无描述
    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            user_id = self.kwargs.get("user_id")
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_id=user_id)
        return super().get_object()
