from django.urls import path

from teacher.views.teacher_insert import TeacherInsertView, TeacherInsertFileView
from teacher.views.teacher_search import TeacherPaginationSelectView
from teacher.views.teacher_select import TeacherSelectView
from teacher.views.teacher_other import TeacherOtherView, TeacherAmdView
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", TeacherInsertView.as_view({'post': 'create'})),
    # 根据token获得老师信息
    path("getInfoByToken", TeacherSelectView.as_view({'post': 'retrieve_by_token'})),
    path("insert_file", TeacherInsertFileView.as_view({'post': 'batch_import'})),
    path("delete/<int:pk>", TeacherOtherView.as_view({'delete': 'destroy'})),
    # 根据token修改老师信息
    path("update", TeacherOtherView.as_view({'patch': 'partial_update'})),
    # 管理员根据token修改老师信息
    path("admUpdate/<int:pk>", TeacherAmdView.as_view({'patch': 'partial_update'})),

    # 分页查询
    path("search", TeacherPaginationSelectView.as_view({'get': 'search'})),
]
