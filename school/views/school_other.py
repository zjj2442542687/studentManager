from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from school.models import School
from school.views.school_insert import SchoolInfoSerializers
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class SchoolOtherView(ModelViewSet):
    """
    destroy:
    根据id删除学校信息

    输入学校id删除

    update:
    根据id修改学校信息

    无描述
    """
    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        print(School.objects.all())
        return response_success_200(message="删除成功!!")
