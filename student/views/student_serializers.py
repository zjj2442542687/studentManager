from rest_framework import mixins
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from classs.views.class_serializers import ClassSerializersSearch
from student.models import Student

# 添加操作的序列化
from user.views.user_serializers import UserSerializersSearch


class StudentInfoSerializersInsert(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


# 修改操作的序列化
class StudentInfoSerializersUpdate(ModelSerializer):
    class Meta:
        model = Student
        fields = []


# 管理员修改的序列化
class StudentInfoSerializersAdmUpdate(ModelSerializer):
    class Meta:
        model = Student
        # fields = "__all__"
        exclude = ['user']
        # depth = 2

    name = serializers.CharField(label='姓名', required=False)
    card = serializers.CharField(label='身份证', required=False)
    # identity = serializers.CharField(label='身份', required=False)
    phone_number = serializers.CharField(label='手机号码', required=False)
    # id = serializers.IntegerField(label='学号')


# 查询操作的序列化
class StudentInfoSerializersSelect(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentSerializersSearch(ModelSerializer):
    user = serializers.SerializerMethodField(label="用户信息")
    clazz = serializers.SerializerMethodField(label="班级信息")

    class Meta:
        model = Student
        fields = ["id", "user", "clazz", "school"]
        depth = 2

    def get_user(self, student: Student):
        # instance = User.objects.all().filter()
        instance = student.user
        serializer = UserSerializersSearch(instance)
        return serializer.data

    def get_clazz(self, student: Student):
        instance = student.clazz
        serializer = ClassSerializersSearch(instance)
        return serializer.data
