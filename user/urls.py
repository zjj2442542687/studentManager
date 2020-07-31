from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from user.views.user_insert import UserInsertView
from user.views.user_other import UserOtherView, Other
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", UserInsertView.as_view({'post': 'create'})),

    path("getAll", UserSelectView.as_view({'get': 'list'})),
    # 根据id获得用户信息
    # path("getUserById/<int:pk>", UserSelectView.as_view({'get': 'retrieve'})),
    # 根据用户名获得用户信息
    # path("getUserByUserName/<str:user_name>", UserSelectView.as_view({'get': 'retrieve_by_username'})),
    # 根据手机号获得用户信息
    # path("getUserByPhoneNumber/<str:phone_number>", UserSelectView.as_view({'get': 'retrieve_by_phone_number'})),
    # 用户名密码登录
    path("login", UserSelectView.as_view({'post': 'login'})),
    # 判断手机号是否存在
    path("checkPhoneNumber/<str:phone_number>", UserSelectView.as_view({'get': 'check_phone_number'})),
    # 手机号登录
    path("loginPhoneNumber", UserSelectView.as_view({'post': 'login_phone_number'})),
    # token登录
    path("loginToken", UserSelectView.as_view({'post': 'login_token'})),

    # 根据id修改用户信息
    path("update/<int:pk>", UserOtherView.as_view({'patch': 'partial_update'})),
    # 根据id删除用户信息
    path("delete/<int:pk>", UserOtherView.as_view({'delete': 'destroy'})),

    path("sendCode", Other.as_view()),
]
