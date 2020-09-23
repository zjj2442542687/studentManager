from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from user.views.user_insert import UserInsertView
from user.views.user_other import UserOtherView, Other, UserUpdateView
from user.views.user_search import UserPaginationSelectView
from user.views.user_select import UserSelectView, UserSelectViewCheck
from user.views.user_update_password import UserUpdatePassword

urlpatterns = [
    path("insert", UserInsertView.as_view({'post': 'create'})),

    # 用户名密码登录
    path("login", UserSelectView.as_view({'post': 'login'})),
    # 判断手机号是否存在
    path("checkPhoneNumber/<str:phone_number>", UserSelectView.as_view({'get': 'check_phone_number'})),
    # 检测手机号验证码是否正确
    path("check_phone_code", UserSelectView.as_view({'post': 'check_phone_code'})),
    # 检测手机号验证码是否正确
    path("check_password", UserSelectViewCheck.as_view({'post': 'check_password'})),
    # 手机号登录
    path("loginPhoneNumber", UserSelectView.as_view({'post': 'login_phone_number'})),
    # token登录
    path("loginToken", UserSelectView.as_view({'post': 'login_token'})),

    # 根据token修改用户信息
    path("update", UserOtherView.as_view({'patch': 'partial_update'})),

    # 根据手机号修改用户密码
    path("updatePasswordByPhone", UserUpdatePassword.as_view({'patch': 'update_password_by_phone'})),
    # 根据原密码修改用户密码
    path("updatePasswordByPassword", UserUpdatePassword.as_view({'patch': 'update_password_by_password'})),
    # 根据token删除用户信息
    path("delete", UserOtherView.as_view({'delete': 'destroy'})),
    # 根据token修改用户手机号码
    path("update_phone", UserUpdateView.as_view({'patch': 'Phone_update'})),

    path("sendCode", Other.as_view()),

    # 分页查询
    path("search", UserPaginationSelectView.as_view({'get': 'search'})),
]
