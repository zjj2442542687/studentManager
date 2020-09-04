from course.models import Course
from timetable.models import Timetable
from utils.my_response import response_error_400


def add_course(timetable_id: int, course_id: int):
    if not Course.objects.filter(id=course_id):
        return response_error_400(message="课程id不存在")

    try:
        Timetable.objects.get(pk=timetable_id).course_info.add(course_id)
    except Timetable.DoesNotExist:
        return response_error_400(message="课表不存在")

    print(timetable_id)
    print(course_id)
    return None
