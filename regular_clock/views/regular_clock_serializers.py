from rest_framework import serializers

from regular_clock.models import RegularClock
from utils.my_time import time_stamp_to_str


class RegularClockInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = RegularClock
        fields = "__all__"


class RegularClockSerializersSearch(serializers.ModelSerializer):
    clock_in_time_str = serializers.SerializerMethodField(label="打卡时间")

    class Meta:
        model = RegularClock
        fields = "__all__"

    def get_clock_in_time_str(self, regular_clock: RegularClock):
        clock_in_time = regular_clock.clock_in_time
        return time_stamp_to_str(time_stamp=clock_in_time, date_format="%Y-%m-%d %H:%M:%S")
