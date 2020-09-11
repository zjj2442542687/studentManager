from django.urls import path

from work.views.work_insert import WorkInsertView
from work.views.work_other import WorkOtherView
from work.views.work_search import WorkPaginationSelectView

urlpatterns = [
    path("insert", WorkInsertView.as_view({'post': 'create'})),
    # 根据token修改作业信息
    path("update/<int:pk>", WorkOtherView.as_view({'patch': 'partial_update'})),
    # 查询所有作业
    path("getAll", WorkPaginationSelectView.as_view({'get': 'list'})),
    # 删除作业
    path("delete/<int:pk>", WorkOtherView.as_view({'delete': 'destroy'})),
]
