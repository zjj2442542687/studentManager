from django.urls import path

from regular_category.views.regular_category_insert import RegularCategoryInsertView
from regular_category.views.regular_category_other import RegularCategoryOtherView
from regular_category.views.regular_category_search import RegularCategoryPaginationSelectView

urlpatterns = [
    path("insert", RegularCategoryInsertView.as_view({'post': 'create'})),
    path("delete/<int:pk>", RegularCategoryOtherView.as_view({'delete': 'destroy'})),
    path("update/<int:pk>", RegularCategoryOtherView.as_view({'patch': 'partial_update'})),
    # path("list", RegularCategorySelectView.as_view({'get': 'list'})),
    path("search", RegularCategoryPaginationSelectView.as_view({'get': 'search'})),
]
