from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent


class ParentInfoSerializers(ModelSerializer):
    class Meta:
        model = Parent
        fields = ['user_info']


class ParentInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """

    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers

