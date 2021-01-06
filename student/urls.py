from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from student.views.student_insert import StudentInsertView, StudentInsertFileView
from student.views.student_search import StudentPaginationSelectView
from student.views.student_select import StudentSelectView
from student.views.student_other import StudentOtherView, StudentAdmView,StudentDeleteAllView

urlpatterns = [
    path("insert", StudentInsertView.as_view({'post': 'create'})),
    # 根据token修改学生信息
    path("update", StudentOtherView.as_view({'patch': 'partial_update'})),
    # 管理员根据token修改学生信息
    path("amdupdate/<int:pk>", StudentAdmView.as_view({'patch': 'partial_update_adm'})),
    # 根据token获得学生信息
    path("getInfoByToken", StudentSelectView.as_view({'post': 'retrieve_by_token'})),
    # 根据id删除学生
    path("delete/<int:pk>", StudentOtherView.as_view({'delete': 'destroy'})),
    # 批量删除老师信息
    path("deleteAll", StudentDeleteAllView.as_view({'post': 'destroy_all2'})),
    # 学生的批量导入
    path("insertFile", StudentInsertFileView.as_view({'post': 'batch_import'})),
    # 添加家长
    path("addParent", StudentInsertView.as_view({'post': 'add_parent'})),
    # 批量学生添加家长
    path("BatchAddParent", StudentInsertFileView.as_view({'post': 'batch_add_parent'})),

    # 分页查询
    path("search", StudentPaginationSelectView.as_view({'get': 'search'})),
    # 查询所有学生信息
    path("getAll", StudentSelectView.as_view({'get': 'list'})),
    # 根据班级查询所有学生信息
    path("getInfoByclass", StudentSelectView.as_view({'get': 'clazz_search'})),
]
