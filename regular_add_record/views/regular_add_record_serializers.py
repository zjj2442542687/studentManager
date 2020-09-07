from rest_framework.serializers import ModelSerializer

from regular_add_record.models import RegularAddRecord


class RegularAddRecordInfoSerializersAll(ModelSerializer):
    class Meta:
        model = RegularAddRecord
        fields = "__all__"
