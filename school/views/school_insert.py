from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import *


class SchoolInfoSerializers(ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class SchoolInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        resp = super().create(request)
        return response_success_200(data=resp.data)
