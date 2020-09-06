from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from user_details.models import UserDetails
from user_details.views.user_details_serializers import UserDetailsInfoSerializersAll
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import *


class UserDetailsInsertView(mixins.CreateModelMixin,
                            GenericViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersAll

    @swagger_auto_schema(
        operation_summary="添加一条数据",
        required=[],
        request_body=request_body(properties={
            'user': integer_schema('用户id'),
        }),
        deprecated=True
    )
    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return response_success_200(data=resp.data)

