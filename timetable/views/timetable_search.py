from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class TimetableSearchView(mixins.CreateModelMixin,
                          GenericViewSet):
    queryset = Timetable.objects.all()
