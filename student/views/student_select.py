from drf_yasg.utils import swagger_auto_schema, no_body

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.serializers import ModelSerializer

from student.models import Student
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class StudentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    获得所有学生信息

    无描述

    retrieve:
    根据id查询学生信息

    输入id

    retrieve_by_student_name:
    根据名字查询学生信息

    输入姓名

    """
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    def retrieve_by_student_name(self, request, *args, **kwargs):
        try:
            # instance = self.queryset.get(user_name=kwargs.get("student_name"))
            # 模糊查询
            # instance = self.queryset.get(name__contains=kwargs.get("name"))
            instance = self.queryset.get(user_name=kwargs.get("student_name"))
        except Student.DoesNotExist:
            return response_error_500(status=STATUS_NOT_FOUND_ERROR, message="没找到")
        except Student.MultipleObjectsReturned:
            return response_error_500(status=STATUS_MULTIPLE_ERROR, message="找到多个姓名相同用户")
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="通过用户的token获得学生信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def retrieve_by_token(self, request):
        token = request.META.get("HTTP_TOKEN")
        # token = request.data.get("token")
        print(token)
        print(request.user)
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!")

        instance = self.queryset.get(user_info=request.user)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
