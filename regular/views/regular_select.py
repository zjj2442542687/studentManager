from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll


class RegularSelectView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Regular.objects.all()
    serializer_class = RegularInfoSerializersAll
