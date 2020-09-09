from django.urls import path

from regular.views.regular_insert import RegularInsertView
from regular.views.regular_other import RegularOtherView
from regular.views.regular_search import RegularPaginationSelectView
from regular.views.regular_select import RegularSelectView

urlpatterns = [
    path("insert", RegularInsertView.as_view({'post': 'create'})),
    path("delete/<int:pk>", RegularOtherView.as_view({'delete': 'destroy'})),
    path("update/<int:pk>", RegularOtherView.as_view({'patch': 'partial_update'})),
    # path("list", RegularSelectView.as_view({'get': 'list'})),
    path("search", RegularPaginationSelectView.as_view({'get': 'search'})),
]
