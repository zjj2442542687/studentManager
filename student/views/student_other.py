from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from student.models import Student
from student.views.student_serializers import StudentInfoSerializersUpdate, StudentInfoSerializersAdmUpdate
from user.models import User
from user.views.urls import del_user_and_user_details
from user_details.models import UserDetails
from utils.my_info_judge import pd_token, pd_adm_token, pd_phone_number, pd_card, pd_qq, pd_email, \
    STATUS_PHONE_NUMBER_ERROR, STATUS_PHONE_NUMBER_DUPLICATE, STATUS_PARAMETER_ERROR
from utils.my_response import response_success_200
from utils.my_time import check_time_stamp
from utils.status import STATUS_TOKEN_NO_AUTHORITY


class StudentOtherView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="根据id删除学生信息及用户信息",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN')
        ],
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        role = request.auth
        if role >= 0:
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="没有权限")
        # 先删除用户
        check_del = del_user_and_user_details(1, kwargs.get("pk"))
        if check_del:
            return check_del
        # 删除学生
        # super().destroy(request, *args, **kwargs)
        return response_success_200(message="成功")

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
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

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_info_id=self.request.user)
        return super().get_object()


class StudentAdmView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersAdmUpdate

    @swagger_auto_schema(
        operation_summary="管理员修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update_adm(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        user_update = Student.objects.get(pk=kwargs['pk']).user
        phone_number = request.data.get("phone_number")
        if phone_number:
            if not pd_phone_number(phone_number):
                return response_success_200(code=STATUS_PHONE_NUMBER_ERROR, message="手机号输入有误")
            if User.objects.exclude(pk=user_update.id).filter(phone_number=phone_number):
                return response_success_200(code=STATUS_PHONE_NUMBER_DUPLICATE, message="手机号已存在")
            user_update.phone_number = phone_number

        # 获得传过来的参数
        user_details = request.data.get('user_details')
        print(user_details)
        # 获得需要修改的userDetails
        user_detail_update = user_update.user_details
        sex = user_details.get('sex')
        name = user_details.get('name')
        birthday = user_details.get('birthday')
        card = user_details.get('card')
        qq = user_details.get('qq')
        email = user_details.get('email')

        if sex:
            user_detail_update.sex = sex
        if name:
            user_detail_update.name = name
        if birthday:
            check_time = check_time_stamp(int(birthday))
            print(check_time)
            if check_time:
                return response_success_200(code=STATUS_PARAMETER_ERROR, message=check_time)
            user_detail_update.birthday = birthday
        if card:
            if not pd_card(card):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="身份证输入有误")
            if UserDetails.objects.exclude(pk=user_detail_update.id).filter(card=card):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="身份证已存在")
            user_detail_update.card = card
        if qq:
            if not pd_qq(qq):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="qq输入有误")
            if UserDetails.objects.exclude(pk=user_detail_update.id).filter(qq=qq):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="qq已存在")
            user_detail_update.qq = qq
        if email:
            if not pd_email(email):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="email输入有误")
            if UserDetails.objects.exclude(pk=user_detail_update.id).filter(email=email):
                return response_success_200(code=STATUS_PARAMETER_ERROR, message="email已存在")
            user_detail_update.email = email

        # 保存修改
        user_update.save()
        user_detail_update.save()

        resp = super().partial_update(request, *args, **kwargs)

        return response_success_200(data=resp.data)
