from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from student.views import StudentInsertView, StudentOtherView, StudentSelectView


urlpatterns = [
    path("insert", StudentInsertView.as_view({'post': 'create'})),
    path("getAll", StudentSelectView.as_view({'get': 'list'})),
    path("getStudentById/<int:pk>", StudentSelectView.as_view({'get': 'retrieve'})),
    path("getStudentByName/<str:student_name>", StudentInsertView.as_view({'get': 'retrieve_by_studentname'})),
    path("update/<int:pk>", StudentOtherView.as_view({'patch': 'update'})),
    path("delete/<int:pk>", StudentOtherView.as_view({'delete': 'destroy'})),
]
