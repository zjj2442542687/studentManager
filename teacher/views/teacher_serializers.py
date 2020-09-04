from rest_framework.serializers import ModelSerializer

from classs.models import Class
from teacher.models import Teacher
from rest_framework import serializers


# 全部的序列化
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


# 修改操作的序列化
class TeacherInfoSerializersUpdate(ModelSerializer):
    sex = serializers.IntegerField(label='性别', required=False)
    phone_number = serializers.CharField(label='手机号', required=False)
    birthday = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)
    title = serializers.CharField(label='title', required=False)
    identity = serializers.CharField(label='identity', required=False)

    class Meta:
        model = Teacher
        fields = ['sex', 'phone_number', 'birthday', 'qq', 'email', 'title', 'identity']


class TeacherSerializersSearch(ModelSerializer):
    clazz = serializers.SerializerMethodField(label='班级信息')

    class Meta:
        model = Teacher
        fields = ["id", "name", "sex", "card", "title", "identity", "phone_number", "birthday", "qq", "email", "school",
                  "clazz"]
        depth = 1

    def get_clazz(self, teacher: Teacher):
        try:
            return Class.objects.get(teacher_info_id=teacher.id)
        except Class.DoesNotExist:
            print("没找到")
            return None
        except Class.MultipleObjectsReturned:
            print("返回多个!!!!!!")
            return None
