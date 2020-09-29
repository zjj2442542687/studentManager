from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from teacher.models import Teacher
from teacher.views.teacher_serializers import TeacherInfoSerializersUpdate, TeacherInfoSerializersAdmUpdate
from user.views.urls import del_user_and_user_details
from user_details.views.urls import adm_update_user_details
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, array_schema, integer_schema


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
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        # 先删除用户
        check_del = del_user_and_user_details(0, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除老师
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="根据id列表批量删除老师信息及用户信息",
        operation_description="说明：无",
        # request_body=request_body(properties={
        #     'list_id': array_schema('老师ID列表')
        # }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
            openapi.Parameter('list_id', openapi.IN_QUERY, type=openapi.TYPE_ARRAY, description='老师ID列表',
                              items=openapi.Schema(type=openapi.TYPE_INTEGER))
        ]
    )
    def destroy_all(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        list = request.query_params.get('list_id')
        print(list)
        # 先删除用户
        for i in list:
            check_del = del_user_and_user_details(0, int(i))
        if check_del:
            return check_del
        # 删除老师
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        print(request.data)
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_id=self.request.user)
        return super().get_object()


class TeacherAmdView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherInfoSerializersAdmUpdate

    # parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="管理员修改",
        required=[],
        manual_parameters=[
            # openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
            #                   description='性别((-1, 女), (0, 保密), (1, 男))'),
            # openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
            #                   description='身份'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update_adm(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        user_update = Teacher.objects.get(pk=kwargs['pk']).user
        check_update = adm_update_user_details(user_update)
        if check_update:
            return check_update

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)


class TeacherDeleteAllView(ModelViewSet):
    queryset = Teacher.objects.all()

    @swagger_auto_schema(
        operation_summary="根据id列表批量删除老师信息及用户信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
        request_body=request_body(properties={
            'id_list': array_schema('老师ID列表', it=integer_schema())
        }),
    )
    def destroy_all2(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        # print(request.data)
        list = request.data.get("id_list")
        print(list)
        # # 先删除用户
        for i in list:
            check_del = del_user_and_user_details(0, int(i))
        if check_del:
            return check_del
        # 删除老师
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")
