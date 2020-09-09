from regular.models import Regular
from rest_framework import serializers

from user.views.user_serializers import UserSerializersSearch


class RegularInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = Regular
        fields = "__all__"


class RegularSerializersSearch(serializers.ModelSerializer):
    # user = UserSerializersSearch(label="用户id", read_only=True)
    user_id = serializers.IntegerField(label="用户id", read_only=True)

    class Meta:
        model = Regular
        exclude = ['user']
        depth = 1
