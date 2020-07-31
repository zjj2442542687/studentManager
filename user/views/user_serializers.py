from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import User

from user_details.models import UserDetails


class UserInfoSerializers(ModelSerializer):
    name = serializers.SerializerMethodField(label='真实姓名')

    # 把用户详情中的name返回
    def get_name(self, user):
        try:
            return UserDetails.objects.get(user=user).name
        except UserDetails.DoesNotExist:
            return None


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
class UserInfoSerializersUpdate(UserInfoSerializers):
    class Meta:
        model = User
        exclude = ['token']
