from django.urls import path


from classs.views.class_insert import ClassInsertView
from classs.views.class_select import ClassSelectView
from classs.views.class_other import ClassOtherView


urlpatterns = [
    path("insert", ClassInsertView.as_view({'post': 'create'})),
    path("getAll", ClassSelectView.as_view({'get': 'list'})),
    path("getClassByName/<str:class_name>", ClassSelectView.as_view({'get': 'retrieve_by_name'})),
    path("delete/<int:pk>", ClassOtherView.as_view({'delete': 'destroy'})),
]
