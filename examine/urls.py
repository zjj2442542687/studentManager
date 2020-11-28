from django.urls import path

from examine.views.examine_insert import ExamineInsertView
from examine.views.examine_other import ExamineOtherView
from examine.views.examine_search import ExaminePaginationSelectView

urlpatterns = [
    path("insert", ExamineInsertView.as_view({'post': 'create'})),
    path("update/<int:pk>", ExamineOtherView.as_view({'patch': 'examine_update'})),
    path("delete/<int:pk>", ExamineOtherView.as_view({'patch': 'destroy'})),
    # 查询所有审核信息
    path("getAll", ExaminePaginationSelectView.as_view({'get': 'list'})),
    # 查询审核情况(根据学生ID、作业ID)
    path("getInfo", ExaminePaginationSelectView.as_view({'get': 'search'})),
]
