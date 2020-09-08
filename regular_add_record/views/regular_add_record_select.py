from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersAll


class RegularAddRecordSelectView(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 GenericViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersAll
