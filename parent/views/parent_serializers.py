from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from student.models import Student
from user.views.user_serializers import UserSerializersSearch


class ParentInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class ParentInfoSerializersInsert(ModelSerializer):
    user_info = serializers.SerializerMethodField(label="用户信息", read_only=True)

    class Meta:
        model = Parent
        fields = "__all__"

    def get_user_info(self, parent: Parent):
        try:
            instance = parent.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None


# 修改操作的序列化
class ParentInfoSerializersUpdate(ModelSerializer):
    sex = serializers.IntegerField(label='性别', required=False)
    phone_number = serializers.CharField(label='手机号', required=False)
    birthday = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)

    class Meta:
        model = Parent
        fields = ['sex', 'phone_number', 'birthday', 'qq', 'email']


# 修改操作的序列化
class ParentInfoSerializersAdmUpdate(ModelSerializer):
    name = serializers.CharField(label='姓名', required=False)
    card = serializers.CharField(label='身份证', required=False)
    # identity = serializers.CharField(label='身份', required=False)
    phone_number = serializers.CharField(label='手机号码', required=False)
    sex = serializers.IntegerField(label='性别', required=False)
    birthday = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)

    class Meta:
        model = Parent
        exclude = ['user']


# 查询需要的用户序列化
class StudentInfoSerializersUserInfo(ModelSerializer):
    class Meta:
        model = Student
        # fields = ['id', 'user_info']
        # fields = "__all__"
        exclude = ["parent"]
        depth = 1


class ParentInfoSerializersSelect(ModelSerializer):
    student = serializers.SerializerMethodField(label='学生')

    class Meta:
        model = Parent
        fields = "__all__"
        depth = 1

    def get_student(self, parent):
        return StudentInfoSerializersUserInfo(Student.objects.filter(parent=parent), many=True).data


class ParentSerializersSearch(ModelSerializer):
    user = serializers.SerializerMethodField(label="用户信息")

    class Meta:
        model = Parent
        fields = ["id", "user"]

    def get_user(self, parent: Parent):
        try:
            instance = parent.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None
        # instance = User.objects.all().filter()
