from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from parent.views.parent_insert import ParentInfoSerializers
from user.models import User
from rest_framework.response import Response


# class UserInfoSerializers3(ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class ParentOtherView(ModelViewSet):
    """
    update:修改家长表信息

    无描述
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers
