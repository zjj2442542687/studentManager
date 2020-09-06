from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user_details.models import UserDetails
from user_details.views.user_details_serializers import UserDetailsInfoSerializersUpdate
from utils.my_info_judge import pd_token, pd_qq, pd_email
from utils.my_response import *
from rest_framework.parsers import MultiPartParser


class UserDetailsOtherView(ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据token修改用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        # 检测token
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 检测qq和邮箱的合法性
        qq = request.data.get("qq")
        email = request.data.get("email")
        if qq and not pd_qq(qq):
            return response_error_400(message="qq格式不正确")
        if email and not pd_email(email):
            return response_error_400(message="email格式不正确")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return User.objects.get(id=self.request.user).user_details
            # return get_object_or_404(self.queryset, id=self.request.user)
        return super().get_object()

    @swagger_auto_schema(
        operation_summary="根据id删除用户详情",
        required=[],
        deprecated=True
    )
    def destroy(self, request, *args, **kwargs):
        return response_success_200(message="过时!!")
        # super().destroy(request, *args, **kwargs)
        # # print(School.objects.all())
        # return response_success_200(message="删除成功!!")
