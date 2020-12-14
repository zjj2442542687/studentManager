from rest_framework.serializers import ModelSerializer

from classs.models import Class
from rest_framework import serializers

from student.models import Student
from user.views.user_serializers import UserSerializersSearch


class ClassSerializersSearch(ModelSerializer):
    number = serializers.SerializerMethodField(label="班级人数")
    headmaster = serializers.SerializerMethodField(label="用户信息")

    # 查询
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1

    def get_headmaster(self, clazz: Class):
        try:
            instance = clazz.headmaster
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None

    def get_number(self, clazz: Class):
        try:
            count = Student.objects.filter(clazz_id=clazz.id).count()
            return count
        except AttributeError:
            return -1


# 修改操作的序列化
class ClassInfoSerializersUpdate(ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"
