from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import Course
from course.views.course_serializers import CourseALlSerializers
from timetable.models import Timetable


class TimetableAllSerializersInsert(ModelSerializer):
    # 课表中添加每节课的序列化
    class Meta:
        model = Timetable
        fields = "__all__"


class TimetableDepth2SerializersInsert(ModelSerializer):
    clazz = serializers.SerializerMethodField(label="班级信息")
    course = serializers.SerializerMethodField(label="课程信息")

    # 课表中depth的序列化
    class Meta:
        model = Timetable
        fields = ['id', 'date', 'clazz', 'week', 'course']
        depth = 1

    def get_clazz(self, timetable: Timetable):
        clazz = timetable.clazz
        if clazz:
            return {
                "id": clazz.id,
                "clazz_name": clazz.class_name
            }

    def get_course(self, timetable: Timetable):
        try:
            instance = Course.objects.filter(timetable_id=timetable.id)
            serializer = CourseSelectSerializers(instance, many=True)
            return serializer.data
        except AttributeError:
            return None


class CourseSelectSerializers(ModelSerializer):
    teacher = serializers.SerializerMethodField(label="老师信息")

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'index', 'teacher']

    def get_teacher(self, course: Course):
        teacher = course.teacher
        return {
            "name": teacher.user.user_details.name,
            "phone_number": teacher.user.phone_number
        } if teacher else None
