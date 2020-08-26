from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from student.views.student_insert import StudentInsertView, StudentInsertFileView
from student.views.student_search import StudentPaginationSelectView
from student.views.student_select import StudentSelectView
from student.views.student_other import StudentOtherView

urlpatterns = [
    path("insert", StudentInsertView.as_view({'post': 'create'})),
    # 获得全部
    # path("getAll", StudentSelectView.as_view({'get': 'list'})),
    # 根据token修改学生信息
    path("update", StudentOtherView.as_view({'patch': 'partial_update'})),
    # 根据token获得学生信息
    path("getInfoByToken", StudentSelectView.as_view({'post': 'retrieve_by_token'})),
    # 工具id查询
    # path("getStudentById/<int:pk>", StudentSelectView.as_view({'get': 'retrieve'})),
    # path("getStudentByName/<str:student_name>", StudentInsertView.as_view({'get': 'retrieve_by_student_name'})),
    # path("FileInfo/<int:pk>", StudentOtherView.as_view({'patch': 'FileInfo'})),
    path("delete/<int:pk>", StudentOtherView.as_view({'delete': 'destroy'})),
    path("insert_file", StudentInsertFileView.as_view({'post': 'batch_import'})),
    path("addParent", StudentInsertView.as_view({'post': 'add_parent'})),

    # 分页查询
    path("search", StudentPaginationSelectView.as_view({'get': 'search'})),
]
