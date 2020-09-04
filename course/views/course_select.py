from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions

from course.models import Course
from course.views.course_serializers import CourseALlSerializers
from utils.my_response import *


class CourseSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseALlSerializers
