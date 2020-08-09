from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user_details.models import UserDetails


# 包括所有参数的序列化
class UserDetailsInfoSerializersAll(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"


# 没有user的序列化
class UserDetailsInfoSerializersNoUser(ModelSerializer):
    class Meta:
        model = UserDetails
        exclude = ["user"]


# 查询全部，而且深度查询一级
class UserInfoSerializersUserInfo(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"
        depth = 1


# update中包含的序列化
class UserDetailsInfoSerializersUpdate(ModelSerializer):
    name = serializers.CharField(label='昵称', required=False)
    avatar = serializers.ImageField(label='头像', required=False)
    sex = serializers.IntegerField(label='性别', required=False)
    birthday = serializers.DateTimeField(label='生日', required=False)
    personal_signature = serializers.CharField(label='个性签名', required=False)

    class Meta:
        model = UserDetails
        fields = ["name", "avatar", "sex", "birthday", "personal_signature"]