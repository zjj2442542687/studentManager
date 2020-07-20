from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from classs.views.class_insert import ClassInfoSerializers, ClassInsertView


urlpatterns = [
    path("insert", ClassInsertView.as_view({'post': 'create'})),
    # path("getAll", ClassSelectView.as_view({'get': 'list'})),
    # path("getParentById/<int:pk>", ClassSelectView.as_view({'get': 'retrieve'})),
    # path("update/<int:pk>", ClassOtherView.as_view({'patch': 'update'})),
    # path("delete/<int:pk>", ClassOtherView.as_view({'delete': 'destroy'})),
]
