from django.urls import path

from regular_add_record.views.regular_add_record_insert import RegularAddRecordInsertView
from regular_add_record.views.regular_add_record_other import RegularAddRecordOtherView
from regular_add_record.views.regular_add_record_search import RegularAddRecordPaginationSelectView
from regular_add_record.views.regular_add_record_select import RegularAddRecordSelectView

urlpatterns = [
    path("insert", RegularAddRecordInsertView.as_view({'post': 'create'})),
    path("delete/<int:pk>", RegularAddRecordOtherView.as_view({'delete': 'destroy'})),
    path("update/<int:pk>", RegularAddRecordOtherView.as_view({'patch': 'partial_update'})),
    # path("list", RegularAddRecordSelectView.as_view({'get': 'list'})),
    path("search", RegularAddRecordPaginationSelectView.as_view({'get': 'search'})),
]
