from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from school.models import School
from school.views.school_insert import SchoolInfoSerializers
from utils.my_response import *


class SchoolSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers
