from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import User
from user.views.urls import get_info


class UserInfoSerializers(ModelSerializer):
    pass
    # name = serializers.SerializerMethodField(label='真实姓名')
    #
    # # 把用户详情中的name返回
    # def get_name(self, user):
    #     try:
    #         return UserDetails.objects.get(user=user).name
    #     except UserDetails.DoesNotExist:
    #         return None


# 包括所有参数的序列化
class UserInfoSerializersAll(UserInfoSerializers):
    class Meta:
        model = User
        fields = "__all__"


# 没有token的序列化
class UserInfoSerializersNoToken(UserInfoSerializers):
    class Meta:
        model = User
        exclude = ["token"]


# 不显示token的
class UserInfoSerializersLess(UserInfoSerializers):
    class Meta:
        model = User
        exclude = ['token']


# 不显示password(只写，不显示)
class UserInfoSerializersLogin(UserInfoSerializers):
    password = serializers.CharField(write_only=True, label="密码")

    class Meta:
        model = User
        fields = "__all__"
        depth = 1


# 只显示password(只写，不显示)
class UserInfoSerializersPassword(UserInfoSerializers):
    password = serializers.CharField(label='密码', required=False)

    class Meta:
        model = User
        fields = ["password"]


# 手机号验证码验证
class UserInfoSerializersCheck(UserInfoSerializers):
    phone_number = serializers.CharField(label='手机号码', required=False)

    class Meta:
        model = User
        fields = ["phone_number"]


# 修改信息的token
# class UserInfoSerializersUpdate(UserInfoSerializers):
#     class Meta:
#         model = User
#         exclude = ['token']


# update中包含的序列化
class UserInfoSerializersUpdate(ModelSerializer):
    user_name = serializers.CharField(label='用户名', required=False)
    phone_number = serializers.CharField(label='手机号', required=False)

    class Meta:
        model = User
        fields = ["user_name", "phone_number"]


# updatePhone中包含的序列化
class UserInfoSerializersUpdatePhone(ModelSerializer):
    phone_number = serializers.CharField(label='手机号', required=False)

    class Meta:
        model = User
        fields = ["phone_number"]


# 手机号验证码修改密码
class UserInfoSerializersUpdatePasswordByPhone(ModelSerializer):
    phone_number = serializers.CharField(label='手机号', required=False)
    password = serializers.CharField(label='密码', required=False)

    class Meta:
        model = User
        fields = ["phone_number", "password"]


class UserSerializersSearch(ModelSerializer):
    # role_info = serializers.SerializerMethodField(label='角色信息')

    class Meta:
        model = User
        fields = ["id", "user_name", "role", "user_details", "phone_number"]
        depth = 2

    def get_role_info(self, user: User):
        info = get_info(user.id, user.role)

        return info.search() if info else None
