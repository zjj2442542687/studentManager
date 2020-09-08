from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from week.models import Week
from week.views.week_serializers import WeekInfoSerializersAll


class WeekSelectView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekInfoSerializersAll
