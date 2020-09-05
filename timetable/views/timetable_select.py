from drf_yasg import openapi

from student.models import Student
from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema, no_body

from timetable.views.timetable_serializers import TimetableDepth2SerializersInsert
from timetable.views.views import select_class
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, integer_schema


class TimetableSelectView(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableDepth2SerializersInsert

    @swagger_auto_schema(
        operation_summary="查询班级的课表",
        operation_description="传入班级id",
        request_body=request_body(properties={
            'class_id': integer_schema('班级id'),
        })
    )
    def select_class(self, request):
        class_id = request.data.get('class_id')
        return select_class(self, class_id)

    @swagger_auto_schema(
        operation_summary="token查询课表",
        operation_description="传入token",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ]
    )
    def select_student_timetable_by_token(self, request):
        # 判断token
        check_token = pd_token(request)
        if check_token:
            return check_token

        if request.auth != 1:
            return response_error_400(message="需要出入学生token")

        try:
            clazz = Student.objects.get(user_info_id=request.user).clazz
            if not clazz:
                return response_error_400(message="请先加入班级")
            return select_class(self, clazz.id)
        except Student.DoesNotExist:
            return response_error_400(message="未找到该学生")





