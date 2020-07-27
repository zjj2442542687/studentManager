from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from classs.views.class_insert import ClassInsertView
from classs.views.class_select import ClassSelectView
from classs.views.class_other import ClassOtherView


urlpatterns = [
    path("insert", ClassInsertView.as_view({'post': 'create'})),
    path("getAll", ClassSelectView.as_view({'get': 'list'})),
    path("delete/<int:pk>", ClassOtherView.as_view({'delete': 'destroy'})),
]
