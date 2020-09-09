from django.urls import path

from work.views.work_insert import WorkInsertView
from work.views.work_other import WorkOtherView

urlpatterns = [
    path("insert", WorkInsertView.as_view({'post': 'create'})),
    # 根据token修改作业信息
    path("update", WorkOtherView.as_view({'patch': 'partial_update'})),
]
