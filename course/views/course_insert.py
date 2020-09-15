from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from course.models import Course
from course.views.course_serializers import CourseALlSerializers
from teacher.models import Teacher
from timetable.models import Timetable
from utils.my_response import response_success_200, STATUS_PARAMETER_ERROR
from utils.my_swagger_auto_schema import request_body, string_schema, integer_schema


class CourseInsertView(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseALlSerializers

    @swagger_auto_schema(
        request_body=request_body(properties={
            'timetable_id': integer_schema('课表id'),
            'teacher_info': integer_schema('老师ID'),
            'course_name': string_schema('课程名'),
            'index': string_schema('第几节课'),
        }),
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def create(self, request, *args, **kwargs):
        teacher_info = request.data.get('teacher_info')
        timetable_id = request.data.get('timetable_id')
        # print(Class.objects.filter(grade_name=grade_name))
        # if Class.objects.filter(grade_name=grade_name):
        #     message = "班级已经存在"
        #     return response_error_400(status=STATUS_CODE_ERROR, message=message)
        if not Teacher.objects.filter(id=teacher_info):
            message = "老师ID信息不存在"
            return response_success_200(status=STATUS_PARAMETER_ERROR, message=message)
        if not Timetable.objects.filter(id=timetable_id):
            message = "课程表不存在"
            return response_success_200(status=STATUS_PARAMETER_ERROR, message=message)
        # 把课程添加到课程表中
        resp = super().create(request)
        Timetable.objects.get(id=timetable_id).course_info.add(resp.data['id'])
        print(resp.data)
        return response_success_200(data=resp.data)
