from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import serializers, mixins, status, exceptions
from rest_framework.serializers import ModelSerializer

from user.models import User
from rest_framework.response import Response

from user.views.user_insert import UserInfoSerializers


class UserSelectView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    """
    list:
    获得所有用户信息

    无描述

    retrieve:
    根据id查询用户信息

    输入id

    retrieve_by_username:
    根据用户名查询用户信息！

    传入用户名查询用户信息

    retrieve_by_phone_number:
    根据手机号查询用户信息！

    传入手机号查询用户信息

    login:
    登录验证

    用户名或手机号加密码登录，同时优先用户名

    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializers

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        # Expected type 'str', got 'Dict[str, Union[int, Any]]' instead
        return Response({"code": 200, "data": serializer.data})

    def retrieve_by_username(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(user_name=kwargs.get("user_name"))
        except User.DoesNotExist:
            return Response({"message": "没找到"})
        except User.MultipleObjectsReturned:
            return Response({"message": "返回多个"})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve_by_phone_number(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(phone_number=kwargs.get("phone_number"))
        except User.DoesNotExist:
            return Response({"message": "没找到"})
        except User.MultipleObjectsReturned:
            return Response({"message": "返回多个"})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["password"],
            properties={
                'user_name': openapi.Schema(type=openapi.TYPE_STRING, description="这是用户名"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        manual_parameters=[
            openapi.Parameter('user_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='用户名')
        ]
    )
    def login(self, request):
        username = request.data.get("user_name")
        password = request.data.get("password")
        phone_number = request.data.get("phone_number")

        print(f"用户名:{username},password:{password},phone_number:{phone_number}")
        try:
            if not password or not username and not phone_number:
                raise UserWarning
                # return Response({"message": "有空参数"})
            if username:
                instance = self.queryset.get(password=password, user_name=username)
            elif phone_number:
                instance = self.queryset.get(password=password, phone_number=phone_number)
            else:
                instance = None
        except User.DoesNotExist:
            return Response({"code": 400, "message": "用户名或密码错误"})
        except UserWarning:
            raise exceptions.ParseError('参数错误!!!!!!')
        serializer = self.get_serializer(instance)
        print(f'数据是：{serializer.data}')
        return Response({"code": 200, "data": serializer.data})
