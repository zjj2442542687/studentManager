from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from parent.views.parent_insert import ParentInsertView
from parent.views.parent_other import ParentOtherView
from parent.views.parent_select import ParentSelectView
from user.views.user_insert import UserInsertView
from user.views.user_other import UserOtherView
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", ParentInsertView.as_view({'post': 'create'})),
    path("getAll", ParentSelectView.as_view({'get': 'list'})),
    path("getParentById/<int:pk>", ParentSelectView.as_view({'get': 'retrieve'})),
    path("update/<int:pk>", ParentOtherView.as_view({'patch': 'update'})),
    # path("delete/<int:pk>", UserOtherView.as_view({'delete': 'destroy'})),
]
