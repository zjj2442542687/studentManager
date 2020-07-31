from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from user.models import User
from user.views.urls import send_code
from user.views.user_insert import pd_phone_number
from user.views.user_serializers import UserInfoSerializersUpdate
from utils.my_encryption import my_encode, my_decode_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import *


class UserOtherView(ModelViewSet):
    """
    destroy:
    根据id删除用户信息

    输入id删除

    partial_update_phone:
    判断手机号码是否已经注册

    传入手机号码
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersUpdate

    @swagger_auto_schema(
        operation_summary="根据id修改用户信息",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        pk = kwargs['pk']
        token = request.META.get("HTTP_TOKEN")

        # 检测token是否过期
        if request.user < 0:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token已过期！")
        # 如果传过来的token的用户是其它用户则显示没有权限
        print(my_decode_token(token)[0])
        if request.user != pk:
            return response_error_400(staus=STATUS_TOKEN_NO_AUTHORITY, message=f"没有权限操作该用户(id={pk})！")
        # 查看id是否存在
        if not User.objects.filter(pk=pk):
            return response_not_found_404(status=STATUS_NOT_FOUND_ERROR, message="id未找到")
        # 验证手机号是否正确
        if phone_number and not pd_phone_number(phone_number):
            return response_error_400(status=STATUS_PHONE_NUMBER_ERROR, message="手机号格式错误!!!!!!!")
        # 如果id一样且用户名不一样（因为前面已经判断了pk，所以pk是找得到的）
        if user_name and not User.objects.filter(pk=pk, user_name=user_name):
            # 如果这个名字已经被占用
            if User.objects.filter(user_name=user_name):
                return response_error_400(status=STATUS_USER_NAME_DUPLICATE, message="用户名已经存在")

        # 如果id一样且手机号不一样（因为前面已经判断了pk，所以pk是找得到的）
        if phone_number and not User.objects.filter(pk=pk, phone_number=phone_number):
            # 如果这个手机号已经被占用
            if User.objects.filter(phone_number=phone_number):
                return response_error_400(status=STATUS_PHONE_NUMBER_DUPLICATE, message="手机号已经被绑定")

        # 如果密码不为空就给密码加密
        if password:
            request.data['password'] = my_encode(password)
        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(message="修改成功!", data=resp.data)

    @swagger_auto_schema(
        request_body=request_body(properties={
            'user_name': string_schema('用户名'),
        })
    )
    def destroy(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        super().destroy(request, *args, **kwargs)
        return response_success_200(message="删除成功!!")


class Other(APIView):
    """
    post:
    发送验证码

    传入一个手机号
    """

    @swagger_auto_schema(
        request_body=request_body({
            "phone_number": string_schema("填入手机号")
        },
            required=['phone_number']
        )
    )
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        try:
            if not pd_phone_number(phone_number):
                raise UserWarning
            send_code(phone_number)
        except UserWarning:
            return response_error_400(status=STATUS_PHONE_NUMBER_ERROR, message='参数错误或手机号不合法')
        return response_success_200(message="发送验证码成功,验证码在10分钟内有效")
