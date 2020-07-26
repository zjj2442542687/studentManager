from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from school.views.school_insert import SchoolInsertView
from school.views.school_select import SchoolSelectView
from school.views.school_other import SchoolOtherView

urlpatterns = [
    path("insert", SchoolInsertView.as_view({'post': 'create'})),
    path("getAll", SchoolSelectView.as_view({'get': 'list'})),
    path("getSchoolById/<int:pk>", SchoolSelectView.as_view({'get': 'retrieve'})),
    path("getSchoolByName/<str:name>", SchoolSelectView.as_view({'get': 'retrieve_by_name'})),
    path("update/<int:pk>", SchoolOtherView.as_view({'patch': 'update'})),
    path("delete/<int:pk>", SchoolOtherView.as_view({'delete': 'destroy'})),
]
