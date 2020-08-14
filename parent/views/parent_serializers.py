from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from parent.models import Parent
from student.models import Student


class ParentInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


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
