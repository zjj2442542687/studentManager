from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular_clock.models import RegularClock
from regular_clock.views.regular_clock_serializers import RegularClockInfoSerializersAll


class RegularClockSelectView(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             GenericViewSet):
    queryset = RegularClock.objects.all()
    serializer_class = RegularClockInfoSerializersAll
