from rest_framework.serializers import ModelSerializer

from classs.models import Class
from rest_framework import serializers

from user.views.user_serializers import UserSerializersSearch


class ClassSerializersSearch(ModelSerializer):
    headmaster = serializers.SerializerMethodField(label="用户信息")

    # 查询
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1

    def get_headmaster(self, clazz: Class):
        instance = clazz.headmaster
        serializer = UserSerializersSearch(instance)
        return serializer.data
