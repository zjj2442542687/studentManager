from rest_framework import mixins
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from classs.views.class_serializers import ClassSerializersSearch
from parent.views.parent_serializers import ParentSerializersSearch
from student.models import Student

# 添加操作的序列化
from user.views.user_serializers import UserSerializersSearch
from user_details.models import UserDetails
from user_details.views.user_details_serializers import UserDetailsInfoSerializersUpdate


class StudentInfoSerializersInsert(ModelSerializer):
    parent = ParentSerializersSearch(label="家长信息", read_only=True)
    user_info = serializers.SerializerMethodField(label="用户信息", read_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        # depth = 1

    def get_user_info(self, student: Student):
        try:
            instance = student.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None


# 修改操作的序列化
class StudentInfoSerializersUpdate(ModelSerializer):
    class Meta:
        model = Student
        fields = []


class StudentInfoSerializersAdmUpdateUserDetails(ModelSerializer):
    name = serializers.CharField(label='姓名', required=False)
    avatar = serializers.ImageField(label='头像', required=False)
    birthday = serializers.IntegerField(label='生日', required=False)
    card = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)

    class Meta:
        model = UserDetails
        fields = ["name", "avatar", "sex", "birthday", "card", "qq", "email"]


# 管理员修改的序列化
class StudentInfoSerializersAdmUpdate(ModelSerializer):
    phone_number = serializers.CharField(label='手机号码', required=False)
    user_details = StudentInfoSerializersAdmUpdateUserDetails(label="详细详细")

    class Meta:
        model = Student
        exclude = ['user']


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
        try:
            instance = student.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None

    def get_clazz(self, student: Student):
        try:
            instance = student.clazz
            serializer = ClassSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None
