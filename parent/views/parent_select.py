from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from utils.my_response import *
from parent.views.parent_insert import ParentInfoSerializers

from student.models import Student


# class StudentInfoSerializersUserInfo(ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'user_info']
#         depth = 1
#
#
# class ParentInfoSerializers2(ModelSerializer):
#     student = serializers.SerializerMethodField(label='学生')
#
#     class Meta:
#         model = Parent
#         fields = "__all__"
#         depth = 1
#
#     def get_student(self, parent):
#         return StudentInfoSerializersUserInfo(Student.objects.filter(parent=parent), many=True).data

class ParentInfoSerializers2(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"
        depth = 1


class ParentSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    获得所有家长信息

    无描述

    retrieve:
    根据id查询家长信息

    。。
    """
    queryset = Parent.objects.all()
    serializer_class = ParentInfoSerializers2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return response_success_200(data=serializer.data)
    # def list(self, request, *args, **kwargs):
    #     resp = super().list(request, *args, **kwargs)
    #     return response_success_200(data=resp.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     print("开始")
    #     try:
    #         resp = super().retrieve(request, *args, **kwargs)
    #         return response_success_200(data=resp.data)
    #     except Exception as e:
    #         print(f'找到错误!!{e}')
    #         print(dir(e))
    #         return response_not_found_404(message="没找到!")
    #
    #     # print("结束")
    #     # print(response)
    #     # print(response.data)
    #     # if response.status_code == 200:
    #     #     return response_success_200(data=response.data)
