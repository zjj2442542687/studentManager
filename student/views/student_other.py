from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from student.models import Student
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, integer_schema


class StudentInfoSerializersOther(ModelSerializer):
    class Meta:
        model = Student
        fields = ('user_info', 'parent')


class StudentOtherView(ModelViewSet):
    """
    create:
    添加一条学生信息数据

    无描述
    """

    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersOther

    @swagger_auto_schema(
        request_body=request_body(properties={
            'student_id': integer_schema('学生id'),
            'parent_id': integer_schema('家长id'),
        })
    )
    def add_parent(self, request):
        student_id = request.data.get('student_id')
        parent_id = request.data.get('parent_id')

        self.queryset.get(pk=student_id).parent.add(parent_id)

        print(student_id)
        print(parent_id)
        return response_success_200(message="成功")
