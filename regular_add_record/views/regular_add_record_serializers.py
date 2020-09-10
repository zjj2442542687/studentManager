import time

from regular.views.regular_serializers import RegularSerializersSearch
from regular_add_record.models import RegularAddRecord
from rest_framework import serializers

from user.views.user_serializers import UserSerializersSearch
from utils.my_time import time_stamp_to_str
from week.views.week_serializers import WeekInfoSerializersAll


class RegularAddRecordInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = RegularAddRecord
        fields = "__all__"


class RegularAddRecordInfoSerializersInsert(serializers.ModelSerializer):
    class Meta:
        model = RegularAddRecord
        exclude = ["user"]


class RegularAddRecordSerializersSearch(serializers.ModelSerializer):
    # user = UserSerializersSearch(label="用户id", read_only=True)
    regular = RegularSerializersSearch(label="regular", read_only=True)
    user_id = serializers.IntegerField(label="用户id", read_only=True)
    reminder_time_str = serializers.SerializerMethodField(label="提醒时间", read_only=True)
    start_time_str = serializers.SerializerMethodField(label="每天开始的时间", read_only=True)
    end_time_str = serializers.SerializerMethodField(label="每天结束的时间", read_only=True)
    start_date_str = serializers.SerializerMethodField(label="开始日期时间", read_only=True)
    end_date_str = serializers.SerializerMethodField(label="结束日期时间", read_only=True)

    class Meta:
        model = RegularAddRecord
        exclude = ['user']

    def get_reminder_time_str(self, regular_add_record: RegularAddRecord):
        reminder_time = regular_add_record.reminder_time
        print(reminder_time)
        return time_stamp_to_str(time_stamp=reminder_time, date_format="%H:%M:%S")

    def get_start_time_str(self, regular_add_record: RegularAddRecord):
        start_time = regular_add_record.start_time
        return time_stamp_to_str(time_stamp=start_time, date_format="%H:%M:%S")

    def get_end_time_str(self, regular_add_record: RegularAddRecord):
        end_time = regular_add_record.end_time
        return time_stamp_to_str(time_stamp=end_time, date_format="%H:%M:%S")

    def get_start_date_str(self, regular_add_record: RegularAddRecord):
        start_date = regular_add_record.start_date
        return time_stamp_to_str(time_stamp=start_date, date_format="%Y-%m-%d %H:%M:%S")

    def get_end_date_str(self, regular_add_record: RegularAddRecord):
        end_date = regular_add_record.end_date
        return time_stamp_to_str(time_stamp=end_date, date_format="%Y-%m-%d %H:%M:%S")
