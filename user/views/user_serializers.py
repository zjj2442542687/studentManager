from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import User

from user_details.models import UserDetails


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


# 不显示password和token的
class UserInfoSerializersLess(UserInfoSerializers):
    class Meta:
        model = User
        exclude = ['password', 'token']


# 不显示password
class UserInfoSerializersNoPassword(UserInfoSerializers):
    class Meta:
        model = User
        exclude = ['password']


# 修改信息的token
# class UserInfoSerializersUpdate(UserInfoSerializers):
#     class Meta:
#         model = User
#         exclude = ['token']


# update中包含的序列化
class UserInfoSerializersUpdate(ModelSerializer):
    user_name = serializers.CharField(label='用户名', required=False)
    password = serializers.CharField(label='密码', required=False)
    phone_number = serializers.CharField(label='手机号', required=False)
    role = serializers.IntegerField(label='角色', required=False)
    avatar = serializers.ImageField(label='头像', required=False)

    class Meta:
        model = UserDetails
        fields = ["user_name", "password", "phone_number", "role", "avatar"]
