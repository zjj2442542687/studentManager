from rest_framework.serializers import ModelSerializer

from examine.models import Examine


# 全部的序列化
class ExamineInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Examine
        fields = "__all__"
        # depth = 1
