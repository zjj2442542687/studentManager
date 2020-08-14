from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from parent.views.parent_insert import ParentInsertView, ParentInsertFileView
from parent.views.parent_other import ParentOtherView
from parent.views.parent_select import ParentSelectView

urlpatterns = [
    path("insert", ParentInsertView.as_view({'post': 'create'})),
    path("getAll", ParentSelectView.as_view({'get': 'list'})),
    # 根据token获得家长信息
    path("getInfoByToken", ParentSelectView.as_view({'post': 'retrieve_by_token'})),
    path("getParentById/<int:pk>", ParentSelectView.as_view({'get': 'retrieve'})),
    # path("FileInfo/<int:pk>", ParentOtherView.as_view({'patch': 'FileInfo'})),
    path("delete/<int:pk>", ParentOtherView.as_view({'delete': 'destroy'})),
    # 根据token修改家长信息
    path("update", ParentOtherView.as_view({'patch': 'partial_update'})),
    path("insert_file", ParentInsertFileView.as_view({'post': 'Batch_import'})),
]
