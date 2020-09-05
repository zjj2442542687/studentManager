from django.urls import path

from parent.views.parent_insert import ParentInsertView, ParentInsertFileView
from parent.views.parent_other import ParentOtherView, ParentAdmView
from parent.views.parent_search import ParentPaginationSelectView
from parent.views.parent_select import ParentSelectView

urlpatterns = [
    path("insert", ParentInsertView.as_view({'post': 'create'})),
    # 获得全部
    # path("getAll", ParentSelectView.as_view({'get': 'list'})),
    # 根据token获得家长信息
    path("getInfoByToken", ParentSelectView.as_view({'post': 'retrieve_by_token'})),
    # 根据id查询
    # path("getParentById/<int:pk>", ParentSelectView.as_view({'get': 'retrieve'})),
    # path("FileInfo/<int:pk>", ParentOtherView.as_view({'patch': 'FileInfo'})),
    path("delete/<int:pk>", ParentOtherView.as_view({'delete': 'destroy'})),
    # 根据token修改家长信息
    path("update", ParentOtherView.as_view({'patch': 'partial_update'})),
    # 根据token修改家长信息
    path("admupdate/<int:pk>", ParentAdmView.as_view({'patch': 'partial_update_adm'})),
    # 信息的批量导入
    path("insert_file", ParentInsertFileView.as_view({'post': 'batch_import'})),

    # 分页查询
    path("search", ParentPaginationSelectView.as_view({'get': 'search'})),
]
