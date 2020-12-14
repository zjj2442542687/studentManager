from django.urls import path


from classs.views.class_insert import ClassInsertView
from classs.views.class_search import ClassPaginationSelectView
from classs.views.class_select import ClassSelectView
from classs.views.class_other import ClassOtherView,ClassDeleteAllView


urlpatterns = [
    path("insert", ClassInsertView.as_view({'post': 'create'})),
    path("getAll", ClassSelectView.as_view({'get': 'list'})),
    path("getClassByName/<str:class_name>", ClassSelectView.as_view({'get': 'retrieve_by_name'})),
    path("delete/<int:pk>", ClassOtherView.as_view({'delete': 'destroy'})),
    # 批量删除班级信息
    path("delete_all", ClassDeleteAllView.as_view({'post': 'destroy_all'})),
    path("selectBySchoolId/<int:school_id>", ClassSelectView.as_view({'get': 'retrieve_by_school_id'})),
    path("search", ClassPaginationSelectView.as_view({'get': 'search'})),
    path("partialUpdate/<int:pk>", ClassOtherView.as_view({'patch': 'partial_update'})),
]
