from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from user.models import User
from utils.my_response import *
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
        user_id = request.data.get('user_info')
        if not User.objects.filter(id=user_id):
            message = "用户ID不存在"
            return response_error_400(status=STATUS_CODE_ERROR, message=message)
        user_obj = User.objects.get(id=user_id)
        # print(user_obj)
        response = super().create(request, user_info=user_obj)
        return response_success_200(data=response.data)
