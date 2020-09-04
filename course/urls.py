from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

from course.views.course_insert import CourseInsertView
from course.views.course_other import CourseOtherView
from course.views.course_select import CourseSelectView

urlpatterns = [
    path("insert", CourseInsertView.as_view({'post': 'create'})),
    path("getAll", CourseSelectView.as_view({'get': 'list'})),
    path("delete/<int:pk>", CourseOtherView.as_view({'delete': 'destroy'})),

]
