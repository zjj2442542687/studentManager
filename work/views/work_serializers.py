from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from classs.models import Class
from work.models import Work


# 全部的序列化
class WorkInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


# 全部的序列化且深层1
class WorkInfoSerializersDepth(ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"
        depth = 1


# 修改操作的序列化
class TeacherInfoSerializersUpdate(ModelSerializer):
    title = serializers.CharField(label='title', required=False)
    course = serializers.CharField(label='作业课程科目', required=False)
    content = serializers.CharField(label='作业内容', required=False)
    request = serializers.CharField(label='作业要求', required=False)

    class Meta:
        model = Work
        fields = "__all__"


# 全部的序列化
class WorkSerializersSearch(ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"
