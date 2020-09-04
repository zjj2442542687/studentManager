from rest_framework import mixins
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from student.models import Student


# 添加操作的序列化
class StudentInfoSerializersInsert(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


# 修改操作的序列化
class StudentInfoSerializersUpdate(ModelSerializer):
    sex = serializers.IntegerField(label='性别', required=False)
    phone_number = serializers.CharField(label='手机号', required=False)
    birthday = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)

    class Meta:
        model = Student
        fields = ['sex', 'phone_number', 'birthday', 'qq', 'email']


# 查询操作的序列化
class StudentInfoSerializersSelect(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentSerializersSearch(ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "sex", "card", "phone_number", "birthday", "qq", "email", "clazz"]
        depth = 2

