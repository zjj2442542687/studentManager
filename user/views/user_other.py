from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from user.models import User
from user.views.urls import send_code, judge_code
from user.views.user_insert import pd_phone_number
from user.views.user_serializers import UserInfoSerializersUpdate
from utils.my_encryption import my_encode, my_decode_token
from utils.my_info_judge import pd_token
from utils.my_response import *
from utils.my_swagger_auto_schema import request_body, string_schema
from utils.status import *
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser


class UserOtherView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据token修改用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('role', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='(-2, 学校管理员), (-1, 超级管理员), (0, 老师), (1, 学生), (2, 家长), (3, 辅导员)'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        phone_number = request.data.get("phone_number")

        # 判断token
        token = request.META.get("HTTP_TOKEN")
        check_token = pd_token(request, token)
        if check_token:
            return check_token

        # 获得pk
        pk = request.user
        print(pk)
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

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(message="修改成功!", data=resp.data)

    @swagger_auto_schema(
        operation_summary="根据token删除用户",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def destroy(self, request, *args, **kwargs):
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="token参数错误!!!!!")

        super().destroy(request, *args, **kwargs)
        return response_success_200(message="删除成功!!")

    def get_object(self):
        if self.action == "partial_update" or self.action == "destroy":
            pk = self.request.user
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, pk=pk)
        return super().get_object()


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
