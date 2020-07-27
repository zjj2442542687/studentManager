from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from course.models import Course
from school.views.school_insert import SchoolInfoSerializers
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class CourseOtherView(ModelViewSet):
    """
    destroy:
    根据id删除课程信息

    输入课程id删除

    """
    queryset = Course.objects.all()
    serializer_course = SchoolInfoSerializers

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        # print(Course.objects.all())
        return response_success_200(message="删除成功!!")
