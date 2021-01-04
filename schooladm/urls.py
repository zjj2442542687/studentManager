from django.urls import path

from schooladm.views import SchooladmView

urlpatterns = [
    path("insert", SchooladmView.as_view({'post': 'create'})),
    path("getAll", SchooladmView.as_view({'get': 'list'})),
    path("delete/<int:pk>", SchooladmView.as_view({'delete': 'destroy'})),
]
