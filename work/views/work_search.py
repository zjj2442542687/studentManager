from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from utils.my_limit_offset_pagination import MyLimitOffsetPagination
from work.models import Work
from work.views.work_serializers import WorkSerializersSearch


class WorkPaginationSelectView(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializersSearch
    pagination_class = MyLimitOffsetPagination

    """
        List a queryset.
        """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
