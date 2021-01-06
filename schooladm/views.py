from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from schooladm.models import Schooladm
from utils.my_info_judge import pd_super_adm_token
from utils.my_response import response_success_200


class SchoolAdmSerializer(ModelSerializer):
    class Meta:
        model = Schooladm
        fields = '__all__'
        depth = 2


class SchoolAdmView(RetrieveModelMixin, CreateModelMixin, GenericViewSet, ListModelMixin, DestroyModelMixin):
    queryset = Schooladm.objects.all()
    serializer_class = SchoolAdmSerializer
    parser_classes = [MultiPartParser]


class SchoolAdmSelectView(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = Schooladm.objects.all()
    serializer_class = SchoolAdmSerializer

    @swagger_auto_schema(
        operation_summary="根据学校查询学校管理员信息",
        operation_description="传学校ID",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('school_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='学校的id'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='超管TOKEN'),
        ]
    )
    def search_school(self, request):
        check_token = pd_super_adm_token(request)
        if check_token:
            return check_token

        school_id = request.GET.get("school_id")
        print(school_id)

        instance = self.queryset.filter(school=school_id)
        serializer = self.get_serializer(instance)
        return response_success_200(data=serializer.data)
