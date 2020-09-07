from django.urls import path

from week.views.week_insert import WeekInsertView
from week.views.week_other import WeekOtherView

urlpatterns = [
    path("insert", WeekInsertView.as_view({'post': 'create'})),
    path("delete/<int:pk>", WeekOtherView.as_view({'delete': 'destroy'})),
    path("update/<int:pk>", WeekOtherView.as_view({'patch': 'partial_update'})),
    path("list", WeekOtherView.as_view({'get': 'list'})),
]
