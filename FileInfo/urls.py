from django.urls import path

from teacher.views.teacher_insert import TeacherInsertView
from teacher.views.teacher_select import TeacherSelectView
from FileInfo.views import *
from user.views.user_other import UserOtherView, Other
from user.views.user_select import UserSelectView

urlpatterns = [
    path('file/<int:pk>', FileInfoView.as_view({'get': 'retrieve'})),
    path('file/create', FileInfoView.as_view({'post': 'create'})),
    path("getAll", FileInfoView.as_view({'get': 'list'})),
    path("delete/<int:pk>", FileInfoView.as_view({'delete': 'destroy'})),
    path("download/<int:pk>", FileInfoDownloadView.as_view({'get': 'download'})),
]
