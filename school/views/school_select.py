from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from school.models import School
from school.views.school_insert import SchoolInfoSerializers


class SchoolSelectView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolInfoSerializers
