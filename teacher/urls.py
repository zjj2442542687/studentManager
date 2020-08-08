from django.urls import path

from teacher.views.teacher_insert import TeacherInsertView, TeacherInsertFileView
from teacher.views.teacher_select import TeacherSelectView
from teacher.views.teacher_other import TeacherOtherView
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", TeacherInsertView.as_view({'post': 'create'})),

    path("getAll", TeacherSelectView.as_view({'get': 'list'})),
    path("getTeacherById/<int:pk>", TeacherSelectView.as_view({'get': 'retrieve'})),
    path("getUserByName/<str:name>", TeacherSelectView.as_view({'get': 'retrieve_by_name'})),
    path("insert_file", TeacherInsertFileView.as_view({'post': 'Batch_import'})),
    path("delete/<int:pk>", TeacherOtherView.as_view({'delete': 'destroy'})),
]
