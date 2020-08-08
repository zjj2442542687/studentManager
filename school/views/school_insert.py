from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class SchoolInfoSerializers(ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class SchoolInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """

    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers

    # @swagger_auto_schema(
    #     request_body=request_body(properties={
    #         # 'school_name': string_schema('学校名'),
    #         # 'school_info':string_schema('学校名'),
    #         # 'school_date':('学校名'),
    #     })
    # )
    def create(self, request, *args, **kwargs):
        response = super().create(request)
        return response_success_200(data=response.data)
