from rest_framework.serializers import ModelSerializer

from classs.models import Class
from teacher.models import Teacher
from rest_framework import serializers

# 全部的序列化
from user.models import User
from user.views.user_serializers import UserSerializersSearch


class TeacherInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


# 全部的序列化且深层1
class TeacherInfoSerializersDepth(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        depth = 1


# 管理员修改的序列化
class TeacherInfoSerializersAdmUpdate(ModelSerializer):
    title = serializers.CharField(label='职称', required=False)
    identity = serializers.CharField(label='身份', required=False)

    class Meta:
        model = Teacher
        fields = ['title', 'identity']


# 修改操作的序列化
class TeacherInfoSerializersUpdate(ModelSerializer):
    title = serializers.CharField(label='title', required=False)
    identity = serializers.CharField(label='identity', required=False)

    class Meta:
        model = Teacher
        fields = ['title', 'identity']


class TeacherSerializersSearch(ModelSerializer):
    clazz = serializers.SerializerMethodField(label='班级信息')
    user = serializers.SerializerMethodField(label="用户信息")

    class Meta:
        model = Teacher
        fields = ["id", "user", "school", "clazz"]
        depth = 2

    def get_user(self, teacher: Teacher):
        # instance = User.objects.all().filter()
        instance = teacher.user
        serializer = UserSerializersSearch(instance)
        return serializer.data

    def get_clazz(self, teacher: Teacher):
        try:
            return Class.objects.get(headmaster_id=teacher.user.id)
        except Class.DoesNotExist:
            print("没找到")
            return None
        except Class.MultipleObjectsReturned:
            print("返回多个!!!!!!")
            return None
