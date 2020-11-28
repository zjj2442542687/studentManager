from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from parent.models import Parent
from parent.views.parent_serializers import ParentInfoSerializersUpdate, ParentInfoSerializersAdmUpdate
from user.views.urls import del_user_and_user_details
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, integer_schema, array_schema


class ParentOtherView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除家长信息及用户信息",
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
        check_del = del_user_and_user_details(2, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除家长
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
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


class ParentAdmView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersAdmUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="家长信息修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
        # deprecated=True
    )
    def partial_update(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)


class ParentDeleteAllView(ModelViewSet):
    queryset = Parent.objects.all()

    @swagger_auto_schema(
        operation_summary="根据id列表批量删除家长信息及用户信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
        request_body=request_body(properties={
            'id_list': array_schema('家长ID列表', it=integer_schema())
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
            check_del = del_user_and_user_details(2, int(i))
        if check_del:
            return check_del
        # 删除老师
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")
