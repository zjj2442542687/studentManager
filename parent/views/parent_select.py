from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from rest_framework.response import Response


class ParentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"
        depth = 1


class ParentSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    获得所有家长信息

    无描述
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers2

