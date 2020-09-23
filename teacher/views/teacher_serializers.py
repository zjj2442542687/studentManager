from rest_framework.serializers import ModelSerializer

from classs.models import Class
from classs.views.class_serializers import ClassSerializersSearch
from teacher.models import Teacher
from rest_framework import serializers

# 全部的序列化
from user.models import User
from user.views.user_serializers import UserSerializersSearch
from user_details.models import UserDetails


class TeacherInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


# 全部的序列化且深层1
class TeacherInfoSerializersInsert(ModelSerializer):
    user_info = serializers.SerializerMethodField(label="用户信息", read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"

    def get_user_info(self, teacher: Teacher):
        try:
            instance = teacher.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None


# 管理员修改的序列化
class TeacherInfoSerializersAdmUpdateUserDetails(ModelSerializer):
    name = serializers.CharField(label='姓名', required=False)
    avatar = serializers.ImageField(label='头像', required=False)
    birthday = serializers.IntegerField(label='生日', required=False)
    card = serializers.CharField(label='生日', required=False)
    qq = serializers.CharField(label='qq', required=False)
    email = serializers.CharField(label='邮箱', required=False)

    class Meta:
        model = UserDetails
        fields = ["name", "avatar", "sex", "birthday", "card", "qq", "email"]


class TeacherInfoSerializersAdmUpdate(ModelSerializer):
    phone_number = serializers.CharField(label='手机号码', required=False)
    # clazz_id = serializers.IntegerField(label='班级', required=False)
    user_details = TeacherInfoSerializersAdmUpdateUserDetails(label="详细详细")

    class Meta:
        model = Teacher
        exclude = ['user', 'school']


# 修改操作的序列化
class TeacherInfoSerializersUpdate(ModelSerializer):
    title = serializers.CharField(label='title', required=False)
    identity = serializers.CharField(label='identity', required=False)

    class Meta:
        model = Teacher
        fields = ['title', 'identity']


# 批量删除操作的序列化
class TeacherInfoSerializersDeleteAll(ModelSerializer):
    id_list = serializers.ListField(label='id_list', required=False)

    class Meta:
        model = Teacher
        fields = ['id_list']


class TeacherSerializersSearch(ModelSerializer):
    clazz = serializers.SerializerMethodField(label='班级信息')
    user = serializers.SerializerMethodField(label="用户信息")

    class Meta:
        model = Teacher
        fields = ["id", "user", "school", "clazz"]
        depth = 2

    def get_user(self, teacher: Teacher):
        try:
            instance = teacher.user
            serializer = UserSerializersSearch(instance)
            return serializer.data
        except AttributeError:
            return None

    def get_clazz(self, teacher: Teacher):
        try:
            instance = Class.objects.get(headmaster_id=teacher.user.id)
            serializer = ClassSerializersSearch(instance)
            return serializer.data
        except Class.DoesNotExist:
            print("没找到")
            return None
        except Class.MultipleObjectsReturned:
            print("返回多个!!!!!!")
            return None
