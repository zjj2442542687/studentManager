from course.models import Course
from timetable.models import Timetable
from utils.my_response import response_error_400, response_success_200
from utils.status import STATUS_NOT_FOUND_ERROR, STATUS_404_NOT_FOUND


def add_course(timetable_id: int, course_id: int):
    if not Course.objects.filter(id=course_id):
        return response_success_200(code=STATUS_NOT_FOUND_ERROR, message="课程id不存在")

    try:
        Timetable.objects.get(pk=timetable_id).course_info.add(course_id)
    except Timetable.DoesNotExist:
        return response_success_200(code=STATUS_404_NOT_FOUND, message="课表不存在")

    print(timetable_id)
    print(course_id)
    return None


def select_class(self, class_id):
    print(class_id)

    timetable = self.queryset.filter(clazz=class_id)
    print(timetable)
    if not timetable:
        return response_success_200(code=STATUS_NOT_FOUND_ERROR, message="该班级没有课表")
    serializer = self.get_serializer(timetable, many=True)
    return response_success_200(data=serializer.data)
