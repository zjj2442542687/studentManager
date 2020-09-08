import pandas as pd
import numpy as np
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from classs.models import Class
from course.models import Course
from teacher.models import Teacher
from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema, no_body

from timetable.views import views
from timetable.views.timetable_serializers import TimetableAllSerializersInsert
from utils.my_info_judge import pd_adm_token
from utils.my_response import response_success_200, response_error_400, STATUS_PARAMETER_ERROR
from utils.my_swagger_auto_schema import request_body, integer_schema, string_schema
from week.models import Week


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


class TimetableInsertFileView(mixins.CreateModelMixin,
                              GenericViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableAllSerializersInsert
    parser_classes = [MultiPartParser]
    """
    batch_create

    批量导入课程

    传入文件ID
    """

    @swagger_auto_schema(
        operation_summary="课程信息批量导入",
        operation_description="传入文件",
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='文件 '),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ],
    )
    def batch_import(self, request, *args, **kwargs):
        check_token = pd_adm_token(request)
        if check_token:
            return check_token

        file = request.FILES.get("file")

        check_file = batch_import_test(file)
        if check_file:
            return check_file

        excel_data = pd.read_excel(file, header=0, dtype='str')
        for dt in excel_data.iterrows():
            clazz = dt[1]['班级']
            # week = dt[1]['星期']
            teacher = ['课程老师工号']
            allweek = ['星期', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            week = Week.objects.create(index=allweek.index(dt[1]['星期']))
            course = ['课程', ' 第一节课', ' 第二节课', ' 第三节课', ' 第四节课', ' 第五节课', ' 第六节课', ' 第七节课', ' 第八节课']
            for j in range(1, 9):
                s = dt[1]['课程老师工号' + str(j)]
                if s is not np.nan:
                    teacher.append(s)
            # 创建timetable表
            timetable = Timetable.objects.create(week=week, clazz=Class.objects.get(class_name=clazz))
            for j in range(1, len(teacher)):
                # print(j)
                Course.objects.create(teacher=Teacher.objects.get(pk=teacher[j]), course_name=dt[1][course[j]], index=j, timetable=timetable)

        return response_success_200(message="成功!!!!")


def batch_import_test(file):
    excel_data = pd.read_excel(file, header=0, dtype='str')
    # print(excel_data)
    test = []
    i = 0
    for dt in excel_data.iterrows():
        i = i + 1
        message = ""
        clazz = dt[1]['班级']
        week = dt[1]['星期']
        teacher = ['课程老师工号']
        for j in range(1, 9):
            s = dt[1]['课程老师工号' + str(j)]
            if s is not np.nan:
                teacher.append(s)

        if week not in ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']:
            message += "星期不正确"

        if not Class.objects.filter(class_name=clazz):
            message += ",班级不存在"

        for j in range(1, len(teacher)):
            if not Teacher.objects.filter(pk=teacher[j]):
                message += ",第" + str(j) + "节课老师不存在"

        if message:
            test.append({"index": i, "message": message})
    if len(test) > 0:
        return response_error_400(status=STATUS_PARAMETER_ERROR, message="有错误信息", err_data=test, length=len(test))
    return None
