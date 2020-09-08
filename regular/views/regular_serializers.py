from regular.models import Regular
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class RegularInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Regular
        fields = "__all__"
