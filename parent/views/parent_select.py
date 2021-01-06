from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from parent.models import Parent
from parent.views.parent_serializers import *
from student.models import Student
from utils.my_info_judge import pd__token1, STATUS_404_NOT_FOUND
from utils.my_response import response_success_200, STATUS_TOKEN_OVER, STATUS_PARAMETER_ERROR


class ParentSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    获得所有家长信息

    无描述

    retrieve:
    根据id查询家长信息

    传家长ID
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializersSelect

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="通过用户的token获得家长信息",
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
            return response_success_200(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_success_200(staus=STATUS_PARAMETER_ERROR, message="参数错误!!!!!")

        instance = self.queryset.get(user_info=request.user)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)


class ParentSelect2View(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    获得所有家长信息

    无描述

    retrieve:
    根据id查询家长信息

    传家长ID
    """
    queryset = Parent.objects.all()
    serializer_class = StudentInfoSerializersUserInfo

    @swagger_auto_schema(
        operation_summary="根据班级查询家长信息",
        operation_description="传班级ID",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('class_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='班级的id'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN'),
        ]
    )
    def retrieve_by_Class(self, request):
        check_token = pd__token1(request)
        if check_token:
            return check_token

        clazz_id = request.GET.get("class_id")
        student = Student.objects.filter(clazz=clazz_id)
        print(student)
        parent = []
        for i in student:
            p = Parent.objects.filter(student=i.id)
            if p:
                for j in p:
                    parent.append(j.pk)
        print(parent)
        if not parent:
            return response_success_200(staus=STATUS_404_NOT_FOUND, message="没有查到该信息")
        instance = self.queryset.filter(pk__in=[x for x in parent]).all()
        # print(instance)
        serializer = self.get_serializer(instance, many=True)
        # print(serializer)
        return response_success_200(data=serializer.data)
