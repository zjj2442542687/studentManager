from django.urls import path

from teacher.views.teacher_insert import TeacherInsertView, TeacherInsertFileView
from teacher.views.teacher_search import TeacherPaginationSelectView
from teacher.views.teacher_select import TeacherSelectView, ClassSelectView
from teacher.views.teacher_other import TeacherOtherView, TeacherAmdView, TeacherDeleteAllView
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", TeacherInsertView.as_view({'post': 'create'})),
    # 根据token获得老师信息
    path("getInfoByToken", TeacherSelectView.as_view({'post': 'retrieve_by_token'})),
    path("insertFile", TeacherInsertFileView.as_view({'post': 'batch_import'})),
    path("delete/<int:pk>", TeacherOtherView.as_view({'delete': 'destroy'})),
    # 批量删除老师信息
    path("deleteAll", TeacherOtherView.as_view({'delete': 'destroy_all'})),
    # 批量删除老师信息
    path("deleteAll2", TeacherDeleteAllView.as_view({'post': 'destroy_all2'})),
    # 根据token修改老师信息
    path("update", TeacherOtherView.as_view({'patch': 'partial_update'})),
    # 管理员根据token修改老师信息
    path("admUpdate/<int:pk>", TeacherAmdView.as_view({'patch': 'partial_update_adm'})),

    # 分页查询
    path("search", TeacherPaginationSelectView.as_view({'get': 'search'})),
    # 查询所有老师信息
    path("getAll", TeacherSelectView.as_view({'get': 'list'})),
    # 查询辅导员所带班级信息
    path("getClazz", ClassSelectView.as_view({'get': 'search_clazz'})),
    # 查询老师所带班级信息
    path("getClazzByTeacher", ClassSelectView.as_view({'get': 'search_clazz_teacher'})),
]
