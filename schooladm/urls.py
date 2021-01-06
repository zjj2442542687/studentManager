from django.urls import path

from schooladm.views import SchoolAdmView, SchoolAdmSelectView

urlpatterns = [
    path("insert", SchoolAdmView.as_view({'post': 'create'})),
    path("getAll", SchoolAdmView.as_view({'get': 'list'})),
    path("delete/<int:pk>", SchoolAdmView.as_view({'delete': 'destroy'})),
    # 根据学校ID查询学校管理员信息
    path("searchBySchool", SchoolAdmSelectView.as_view({'get': 'search_school'})),
]
