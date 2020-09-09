from regular_add_record.models import RegularAddRecord
from rest_framework import serializers

from user.views.user_serializers import UserSerializersSearch
from week.views.week_serializers import WeekInfoSerializersAll


class RegularAddRecordInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = RegularAddRecord
        fields = "__all__"


class RegularAddRecordInfoSerializersInsert(serializers.ModelSerializer):
    class Meta:
        model = RegularAddRecord
        exclude = ["user"]




