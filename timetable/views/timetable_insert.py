from course.models import Course
from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema

from timetable.views import views
from timetable.views.timetable_serializers import TimetableAllSerializersInsert
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, integer_schema


class TimetableInsertView(mixins.CreateModelMixin,
                          GenericViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableAllSerializersInsert

    @swagger_auto_schema(
        operation_description="添加课程到课表中",
        operation_summary="timetable添加课程",
        request_body=request_body(properties={
            'timetable_id': integer_schema('课表id'),
            'course_id': integer_schema('课程id'),
        })
    )
    def add_course(self, request):
        timetable_id = request.data.get('timetable_id')
        course_id = request.data.get('course_id')

        result = views.add_course(timetable_id, course_id)
        return result if result else response_success_200(message="添加成功")

