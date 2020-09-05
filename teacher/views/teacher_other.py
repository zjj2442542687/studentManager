from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherInfoSerializersAll, TeacherInfoSerializersUpdate, \
    TeacherInfoSerializersAdmUpdate
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser

from user.views.urls import del_user
from utils.my_encryption import my_decode_token
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200, response_error_400
from utils.status import STATUS_TOKEN_OVER, STATUS_PARAMETER_ERROR, STATUS_TOKEN_NO_AUTHORITY


class TeacherOtherView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除老师信息及用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
        if check_token:
            return check_token
        role = int(my_decode_token(token)[1])
        if role >= 0:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")
        # 先删除用户
        check_del = del_user(0, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除老师
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
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


class TeacherAmdView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersAdmUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="管理员修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update_adm(self, request, *args, **kwargs):
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)
