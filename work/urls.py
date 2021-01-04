from django.urls import path

from work.views.work_insert import WorkInsertView
from work.views.work_other import WorkOtherView, WorkInfoDownloadView
from work.views.work_search import WorkPaginationSelectView

urlpatterns = [
    path("insert", WorkInsertView.as_view({'post': 'create'})),
    # 根据token修改作业信息
    path("update/<int:pk>", WorkOtherView.as_view({'patch': 'partial_update'})),
    # 根据作业ID查询作业
    path('work/<int:pk>', WorkPaginationSelectView.as_view({'get': 'retrieve'})),
    # 查询所有作业
    path("getAll", WorkPaginationSelectView.as_view({'get': 'list'})),
    # 管理员查询作业信息
    path("getInfo", WorkPaginationSelectView.as_view({'get': 'search_adm'})),
    # 老师查询自己发布作业信息
    path("getTeacherInfo", WorkPaginationSelectView.as_view({'get': 'search_teacher'})),
    # 学生查询自己发布作业信息
    path("getStudentInfo", WorkPaginationSelectView.as_view({'get': 'search_student'})),
    # 辅导员查询自己班级作业信息
    path("getClassInfo", WorkPaginationSelectView.as_view({'get': 'search_clazz'})),
    # 删除作业
    path("delete/<int:pk>", WorkOtherView.as_view({'delete': 'destroy'})),
    # 根据作业ID下载作业附件
    path("download/<int:pk>", WorkInfoDownloadView.as_view({'get': 'download'})),
]
