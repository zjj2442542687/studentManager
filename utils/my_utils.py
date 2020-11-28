import re

# '"1","2"' 的 字符串转换成 [1, 2] int数组
from django.db.models import QuerySet

from classs.models import Class
from regular.models import Regular
from regular_add_record.models import RegularAddRecord
from regular_category.models import RegularCategory
from regular_clock.models import RegularClock
from school.models import School
from student.models import Student
from teacher.models import Teacher
from user.models import User
from work.models import Work


def string_to_int_arr(s: str):
    s = s.split(",")
    s = [int(re.sub("\D", "", w)) for w in s]
    return s


# 获得所有queryset中的id
def get_queryset_all_id(queryset: QuerySet):
    return [r.id for r in queryset]


# 获得所有user中的id 返回list
def get_user_all_id() -> list:
    return get_queryset_all_id(User.objects.all())


# 获得所有school中的id 返回list
def get_school_all_id() -> list:
    return get_queryset_all_id(School.objects.all())


# 获得所有class中的id 返回list
def get_class_all_id() -> list:
    return get_queryset_all_id(Class.objects.all())


# 获得所有teacher中的id 返回list
def get_teacher_all_id() -> list:
    return get_queryset_all_id(Teacher.objects.all())


# 获得所有Student中的id 返回list
def get_student_all_id() -> list:
    return get_queryset_all_id(Student.objects.all())


# 获得所有regular中的id 返回list
def get_regular_all_id() -> list:
    return get_queryset_all_id(Regular.objects.all())


# 获得所有RegularCategory中的id 返回list
def get_regular_category_all_id() -> list:
    return get_queryset_all_id(RegularCategory.objects.all())


# 获得所有RegularClock中的id 返回list
def get_regular_clock_all_id() -> list:
    return get_queryset_all_id(RegularClock.objects.all())


# 获得所有RegularAddRecord中的id 返回list
def get_regular_add_record_all_id() -> list:
    return get_queryset_all_id(RegularAddRecord.objects.all())


# work 返回list
def get_work_all_id() -> list:
    return get_queryset_all_id(Work.objects.all())
