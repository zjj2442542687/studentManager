from rest_framework.serializers import ModelSerializer

from timetable.models import Timetable


class TimetableAllSerializersInsert(ModelSerializer):
    # 课表中添加每节课的序列化
    class Meta:
        model = Timetable
        fields = "__all__"


class TimetableDepth2SerializersInsert(ModelSerializer):
    # 课表中depth的序列化
    class Meta:
        model = Timetable
        fields = "__all__"
        depth = 2
