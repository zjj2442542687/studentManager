from rest_framework import serializers

from regular.models import Regular
from utils.my_time import time_stamp_to_str


class RegularInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = Regular
        fields = "__all__"


class RegularSerializersSearch(serializers.ModelSerializer):
    # user = UserSerializersSearch(label="用户id", read_only=True)
    user_id = serializers.IntegerField(label="用户id", read_only=True)
    creation_time_str = serializers.SerializerMethodField(label="创建时间的string表示", read_only=True)

    class Meta:
        model = Regular
        exclude = ['user']
        depth = 1

    def get_creation_time_str(self, regular: Regular):
        creation_time = regular.creation_time
        return time_stamp_to_str(time_stamp=creation_time, date_format="%Y-%m-%d %H:%M:%S")
