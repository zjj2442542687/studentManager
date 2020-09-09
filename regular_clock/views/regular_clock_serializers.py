from rest_framework.serializers import ModelSerializer

from regular_clock.models import RegularClock


class RegularClockInfoSerializersAll(ModelSerializer):
    class Meta:
        model = RegularClock
        fields = "__all__"
