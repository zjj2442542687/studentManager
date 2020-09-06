from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import get_object_or_404

from school.models import School
from student.models import Student
from student.views.student_serializers import StudentInfoSerializersUpdate, StudentInfoSerializersInsert, \
    StudentInfoSerializersAdmUpdate, StudentInfoSerializersSelect
from user.views.urls import del_user_and_user_details
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import STATUS_TOKEN_OVER, STATUS_PARAMETER_ERROR, STATUS_TOKEN_NO_AUTHORITY


class StudentOtherView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除学生信息及用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        role = request.auth
        if role >= 0:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")
        # 先删除用户
        check_del = del_user_and_user_details(1, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除学生
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
        deprecated=True
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_info_id=self.request.user)
        return super().get_object()


class StudentAdmView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersAdmUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="管理员修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            # openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
            #                   description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
            # ,
            # openapi.Parameter('id', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='学号')
        ],
        deprecated=True
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        resp = super().partial_update(request, *args, **kwargs)

        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        #
        # instance = self.get_object()
        # serializer = StudentInfoSerializersSelect(instance, context=self.get_serializer_context())
        # print(serializer.data)
        # return response_success_200(data=serializer.data)

        return response_success_200(data=resp.data)
