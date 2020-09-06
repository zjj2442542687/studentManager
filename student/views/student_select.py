from drf_yasg.utils import swagger_auto_schema, no_body

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.serializers import ModelSerializer

from student.models import Student
from student.views.student_serializers import StudentSerializersSearch
from utils.my_info_judge import pd_token
from utils.my_response import *
from utils.my_swagger_auto_schema import *


class StudentSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializersSearch

    @swagger_auto_schema(
        operation_summary="通过用户的token获得学生信息",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def retrieve_by_token(self, request):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth != 1:
            return response_error_400(message="没有权限")

        instance = self.queryset.get(user_id=request.user)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
