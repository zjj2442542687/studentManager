from classs.models import Class
from course.models import Course
from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema

from timetable.views import views
from timetable.views.timetable_serializers import TimetableAllSerializersInsert
from utils.my_response import response_success_200, response_error_400, STATUS_PARAMETER_ERROR
from utils.my_swagger_auto_schema import request_body, integer_schema, string_schema


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

    # @swagger_auto_schema(
    #     request_body=request_body(properties={
    #         'class_info': integer_schema('班级id'),
    #         'course_info': integer_schema('课程ID'),
    #         'week': string_schema('星期'),
    #         'Date': string_schema('时间'),
    #     })
    # )
    # def create(self, request, *args, **kwargs):
    #     class_info = request.data.get('class_info')
    #     course_info = request.data.get('course_info')
    #     if not Class.objects.filter(id=class_info):
    #         message = "班级ID信息不存在"
    #         return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)
    #     if not Course.objects.filter(id=course_info):
    #         message = "课程不存在"
    #         return response_error_400(status=STATUS_PARAMETER_ERROR, message=message)
    #     # 把课程添加到课程表中
    #     resp = super().create(request)
    #     Timetable.objects.get(id=resp.data['id']).course_info.add(course_info)
    #     print(resp.data)
    #     return response_success_200(data=resp.data)
