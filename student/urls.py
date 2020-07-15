from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from student.views import StudentInsertView
from student.views import StudentOtherView
from student.views import StudentSelectView
from user.views.user_insert import UserInsertView
from user.views.user_other import UserOtherView
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", StudentInsertView.as_view({'post': 'create'})),
    path("getAll", StudentSelectView.as_view({'get': 'list'})),
    path("getStudentById/<int:pk>", StudentSelectView.as_view({'get': 'retrieve'})),
    path("update/<int:pk>", StudentOtherView.as_view({'patch': 'update'})),
    # path("delete/<int:pk>", UserOtherView.as_view({'delete': 'destroy'})),
]
