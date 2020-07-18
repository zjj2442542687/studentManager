from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, string_schema


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

    @swagger_auto_schema(
        request_body=request_body(properties={
            'user_info': string_schema('用户ID')
        })
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success_200(data=response.data)
