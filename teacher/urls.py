from django.urls import path

from teacher.views.teacher_insert import TeacherInsertView
from teacher.views.teacher_select import TeacherSelectView
from user.views.user_other import UserOtherView, Other
from user.views.user_select import UserSelectView

urlpatterns = [
    path("insert", TeacherInsertView.as_view({'post': 'create'})),

    path("getAll", TeacherSelectView.as_view({'get': 'list'})),
    path("getTeacherById/<int:pk>", TeacherSelectView.as_view({'get': 'retrieve'})),
    path("getUserByName/<str:name>", TeacherSelectView.as_view({'get': 'retrieve_by_name'})),
]
