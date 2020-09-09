from django.urls import path

from regular_clock.views.regular_clock_insert import RegularClockInsertView
from regular_clock.views.regular_clock_select import RegularClockSelectView

urlpatterns = [
    path("insert", RegularClockInsertView.as_view({'post': 'create'})),
    # path("delete/<int:pk>", RegularCategoryOtherView.as_view({'delete': 'destroy'})),
    # path("update/<int:pk>", RegularCategoryOtherView.as_view({'patch': 'partial_update'})),
    path("list", RegularClockSelectView.as_view({'get': 'list'})),
]
