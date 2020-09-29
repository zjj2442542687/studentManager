from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from classs.models import Class
from classs.views.class_select import ClassInfoSerializers2
from utils.my_info_judge import pd_token, pd_adm_token
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, integer_schema, array_schema
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class ClassOtherView(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassInfoSerializers2

    @swagger_auto_schema(
        operation_summary="删除",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth >= 0:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")

        # return super().destroy(request, *args, **kwargs)
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="删除成功!!")


class ClassDeleteAllView(ModelViewSet):
    queryset = Class.objects.all()

    @swagger_auto_schema(
        operation_summary="根据id列表批量删除班级信息及用户信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
        request_body=request_body(properties={
            'id_list': array_schema('班级ID列表', it=integer_schema())
        }),
    )
    def destroy_all(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token
        # print(request.data)
        list = request.data.get("id_list")
        message = ""
        print(list)
        for i in list:
            if not Class.objects.filter(pk=i):
                message += "班级i+未找到"
            else:
                Class.objects.filter(pk=i).delete()
        return response_success_200(message="批量删除删除结束," + message)
