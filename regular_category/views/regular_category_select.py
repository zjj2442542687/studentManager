from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular_category.models import RegularCategory
from regular_category.views.regular_category_serializers import RegularCategoryInfoSerializersAll


class RegularCategorySelectView(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                GenericViewSet):
    queryset = RegularCategory.objects.all()
    serializer_class = RegularCategoryInfoSerializersAll
